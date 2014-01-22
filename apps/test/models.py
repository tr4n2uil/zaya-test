from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

from django.contrib.auth.models import User
from slugify import slugify


# User Account Class
class Account( models.Model ):
	id = models.AutoField( primary_key = True )
	user = models.OneToOneField( User )
	age = models.IntegerField( default = 0 )
	class_no = models.IntegerField( default = 0 )

	@staticmethod
	def find_or_create( user, *kwargs ):
		try:
			return Account.objects.get( user = user )
		except Account.DoesNotExist:
			return Account.objects.create( user = user )


# register signal handler
def create_person( sender, instance, created, **kwargs ):
	if created:
		user_account = Account.find_or_create( user = instance )

post_save.connect( create_person, sender = User )


# Attendance Class
class Attendance( models.Model ):
	id = models.AutoField( primary_key = True )
	owner = models.ForeignKey( User, related_name = 'user_attendance', on_delete = models.SET_NULL, null = True )
	ctime = models.DateTimeField( auto_now_add = True )
	mtime = models.DateTimeField( auto_now = True )


# Points Class
class Points( models.Model ):
	id = models.AutoField( primary_key = True )
	owner = models.ForeignKey( User, related_name = 'user_points', on_delete = models.SET_NULL, null = True )
	points = models.IntegerField( default = 0 )

# Behaviour Class
class Behaviour( models.Model ):
	id = models.AutoField( primary_key = True )
	name = models.CharField( max_length = 128, unique = True )
	points = models.IntegerField( default = 0 )
