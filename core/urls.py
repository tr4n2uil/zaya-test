from django.conf import settings
from django.conf.urls import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()

from tastypie.api import Api
from apps.test import api

v1_api = Api( api_name='v1' )
v1_api.register( api.UserResource() )
v1_api.register( api.AccountResource() )
v1_api.register( api.AttendanceResource() )
v1_api.register( api.PointsResource() )
v1_api.register( api.BehaviourResource() )

urlpatterns = patterns('',

	# core
	url( r'^$', 'django.contrib.auth.views.login', { 'template_name': 'home.jade' }, name='home' ),
	url( r'^drive/(.*)$', 'django.views.static.serve', kwargs = { 'document_root': settings.MEDIA_ROOT } ),
	
	# auth urls
	url( r'^logout/$', 'django.contrib.auth.views.logout', { 'next_page': '/' }, name='logout' ),

	# api urls
	url( r'^api/', include( v1_api.urls ) ),
)

