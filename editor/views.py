from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import redirect,render
from django.template import RequestContext, loader
from django.core.context_processors import csrf
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.sessions import *
from django.http import HttpResponse
from json import dumps, loads, JSONEncoder, JSONDecoder
from datetime import datetime
from random import randint
from .models import *

import time
from EditorServer import *

Types = {'Road' : 0, 'Tree' : 2, 'Water' : 4, 'Building' : 7, 'Selected' : 8, 'Progressed' : 9}

ActiveUser = None

class JSONPayload(object):
    def __init__(self, j):
         self.__dict__ = loads(j)
    def __getitem__(self, item):
    	return self.__dict__[item]

def addMapsToEditor():

	maps = MapObject.objects.all()

	for m in maps:

		tempMap = Map(name = m.Name)

		buildings = BuildingObject.objects.filter(Map = m)
		for b in buildings:
			temp = Building(Id = int(b.ID) , name = b.Name , loc =json.loads(b.Location))
			tempMap.buildings.append(temp)

		naturalElements = NaturalElementObject.objects.filter(Map = m)
		for n in naturalElements:
			temp = NaturalElement(Id = int(n.ID) , name = n.Name , loc = json.loads(n.Location), typ =n.Type)
			tempMap.naturalElements.append(temp)

		roads = RoadObject.objects.filter(Map = m)
		for r in roads:
			temp = Road(Id = int(r.ID) , name = r.Name , loc = json.loads(r.Location))
			tempMap.roads.append(temp)
		Editor().addMap(tempMap)    	

addMapsToEditor()

def randomMapCreator(request,mapName):
	newMap1 = Map(name = mapName)
	newMap1.randomize()

	m = MapObject.objects.create(Name =mapName)
	m.save
	for b in newMap1.buildings:
		try:
			c = BuildingObject.objects.create(ID = b.ID, 
				Name = b.name,
				Map = m,
				Location = dumps(b.location))
			c.save()
		except Exception as e:
			print e
	for r in newMap1.roads:
		try:
			c = RoadObject.objects.create(ID = r.ID, 
				Name = r.name,
				Map = m,
				Location = dumps(r.location))
			c.save()
		except Exception as e:
			print e
	for n in newMap1.naturalElements:
		try:
			c = NaturalElementObject.objects.create(Type = n.type,
				ID = n.ID, 
				Name = n.name,
				Map = m,
				Location = dumps(n.location))
			c.save()
		except Exception as e:
			print e
	return redirect("/login")

def prepareDictionary(TYPE, NAME, ID, LOC):
	return {'TYPE': TYPE, 'NAME': str(NAME), 'ID': ID, 'LOC': LOC}

def insideArea(locations):
	global ActiveUser
	inArea = True
	LOC = []
	for i in locations:
		inArea = True
		if (i[0] < ActiveUser.sight[0]) or i[0] > (ActiveUser.sight[0] + ActiveUser.sight[2]) or (i[1] < ActiveUser.sight[1]) or (i[1]+i[2] > ActiveUser.sight[1] + ActiveUser.sight[2]):
			inArea = False
		if inArea:
			LOC.append([i[0] - ActiveUser.sight[0], i[1] - ActiveUser.sight[1], i[2]])
	return LOC

def session_process(request):
	global ActiveUser
	try:
		last_activity = request.session['last_activity']
		now = time.time()
		key = request.session.session_key
		try:
			ActiveUser = [u for u in Editor().users if str(u.session) == str(key)][0]
			print ActiveUser
		except IndexError as e:
			print e
			return redirect("/login")
		
		if (now - last_activity)/60.0 > 5:
			ActiveUser.removeFromMap()
			removedUser = [u for u in Editor().users if str(u.session) == str(key)][0]
			Editor().users.remove(removedUser)
			ActiveUser = None
			del request.session['last_activity']
			logout(request)
			return redirect("/login")
			#return render(request, 'login.html', {'message':'Session is expired'})
	   	request.session['last_activity'] = now
	except Exception as e:
		print e
		return redirect("/Editor")

def findEA(ID):
	for b in Editor().maps[ActiveUser.proc.mapID].buildings:
		if b.ID == ID:
			return b
	for n in Editor().maps[ActiveUser.proc.mapID].naturalElements:
		if n.ID == ID:
			return n
	for r in Editor().maps[ActiveUser.proc.mapID].roads:
		if r.ID == ID:
			return r
	return None

def locationAdjuster(loc, OPname):
	global ActiveUser
	
	if OPname == 'START':
		return [[loc[0][0] + ActiveUser.sight[0], loc[0][1] + ActiveUser.sight[1]], [loc[1][0] + ActiveUser.sight[0], loc[1][1] + ActiveUser.sight[1]]]
	elif OPname == 'MOVE':
		return [loc[0] + ActiveUser.sight[0], loc[1] + ActiveUser.sight[1]]
	else : 
		LOC = []
		for i in loc:
			pass

def mapToDictionary():
	global ActiveUser

	shownMapDict = []
	for progress in Editor().maps[ActiveUser.proc.mapID].progresses:
		if((progress[1][0][0] > ActiveUser.sight[0]) and (progress[1][1][0] < ActiveUser.sight[0] + ActiveUser.sight[2]) and (progress[1][0][1] > ActiveUser.sight[1]) and (progress[1][1][1] < ActiveUser.sight[1] + ActiveUser.sight[2])):
			LOC = [[progress[1][0][0] - ActiveUser.sight[0], progress[1][0][1] - ActiveUser.sight[1]], [progress[1][1][0] - ActiveUser.sight[0], progress[1][1][1] - ActiveUser.sight[1]]]
			print LOC
			temp = prepareDictionary(Types['Progressed'], progress[0], progress[2], LOC)
			shownMapDict.append(temp)
	for aspect in Editor().maps[ActiveUser.proc.mapID].buildings:
		LOC = insideArea(aspect.location)
		if (aspect.permanent == ActiveUser.ID or aspect.permanent == -1) and len(LOC):
			temp = prepareDictionary(Types['Building'], aspect.name, aspect.ID, LOC)
			shownMapDict.append(temp)
	for aspect in Editor().maps[ActiveUser.proc.mapID].roads:
		LOC = insideArea(aspect.location)
		if (aspect.permanent == ActiveUser.ID or aspect.permanent == -1) and len(LOC):
			temp = prepareDictionary(Types['Road'], aspect.name, aspect.ID, LOC)
			shownMapDict.append(temp)
	for aspect in Editor().maps[ActiveUser.proc.mapID].naturalElements:
		LOC = insideArea(aspect.location)
		if (aspect.permanent == ActiveUser.ID or aspect.permanent == -1) and len(LOC):
			temp = prepareDictionary(Types[aspect.type], aspect.name, aspect.ID, LOC)
			shownMapDict.append(temp)
	return shownMapDict	

def login_view(request):
	'''Show login form'''
	try:
		context =  {'message':''}
		return render(request, 'login.html', context)
	except Exception as e:
		print e
		return redirect("/login")

def login2(request):
	'''Login to system'''
	global ActiveUser
	try:
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				request.session['last_activity'] = time.time()	
				new_active_user = User(username)
				new_active_user.session = request.session.session_key
				ActiveUser = new_active_user
				Editor().users.append(ActiveUser)
				return redirect("/select_map")
			else:
				return render(request, 'login.html', {'message':'Account is disabled'})
		else:
			return render(request, 'login.html', {'message':'Invalid username or password'})
	except Exception as e:
		print e
		return redirect("/login")

def logout_view(request):
	'''Simply logout'''
	global ActiveUser
	try:
		session_process(request)
		ActiveUser.removeFromMap()
		Editor().users.remove(ActiveUser)
		del request.session['last_activity']
		ActiveUser = None
		logout(request)
		return redirect("/login")
	except Exception as e:
		print e
		return redirect("/login")


@login_required(login_url='/login')
def Manage(request):
	'''Main Map Screen'''
	global ActiveUser
	try:
		session_process(request)
		message = ''
		response = {}
		obj =  None
		if request.method == 'POST' :
			if request.META['HTTP_REFERER'].split('/')[-1] == 'Editor':
				print request.POST
				JSONObj = JSONPayload(request.POST['JSON'])
				
				if JSONObj['OP'] == 'START':
					message = ActiveUser.takeAction('progress', None, JSONObj['LOC'][0], JSONObj['LOC'][1])
					if 'success' in message:
						obj = (prepareDictionary(Types['Progressed'], ActiveUser.ID, int(message.split('.')[0]), JSONObj['LOC']))
				
				if JSONObj['OP'] == 'ADD':
					if(JSONObj['TYPE'] == 'Natural Element'):
						newEA = EAFactory().new(randomGen(),'NaturalElement', JSONObj['NAME'], JSONObj['LOC'], JSONObj['NETYPE'])
						print newEA
					else:
						newEA = EAFactory().new(randomGen(), JSONObj['TYPE'], JSONObj['NAME'], JSONObj['LOC'])
					message = ActiveUser.takeAction('add', newEA) 
					if 'success' in message:
						if(JSONObj['TYPE'] == 'Natural Element'):
							obj = (prepareDictionary(Types[JSONObj['NETYPE']], JSONObj['NAME'], newEA.ID, JSONObj['LOC']))
						else:
							obj = (prepareDictionary(Types[JSONObj['TYPE']], JSONObj['NAME'], newEA.ID, JSONObj['LOC']))	
						try:
							m = MapObject.objects.get(Name = Editor().maps[ActiveUser.proc.mapID].name)	
						except Exception as e:
							print e		
						if JSONObj['TYPE'] == "Building":
							try:
								c = BuildingObject.objects.create(ID = newEA.ID, 
									Name = newEA.name,
									Map = m,
									Location = dumps(newEA.location))
								c.save()
							except Exception as e:
								print e
						if JSONObj['TYPE'] == "Road":
							try:
								c = RoadObject.objects.create(ID = newEA.ID, 
									Name = newEA.name,
									Map = m,
									Location = dumps(newEA.location))
								c.save()
							except Exception as e:
								print e
						else:
							try:
								c = NaturalElementObject.objects.create(Type = newEA.type,
									ID = newEA.ID, 
									Name = newEA.name,
									Map = m,
									Location = dumps(newEA.location))
								c.save()
							except Exception as e:
								print e
				if JSONObj['OP'] == 'DELETE':
					deletedEA = findEA(JSONObj['ID'])
					message = ActiveUser.takeAction('delete', deletedEA)
					if 'success' in message:
						if deletedEA.type == "Building":
							try:
								BuildingObject.objects.get(ID = deletedEA.ID).delete()
							except Exception as e:
								print e
						if deletedEA.type == "Road":
							try:
								RoadObject.objects.get(ID = deletedEA.ID).delete()
							except Exception as e:
								print e
						else:
							try:
								NaturalElementObject.objects.get(ID = deletedEA.ID).delete()
							except Exception as e:
								print e

				if JSONObj['OP'] == 'MOVE':
					message = ActiveUser.takeAction('move', findEA(JSONObj['ID']), JSONObj['LOC'])
					if 'success' in message:
						newEA = findEA(int(message.split(':')[-1]))
						obj = (prepareDictionary(Types[newEA.type], newEA.name, newEA.ID, newEA.location))				
				
				if JSONObj['OP'] == 'STOP':
					message = ActiveUser.takeAction('stop', pID=JSONObj['ID']) 

				if JSONObj['OP'] == 'UNDO':
					message = ActiveUser.takeAction('undoNext')
					print message
					if 'success' in message:
						obj = mapToDictionary()

				if JSONObj['OP'] == 'UNDOALL':
					message = ActiveUser.takeAction('undoAll')
					if 'success' in message:
						obj = mapToDictionary()
				
				if JSONObj['OP'] == 'REFRESH':
					message = "You successfully refreshed the map."
					if 'success' in message:
						obj = mapToDictionary()

				if JSONObj['OP'] == 'CHANGE':
					message = "You successfully change the location."
					if 'success' in message:
						ActiveUser.sight[0], ActiveUser.sight[1] = JSONObj['LOC'][0], JSONObj['LOC'][1]
						obj = mapToDictionary()      

				print message
				response = {'RESULT': message, 'OBJECT': obj}
				return HttpResponse(dumps(response), content_type = "application/json")

		Editor().maps[ActiveUser.proc.mapID].locateMap(ActiveUser.ID)
 		shownMapDict = mapToDictionary()
		context =  {'message': message, 'map': shownMapDict}
		return render(request, 'Editor.html', context)
	except Exception as e:
		print "Editor Exception : " + str(e)
		return render(request, 'Editor.html', '')


@login_required(login_url='/login')
def select_map(request):
	'''Map selection'''
	global ActiveUser
	session_process(request)
	maps = [n.name for n in Editor().maps]
	context = {'maps': maps}
	return render(request, 'select_map.html', context)

@login_required(login_url='/login')
def map_information(request):
	'''Map selection'''
	global ActiveUser
	message = 'Map selected.'
	session_process(request)
	map_name = request.POST['MAP']
	map_index = [Editor().maps.index(m) for m in Editor().maps if m.name == map_name][0]
	#map_info = Editor().maps[map_index].getMapInfo()
	ActiveUser.enterMap(map_index)
 	shownMapDict = mapToDictionary()
	context =  {'message': message, 'map': shownMapDict}
	return redirect("/Editor")
	#return render(request, 'Editor.html', context)


