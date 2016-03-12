from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^map_information$', 'editor.views.map_information', name='Map Information'),
#	UPDATE movie action
    url(r'^select_map$', 'editor.views.select_map', name='Select map'),
#	CHANGE watch status of movie
 
    url(r'^logout$', 'editor.views.logout_view', name='Logout'),
# 	LOGIN post
    url(r'^Editor$', 'editor.views.Manage', name='Main Screen'),
#	LOGIN page
    url(r'^login$', 'editor.views.login_view', name='Login'),
    
    url(r'^login2$', 'editor.views.login2', name='Login'),

    url(r'^1982gonzo/([0-9a-zA-Z]+)$', 'editor.views.randomMapCreator', name='Random Map'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^$',  'editor.views.login_view', name='Home'),
#	uncomment if python-django-registration is installed
#    url(r'^accounts/', include('registration.backends.default.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
   # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
