from django.conf.urls import url
from django.db.models import Sum
from django.contrib.auth.models import User
from tastypie import fields, resources, authorization

from apps.test.models import Account, Attendance, Points, Behaviour


# User Resource Class
class UserResource( resources.ModelResource ):
	class Meta:
		queryset = User.objects.all()
		resource_name = 'user'
		fields = [ 'username', 'first_name', 'last_name', 'last_login' ]
		detail_uri_name = 'username'

	def prepend_urls( self ):
		return [ url( r"^(?P<resource_name>%s)/(?P<username>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view( 'dispatch_detail' ), name="api_dispatch_detail" ), ]


# Account Resource Class
class AccountResource( resources.ModelResource ):
	user = fields.ForeignKey( UserResource, 'user', full = True )
	attendance = fields.IntegerField( readonly = True )
	points = fields.IntegerField( readonly = True )

	class Meta:
		queryset = Account.objects.all()
		resource_name = 'account'
		authorization = authorization.Authorization()

	def obj_create( self, bundle, request = None, **kwargs ):
		username, email, password, age = bundle.data[ 'username' ], bundle.data[ 'email' ], bundle.data[ 'password' ], bundle.data[ 'age' ]

		try:
			user = User.objects.create_user( username, email, password )
			bundle.obj = user.get_profile()
			bundle.obj.age = age
			bundle.obj.save()
		except IntegrityError:
			raise BadRequest( 'That username already exists' )

		return bundle

	def dehydrate_attendance( self, bundle ):
		return bundle.obj.user.user_attendance.all().count()

	def dehydrate_points( self, bundle ):
		return bundle.obj.user.user_points.all().aggregate( Sum( 'points' ) )[ 'points__sum' ]


# Attendance Resource Class
class AttendanceResource( resources.ModelResource ):
	owner = fields.ForeignKey( UserResource, 'owner', full = True )

	class Meta:
		queryset = Attendance.objects.all()
		resource_name = 'attendance'
		authorization = authorization.Authorization()


# Behaviour Resource Class
class BehaviourResource( resources.ModelResource ):
	class Meta:
		queryset = Behaviour.objects.all()
		resource_name = 'behaviour'
		detail_uri_name = 'name'
		allowed_methods = ['get']

	def prepend_urls( self ):
		return [ url( r"^(?P<resource_name>%s)/(?P<name>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view( 'dispatch_detail' ), name="api_dispatch_detail" ), ]


# Points Resource Class
class PointsResource( resources.ModelResource ):
	owner = fields.ForeignKey( UserResource, 'owner', full = True )

	class Meta:
		queryset = Points.objects.all()
		resource_name = 'points'
		authorization = authorization.Authorization()

	def obj_create( self, bundle, request = None, **kwargs ):
		owner, behaviour = bundle.data[ 'owner' ], bundle.data[ 'behaviour' ]

		try:
			bundle.obj.owner = User.objects.get( username = owner.split( '/' )[ -2 ] )
			bundle.obj.points = Behaviour.objects.get( name = behaviour.split( '/' )[ -2 ] ).points
			bundle.obj.save()
		except Model.DoesNotExist:
			raise BadRequest( 'Invalid User and/or Behaviour' )

		return bundle	
