from random import *
from math import *
from multiprocessing import *
import uuid

def singleton(class_):
  instances = {}
  def getinstance(*args, **kwargs):
    if class_ not in instances:
        instances[class_] = class_(*args, **kwargs)
    return instances[class_]
  return getinstance

def randomGen():
    return int(str(uuid.uuid4().int)[:8])

#------------------------ENVIRONMENTAL ASPECT--------------------------#

class EnvironmentalAspect(object):
    def __init__(self, Id = randomGen(), name = 'default', loc = [], duration = -1):
        self.ID = Id
        self.name = name
        self.creator = 'admin'
        self.location = loc
        self.draw = -1
        self.durationLock = Lock()
        self.permanent = duration

    def findCorners(self):
        if len(self.location) == 1:
            locTop = [(self.location)[0][0], (self.location)[0][1]]
            locBot = [(self.location)[0][0], (self.location)[0][1] + (self.location)[0][2]]
            return (locTop, locBot)
        TL = [min([x[0] for x in self.location]), min([y[1] for y in self.location])]         
        BR = [max([x[0] for x in self.location]), max([y[1] + y[2] for y in self.location])]
        return (TL,BR) 

class Building(EnvironmentalAspect):
    def __init__(self, Id = randomGen(), name = 'default', loc = [], typ = 'Building'):
        EnvironmentalAspect.__init__(self,Id ,name, loc)
        self.type = typ
    def changeType(self, typ):
        self.type = typ
        if typ == 'House' :
            self.draw = 0
        if typ == 'School' :
            self.draw = 1
        if typ == 'Hospital' :
            self.draw = 2

    def randomize(self, low_x, high_x , low_y, high_y, low_length, high_length):
        randx = randint(low_x,high_x)
        randy = randint(low_y,high_y)
        randlength = randint(low_length,high_length)
        randheight = randint(low_length,high_length)
        loc=[]
        for a in range(randheight):
            loc.append([randx+a,randy,randlength])
        return EAFactory().new(self.ID, "Building", "Building"+str(self.ID),loc)

class NaturalElement(EnvironmentalAspect):
    def __init__(self, Id = randomGen(), name = '', loc = '', typ = 'default'):
        EnvironmentalAspect.__init__(self, Id , name, loc)
        self.type = typ
    def changeType(self, typ):
        self.type = typ
        if typ == 'Tree' :
            self.draw = 3
        if typ == 'Water' :
            self.draw = 4

    def randomizeRiver(self, start_x, start_y):
        loc=[]
        rawIndex=0
        onYLength=0
        while True:
            length =randint(2,4)
            rndm = randint(0,1)
            if (start_y+rawIndex+length+rndm) >= 40 :
                loc.append([start_x+rawIndex,start_y+rawIndex,40-start_y-rawIndex])
                break
            loc.append([start_x+rawIndex,start_y+rawIndex+rndm,length,0])
            rawIndex+=1
        return EAFactory().new(self.ID,"NaturalElement","NaturalElement" + str(self.ID),loc,"Water")  
    
    def randomizeLake(self, low_x, high_x , low_y, high_y, low_length, high_length):
        randx = randint(low_x,high_x)
        randy = randint(low_y,high_y)
        
        randheight = randint(low_length,high_length)
        loc=[]
        for a in range(randheight):

            randlength1 = randint(low_length,high_length)
            randlength2 = randint(0,2)

            loc.append([randx+a,randy+randlength2,randlength1])
        return EAFactory().new(self.ID,"NaturalElement","NaturalElement" + str(self.ID),loc,"Water") 

class Road(EnvironmentalAspect):    
    def __init__(self, Id = randomGen(), name = 'default', loc = [], typ ='Road'):
        EnvironmentalAspect.__init__(self,Id , name, loc)
        self.draw= 5
        self.type = typ
    def checkAvailability(self,x,y,mapArray):
        return  x<len(mapArray) and y<len(mapArray) and y>0 and x>0 and mapArray[x][y][0]==3 
    def manhattanCalc(self,x1,y1,x2,y2):
        return sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))
    def manhattanDist(self,x1,y1,x2,y2,px,py):
        man=[]
        toX=x2
        toY=y2
        result = 0
        if True:  
            result = self.manhattanCalc(x1+1,y1,x2,y2)
            toX=x1+1
            toY=y1
            man.append([result,toX,toY])
        if True:
            result= self.manhattanCalc(x1,y1+1,x2,y2)
            toX=x1
            toY=y1+1
            man.append([result,toX,toY])
        if True:
            result= self.manhattanCalc(x1-1,y1,x2,y2)
            toX=x1-1
            toY=y1
            man.append([result,toX,toY])
        if True:
            result= self.manhattanCalc(x1,y1-1,x2,y2)
            toX=x1
            toY=y1-1
            man.append([result,toX,toY])
        man.sort()
        return man
    def drawRoad(self,fromPoint,toPoint,mapArray):
        try:
            loc=[]
            x = fromPoint[0]
            y = fromPoint[1]
            toX = toPoint[0]
            toY = toPoint[1]
            while mapArray[toX][toY][0]!=3:
                toX = toX+1
            queue2=[]
            queue=[]
            prevX=x
            prevY=y
            flag=0
            while (x != toX or y != toY):
                
                man=self.manhattanDist(x,y,toX,toY,prevX,prevY)
                
                if self.checkAvailability(man[0][1],man[0][2],mapArray):
                    loc.append([man[0][1],man[0][2],1])
                    queue.append([x,y])
                    flag=1
                    prevX=x
                    prevY=y
                    x=man[0][1]
                    y=man[0][2]
                    mapArray[x][y][0] = 0
                    mapArray[x][y][1] = 0

                elif self.checkAvailability(man[1][1],man[1][2],mapArray):
                    loc.append([man[1][1],man[1][2],1])
                    queue.append([x,y])
                    flag=1
                    prevX=x
                    prevY=y
                    x=man[1][1]
                    y=man[1][2]
                    mapArray[x][y][0] = 0
                    mapArray[x][y][1] = 0

                elif len(man)>=3 and self.checkAvailability(man[2][1],man[2][2],mapArray):
                    loc.append([man[2][1],man[2][2],1])
                    queue.append([x,y])
                    flag=1
                    prevX=x
                    prevY=y
                    x=man[2][1]
                    y=man[2][2]
                    mapArray[x][y][0] = 0
                    mapArray[x][y][1] = 0

                elif len(man)==4 and self.checkAvailability(man[3][1],man[3][2],mapArray):
                    loc.append([man[3][1],man[3][2],1])
                    queue.append([x,y])
                    flag=1
                    prevX=x
                    prevY=y
                    x=man[3][1]
                    y=man[3][2]
                    mapArray[x][y][0] = 0
                    mapArray[x][y][1] = 0

                else:
                    queue2.append([x,y]);
                    q=queue.pop()
                    x=q[0]
                    y=q[1]
                    loc.pop()
                if flag==1:
                    man=self.manhattanDist(x,y,fromPoint[0],fromPoint[1],prevX,prevY)
                    for m in man:
                        if mapArray[m[1]][m[2]][0]==0 and (m[1]==prevX and m[2]==prevY)==False:

                            q1=queue.pop()
                            q2 = [0,0]
                            while True:
                                q2=queue.pop()
                                print(q2)
                                print(m)
                                print([prevX,prevY])
                                if q2[0]==m[1] and q2[1]==m[2]:
                                    break
                                else:
                                    queue2.append([q2[0],q2[1]])
                            loc.append(q2)
                            loc.append(q1)
                            break
                    flag=0

            for a in queue2:
                mapArray[a[0]][a[1]][0] = 5
                mapArray[a[0]][a[1]][1] = 0               
            return EAFactory().new(self.ID,"Road","Road" + str(self.ID),loc,"Road")
        except Exception as e :
            print e     
@singleton
class EAFactory(object):
    def new(self,Id = randomGen(), asp = '', name = '', loc = '', typ = 'default'):
        if asp == 'Building':
            return Building(Id = randomGen(), name=name, loc=loc)
        if asp == 'NaturalElement':
            return NaturalElement(Id = randomGen(), name=name, loc=loc, typ=typ)
        if asp == 'Road':
            return Road(Id = randomGen(), name=name, loc=loc)

#-------------------------------MAP------------------------------------#            

class Map():
    def __init__(self, name = "defaultMap", owner = "admin", size = 100):
        self.regions = map(Semaphore, 25 * [1])
        self.regionSize = size / 5;
        self.userLock = Lock()
        self.changesLock = Lock()
        self.progressLock = Lock()
        self.totalChangesLength = 0 
        self.deletedChangesLength = 0 
        self.changes = []
        self.users = []
        self.name = name
        self.owner = owner
        self.buildings = []
        self.roads = []
        self.naturalElements = []
        self.permissions = []
        self.size = size
        self.mapArray = []
        self.progresses = []
        self.clearMapArray()

    def clearMapArray(self):
        self.mapArray = []
        for i in range(self.size):
            tempRaw=[]
            for j in range(self.size):
                tempRaw.append([3,0])
            self.mapArray.append(tempRaw)

    def locateMap(self, uid = -1):
        self.clearMapArray()
        for n in self.naturalElements:
            if (n.permanent == uid or n.permanent == -1):
                if(n.type=="Tree" and self.mapArray[n.location[0][0]][n.location[0][1]][0] ==3):
                    self.mapArray[n.location[0][0]][n.location[0][1]] = [2,self.mapArray[n.location[0][0]][n.location[0][1]][1]]

                if(n.type=="Water"):
                    for loc in n.location:
                        for i in range(loc[2]):
                            if (loc[1]+i)<40:
                                self.mapArray[loc[0]][loc[1]+i] = [4,self.mapArray[loc[0]][loc[1]+i][1]]

        for b in self.buildings:
            if (b.permanent == uid or b.permanent == -1):
                for loc in b.location:
                    for i in range(loc[2]):
                        self.mapArray[loc[0]][loc[1]+i][0] = 7


        for r in self.roads:
            if (r.permanent == uid or r.permanent == -1):
                for loc in r.location:
                    self.mapArray[loc[0]][loc[1]] = [0,self.mapArray[loc[0]][loc[1]][1]]

        #[uid,[locTop,locBot]] formatinda
                
        for p in self.progresses:
            for i in range(p[1][0][0],p[1][1][0]):
                for j in range(p[1][0][1],p[1][1][1]):
                    self.mapArray[i][j][1] = p[0]
        

    def randomize(self):
        self.buildings.append(Building().randomize(4,7,10,14,3,5))
        self.buildings.append(Building().randomize(15,20,11,20,2,5))
        self.buildings.append(Building().randomize(26,35,27,34,3,5))
        self.buildings.append(Building().randomize(1,4,30,34,2,5))

        self.naturalElements.append(NaturalElement().randomizeRiver(0,15))
        self.naturalElements.append(NaturalElement().randomizeLake(28,32,2,10,4,7))

        self.locateMap()
        
        fromBuilding=self.buildings[0]
        toBuilding=self.buildings[2]
        fromLocation = fromBuilding.location[len(fromBuilding.location)-3]
        toLocation = toBuilding.location[0]

        self.roads.append(Road().drawRoad([fromLocation[0],fromLocation[1]+fromLocation[2]-1],[toLocation[0],toLocation[1]-1],self.mapArray))

        for i in range(25):
            rndx= randint(25, 35)
            rndy= randint(25, 35)
            while self.mapArray[rndx][rndy][0]!=3:
                rndx= randint(25, 35)
                rndy= randint(25, 35)
            self.mapArray[rndx][rndy][0]=2
            self.naturalElements.append(EAFactory().new(randomGen(), "NaturalElement","Tree"+str(i),[[rndx,rndy,1]],"Tree"))

        for i in range(25):
            rndx= randint(1, 15)
            rndy= randint(25, 35)
            while self.mapArray[rndx][rndy][0]!=3:
                rndx= randint(1, 15)
                rndy= randint(25, 35)
            self.mapArray[rndx][rndy][0]=2
            self.naturalElements.append(EAFactory().new(randomGen(), "NaturalElement","Tree"+str(i),[[rndx,rndy,1]],"Tree"))

        for i in range(25):
            rndx= randint(25, 35)
            rndy= randint(3, 15)
            while self.mapArray[rndx][rndy][0]!=3:
                rndx= randint(25, 35)
                rndy= randint(3, 15)
            self.mapArray[rndx][rndy][0]=2
            self.naturalElements.append(EAFactory().new(randomGen(), "NaturalElement","Tree"+str(i),[[rndx,rndy,1]],"Tree"))
        self.locateMap()

    def isIntersect(self,locs):
        locConflicts=[]
        for loc in locs:
            for j in range(loc[1],loc[1]+loc[2]):
                if self.mapArray[loc[0]][j][0] != 3:
                    locConflicts.append([loc[0],j])
        return locConflicts

    def isProgress(self,locTop,locBot, ID):
        loc= []
        for i in range(locTop[0],locBot[0]):
            for j in range(locTop[1],locBot[1]):
                if self.mapArray[i][j][1] != 0:
                    loc.append([i,j])
        return loc


    def __str__(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.mapArray[i][j][1] > 0:
                    print_color('  ', bg=self.mapArray[i][j][0]+8, end='')
                else:
                    print_color('  ', bg=self.mapArray[i][j][0], end='')
            print("")

        return ""

    def printIntersection(self, loc, coord, size = 20):
        for i in range(coord[0], min([size + coord[0], self.size])):
            for j in range(coord[1], min([size + coord[1], self.size])):
                colored=0
                for k in loc:
                    if k[0]==i and k[1]==j:
                        colored=1
                        print_color('  ', bg=1, end='')
                        break
                if colored==0:    
                    print_color('  ', bg=self.mapArray[i][j][0], end='')

            print("")

    def printZoom(self, coord, size = 20):
        for i in range(coord[0], min([size + coord[0], self.size])):
            for j in range(coord[1], min([size + coord[1], self.size])):
                if self.mapArray[i][j][1] == 1:
                    print_color('  ', bg=self.mapArray[i][j][0]+8, end='')
                else:
                    print_color('  ', bg=self.mapArray[i][j][0], end='')
            print("")
        return ""
    
    def getBuildings(self):
        info = []
        if len(self.buildings) > 0 :
            if len(self.buildings) == 1 :
                info.append("There is 1 building in %s." %(self.name))
            else :
                info.append("There are %d buildings in %s \n\n" %(len(self.buildings), self.name))
            info.append("Building(s) List Here : \n")
            info.append("Building ID\t \tBulding Name\t \t Building Type")
            for b in self.buildings:
                info.append("     %d\t         |     \t%s         |         %s\n" % (b.ID, b.name, b.type))
        else :
            info.append("There is no building in %s" %(self.name))     
        return info       

    def getNaturalElements(self):
        info = []
        if len(self.naturalElements) > 0 :
            if len(self.naturalElements) == 1 :
                info.append("There is 1 natural element in %s \n\n" %(self.name))
            else :
                info.append("There are %d natural elements in %s \n\n" %(len(self.naturalElements), self.name))
            info.append("Natural Elemenet(s) List Here : \n")
            info.append("Elemenet ID\t \tElemenet Name\t \t Elemenet Type \n")
            for b in self.naturalElements:
                info.append("     %d\t         |     \t%s         |         %s\n" % (b.ID, b.name, b.type))
        else :
            info.append("There is no natural element in %s\n" %(self.name))   

        return info
    
    def getRoads(self):
        info = []
        if len(self.roads) > 0 :
            if len(self.naturalElements) == 1 :
                info.append("There is 1 road in %s\n\n" %(self.name))
            else :
                info.append("There are %d roads in %s\n\n" %(len(self.roads), self.name))
            info.append("Road(s) List Here : \n\n")
            info.append("Road ID\t \tRoad Name\n\n")
            for b in self.roads:
                info.append("     %d\t         |     \t%s \n" % (b.ID, b.name))
        else :
            info.append("There is no road in %s\n" %(self.name)) 
     
        return info

    def setPermission(self, user):
        if not user.ID in [x.ID for x in self.permissions]:
            self.permissions.append(user)
            print("%s can edit %s now." %(user.name, self.name))
        else:         
            print("%s is already permitted to edit %s." %(user.name, self.name))

    def getPermissions(self):
        if len(self.permissions) > 0 :
            if len(self.permissions) == 1 :
                print("Only 1 user can access to %s" %(self.name))
                print("")
            else :
                print("There are %d users who can access to %s" %(len(self.permissions), self.name))
                print("")
            print("User(s) List Here : ")
            print("")
            print("User Name")
            print("")
            for b in self.permissions:
                print("%s" % (b.name))
        print("")

    def getMapInfo(self):
        return self.getBuildings() + self.getNaturalElements() + self.getRoads()


#-------------------------------USER-----------------------------------#  

class User(object):
  def __init__(self, nam):
    self.ID = randomGen()
    self.session = ''
    self.name = nam
    self.currentMap = None
    self.proc = ActionProcess(self.ID)
    self.sight = [0,0,40]
  
  def changeName(self, nam):
    self.name = nam
  
  def refresh(self):
    Editor().maps[self.proc.mapID].locateMap(self.ID)

  def removeFromMap(self):
     for b in Editor().maps[self.proc.mapID].buildings:
        if b.permanent == self.ID:
            Editor().maps[self.proc.mapID].buildings.remove(b)
     for n in Editor().maps[self.proc.mapID].naturalElements:
        if n.permanent == self.ID:
            Editor().maps[self.proc.mapID].naturalElements.remove(b)
     for r in Editor().maps[self.proc.mapID].roads:
        if r.permanent == self.ID:
            Editor().maps[self.proc.mapID].roads.remove(b)
     for p in Editor().maps[self.proc.mapID].progresses:
        if p[0] == self.ID:
            Editor().maps[self.proc.mapID].progresses.remove(p)

  def enterMap(self,mapID):
    self.proc.mapID = mapID
    '''    ********************************************                  '''
    #new user added to the map 

    Editor().maps[self.proc.mapID].userLock.acquire()
    Editor().maps[self.proc.mapID].users.append([self.ID,Editor().maps[self.proc.mapID].totalChangesLength])
    Editor().maps[self.proc.mapID].setPermission(self)
    Editor().maps[self.proc.mapID].userLock.release()
       
    '''    ********************************************                  '''
  
  def quitMap(self):
    '''    ********************************************                  '''
    Editor().maps[self.proc.mapID].userLock.acquire()
    index=-1
    for z in range(len(Editor().maps[self.proc.mapID].users)):
      if Editor().maps[self.proc.mapID].users[z][0] == self.ID:
        index = z
        break
        
    del(Editor().maps[self.proc.mapID].users[index])
    self.proc.mapID = -1
    self.cleanUp()
    Editor().maps[self.proc.mapID].userLock.release()
    '''    ********************************************                  '''
  
  def takeAction(self, function = '', EA = None, locTop = [], locBot = [], pID = 0):
    if self.proc.mapID == -1:
      print ("map is not selected")
    elif self.ID in [x.ID for x in Editor().maps[self.proc.mapID].permissions]:
      if function == 'progress':
        return self.proc.progress(locTop, locBot)
      if function == 'add':
        return self.proc.addEA(EA)
      if function == 'delete':
        return self.proc.deleteEA(EA)
      if function == 'move':
        return self.proc.moveEA(EA, locTop)
      if function == 'stop':
        return self.proc.stopProgress(pID)
      if function == 'undoNext':
        return self.proc.undoNext()
      if function == 'undoAll':
        return self.proc.undoAll()

    else:
      print("%s is not permitted to edit %s." %(self.name, Editor().maps[self.proc.mapID].name))


  def cleanUp(self):
    if len(self.proc.progresses) != 0 :
      for prog in self.proc.progresses:
        self.proc.stopProgress(prog[2],0)
class ActionProcess(object):
  
  def __init__(self, ID):
    self.user = ID
    self.progresses = []
    self.undo = []
    self.mapID = -1

  def progress(self,locTop,locBot):

    response = 'DEFAULT'
    '''    ********************************************                  '''
    #find regions
    regionL = int(locTop[1] / Editor().maps[self.mapID].regionSize);
    regionR = regionL + int((locBot[1]-locTop[1])/Editor().maps[self.mapID].regionSize)
    
    regionT = int(locTop[0] / Editor().maps[self.mapID].regionSize);
    regionB = regionT + int((locBot[0]-locTop[0])/Editor().maps[self.mapID].regionSize)

    '''    ********************************************                  '''
    #lock regions
    for i in range (regionT,regionB+1):
      for j in range(regionL, regionR+1):
        Editor().maps[self.mapID].regions[i*5+j].acquire()

    '''    ********************************************                  '''
    #make progress area in use if it is not already
    usedBy = Editor().maps[self.mapID].isProgress(locTop,locBot, self.user)
    if usedBy == [] :
      pid = randomGen()
      new_progress = [self.user, [locTop,locBot], pid]
      '''    ********************************************                  '''  
      #append progress to map's progresses queue
      Editor().maps[self.mapID].progressLock.acquire()      
      Editor().maps[self.mapID].progresses.append(new_progress) 
      Editor().maps[self.mapID].progressLock.release()
      '''    ********************************************                  '''
      #append progress to changes queue
      Editor().maps[self.mapID].changesLock.acquire()
        
      Editor().maps[self.mapID].changes.append(['progress', Editor().maps[self.mapID].name, [locTop,locBot]])
      Editor().maps[self.mapID].totalChangesLength +=1

      Editor().maps[self.mapID].changesLock.release()     
      '''    ********************************************              '''
      #Mmake areas in use and add progress to map's progress list
      for i in range(locTop[0],locBot[0]):
        for j in range(locTop[1],locBot[1]):
          Editor().maps[self.mapID].mapArray[i][j][1] = self.user
        
      print("Progress is created " + str(Editor().maps[self.mapID].progresses))
      response = str(pid) + ". progress is successfully started."
      self.progresses.append(new_progress)
    else :      
      response = "A part of this area is currently in progress."

    '''    ********************************************                  '''
    #release locks
    for i in range (regionT,regionB+1):
      for j in range(regionL, regionR+1):
        Editor().maps[self.mapID].regions[i*5+j].release()
    return response
  
  def stopProgress(self, pID, saved = 1):
    if(self.user == self.user) :    #WORKAROUND FOR SIMPLICITY
        for e in self.progresses:
          if e[0] == self.user and e[2] == pID:

            '''    ********************************************                  '''
            #find regions
            locTop = [e[1][0][0],e[1][0][1]]
            locBot = [e[1][1][0],e[1][1][1]]
            regionL = int(locTop[1] / Editor().maps[self.mapID].regionSize);
            regionR = regionL + int((locBot[1]-locTop[1])/Editor().maps[self.mapID].regionSize)
            
            regionT = int(locTop[0] / Editor().maps[self.mapID].regionSize);
            regionB = regionT + int((locBot[0]-locTop[0])/Editor().maps[self.mapID].regionSize)
            '''    ********************************************                  '''  
            #delete progress from map's progresses queue
            Editor().maps[self.mapID].progressLock.acquire()      
            Editor().maps[self.mapID].progresses.remove(e)
            Editor().maps[self.mapID].progressLock.release()
            '''    ********************************************                  '''
            #lock regions 
            for i in range (regionT,regionB+1):
              for j in range(regionL, regionR+1):
                Editor().maps[self.mapID].regions[i*5+j].acquire()
            
            '''    ********************************************                  '''
            #append changes
            if saved == 1:
              Editor().maps[self.mapID].changesLock.acquire()
              for ch in self.undo:
                #makes added things permanent
                if ch[0] == "add":
                  ch[2].durationLock.acquire()
                  ch[2].permanent = -1
                  ch[2].durationLock.release()
                Editor().maps[self.mapID].changes.append(ch)
                Editor().maps[self.mapID].totalChangesLength +=1
              Editor().maps[self.mapID].changes.append(['stopprogress', Editor().maps[self.mapID].name, e[1]])
              Editor().maps[self.mapID].totalChangesLength +=1
              Editor().maps[self.mapID].changesLock.release()

            
            else:
              '''    ********************************************                  '''
              #delete all the changes
              for ch in self.undo:
                if ch[0] == "add":
                  if(isinstance(ch[2], Building)):
                    Editor().maps[self.mapID].buildings.remove(ch[2])
                  elif(isinstance(ch[2], NaturalElement)):
                    Editor().maps[self.mapID].naturalElements.remove(ch[2])
                  elif(isinstance(ch[2], Road)):
                    Editor().maps[self.mapID].roads.remove(ch[2])
              Editor().maps[self.mapID].changesLock.acquire()
              Editor().maps[self.mapID].changes.append(['stopprogress', Editor().maps[self.mapID].name, e[1]])
              Editor().maps[self.mapID].totalChangesLength +=1
              Editor().maps[self.mapID].changesLock.release()
            
            '''    ********************************************                  '''
            #make areas unuse
            for i in range(e[1][0][0], e[1][1][0]):
              for j in range(e[1][0][1], e[1][1][1]):
                Editor().maps[self.mapID].mapArray[i][j][1] = 0
            
            '''    ********************************************                  '''
            #release regions
            for i in range (regionT,regionB+1):
              for j in range(regionL, regionR+1):
                Editor().maps[self.mapID].regions[i*5+j].release()
            
            '''    ********************************************                  '''
            #delete progress

            self.progresses.remove(e)
            
            '''    ********************************************                  '''
            break
        return str(pID) + ". progress is successfully stopped."
    else:
        return "This process does not belong to you."

  def addEA(self, EA):
    locationConflicts = Editor().maps[self.mapID].isIntersect(EA.location)
    if self.isMyProgress(EA) == False:
      response = (EA.name) + " is not mine."
    elif locationConflicts != []:
      response = (EA.name) + " intersect with another Environmental Aspect. The intersection points are : " + str(locationConflicts)
    else:
      EA.durationLock.acquire()
      EA.permanent = self.user
      EA.durationLock.release()
      if(isinstance(EA, Building)):
        Editor().maps[self.mapID].buildings.append(EA)
      elif(isinstance(EA, NaturalElement)):
        Editor().maps[self.mapID].naturalElements.append(EA)
      elif(isinstance(EA, Road)):
        Editor().maps[self.mapID].roads.append(EA)
      response = EA.name + " is successfully added to " + Editor().maps[self.mapID].name + ". Added ID :" + str(EA.ID)
      Editor().maps[self.mapID].locateMap(self.user)
      self.undo.append(['add', Editor().maps[self.mapID].name, EA])
    return response

  def deleteEA(self, EA):
    if self.isMyProgress(EA) == False:
      response = (EA.name) + " is not mine."
    else:
      if(isinstance(EA, Building)):
        del Editor().maps[self.mapID].buildings[(Editor().maps[self.mapID].buildings.index(EA))]
      elif(isinstance(EA, NaturalElement)):
        del Editor().maps[self.mapID].naturalElements[(Editor().maps[self.mapID].naturalElements.index(EA))]
      elif(isinstance(EA, Road)):
        del Editor().maps[self.mapID].roads[(Editor().maps[self.mapID].roads.index(EA))]
      for l in EA.location:
        for i in range(l[1],l[1]+l[2]):
          Editor().maps[self.mapID].mapArray[l[0]][i][0] = 3
      response = EA.name + " is successfully deleted from " + Editor().maps[self.mapID].name + ". Deleted ID :" + str(EA.ID)
      Editor().maps[self.mapID].locateMap(self.user)
      self.undo.append(['delete', Editor().maps[self.mapID].name, EA])
    return response
    
  def moveEA(self, EA, loc):

    tempEA = EA
    tempCorners = EA.findCorners()
    diffLoc = [tempCorners[0][0] - loc[0], tempCorners[0][1] - loc[1]]
    loc = []

    response = ''
    for l in EA.location:
      newL = [l[0] - diffLoc[0], l[1] - diffLoc[1], l[2]]
      loc.append(newL)
    if(isinstance(EA, Building)):
      tempEA = Building(randomGen(), EA.name, loc, EA.type)
    elif(isinstance(EA, NaturalElement)):
      tempEA = NaturalElement(randomGen(), EA.name, loc, EA.type)
    elif(isinstance(EA, Road)):
      tempEA = Road(randomGen(), EA.name, loc)

    locationConflicts = Editor().maps[self.mapID].isIntersect(tempEA.location)
    if locationConflicts != []:
      response = EA.name + " intersect with another Environmental Aspect."
    elif self.isMyProgress(EA) == False:
      response = EA.name + " is not mine."
    else :
      self.deleteEA(EA)
      response = self.addEA(tempEA)
      Editor().maps[self.mapID].locateMap(self.user)
      self.undo.append(['move', Editor().maps[self.mapID].name, tempEA, tempCorners])
      for i in self.undo :
        if i[2] == EA :
          self.undo[self.undo.index(i)][2] = tempEA
      response = EA.name + " is successfully moved. New ID : " + str((response.split(':'))[1])
    return response

  def undoNext(self):
    if len(self.undo):
        try:
            action = self.undo.pop()
            '''
            mapIndex = 0
            for i in Editor().maps:
              if i.name == action[1]:
                break
              mapIndex += 1
            '''
            if action[0] == 'add':
              self.deleteEA(action[2])
            if action[0] == 'delete':
              self.addEA(action[2])
            if action[0] == 'move':
              self.moveEA(action[2], action[3][0])
            self.undo = self.undo[:-1]
            return "You successfully undo last " + action[0] + " operation." 
        except Exception as e:
            return str(e)
    else:
        return "There is no operation to undo."

  def undoAll(self):
    size = len(self.undo)
    if size :
        for i in range(size):
          self.undoNext()
        return "You successfully undo all queued operations."  
    else:
        return "There is no operation to undo."

  def isMyProgress(self, EA):
    corners = EA.findCorners()
    for k in self.progresses:
      print (k)
      if (corners[0][0] >= k[1][0][0] and corners[1][0] <= k[1][1][0]) and (corners[0][1] >= k[1][0][1] and corners[1][1] <= k[1][1][1]):
        return True
    return False

#-----------------------------EDITOR-----------------------------------#  

@singleton
class Editor(object):
  def __init__(self, maps = []):
    self.maps = maps
    self.users = []

  def addMap(self, mapp):
    self.maps.append(mapp)

  def addUser(self, user):
    self.users.append(user)

  def getUsers(self):
    if len(self.users) > 0 :
      print("There are %d users who are registered to Editor." %(len(self.users)))
      print(" ")
      print("User(s) List Here : ")
      print("")
      print("User Name")
      print("")
      for b in self.users:
        print("%s" % (b.name))
    print("")

   