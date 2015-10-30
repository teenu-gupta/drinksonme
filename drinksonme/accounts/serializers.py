from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator 
from rest_framework.authtoken.models import Token

from django.core.validators import MinLengthValidator
from rest_framework import serializers
from accounts.models import *

import re


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ('first_name','last_name','email','password','username')
		extra_kwargs = {'password': {'write_only': True}}

		def create(self, validated_data):
			user = User(
			email=validated_data['email'],
			username=validated_data['username'],
			first_name = validated_data['first_name'],
			last_name = validated_data['last_name'],
			password = validated_data['password']
			)
			# user.set_password(validated_data['password'])
			user.save()
			return user

class LoginSerializer(serializers.Serializer):
	username = serializers.CharField(max_length=100)
	password = serializers.CharField(validators=[MinLengthValidator(6)])

	
class TokenSerializer(serializers.Serializer):
	class Meta:
		model = Token
		fields = ('key',)
				

class EmailVerifySerializer(serializers.Serializer):
	email = serializers.EmailField()

	def validate_email(self,attrs,source):
		attrs['email']= attrs['email'].lower()
		email = attrs['email']
		return attrs 

class PersonSerializer(serializers.ModelSerializer):
	class Meta:
		model = Person
		field = ('username','email','gender','date_of_birth','first_name' , 'last_name',)

		



class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = ('image',)





		
