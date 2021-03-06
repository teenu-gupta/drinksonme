from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
import urllib, mimetypes


# Create your models here.


def profile_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = 'user_id_' + str(instance.owner.id) + '.' + ext
    return '/'.join(['accounts/profile-image', str(instance.owner.id), filename])

class Person(models.Model):
	CURRENT_STATUS = ((0,'Male'),(1,'Female'))

	username = models.OneToOneField(User,related_name='profile')
	email = models.EmailField()
	gender = models.SmallIntegerField(choices=CURRENT_STATUS, blank = True, default = True)
	date_of_birth = models.DateField(blank=True)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)

	def __unicode__(self):
		return str(self.first_name)

class ProfileImage(models.Model):
	owner = models.OneToOneField(Person, unique=True , related_name= 'profile_image')
	image = models.ImageField(upload_to= profile_image_path , blank= True , null = True)


