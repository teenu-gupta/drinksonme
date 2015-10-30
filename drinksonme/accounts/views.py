from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from serializers import RegisterSerializer , LoginSerializer , EmailVerifySerializer , PersonSerializer, ProfileImageSerializer
from django.contrib.auth import authenticate, get_user_model , logout
from accounts.models import *
import datetime
import random


# Create your views here

class Register(generics.CreateAPIView):

	serializer_class = RegisterSerializer
	
	

	# import ipdb;ipdb.set_trace()
	def get_serializer_class(self):
		return self.serializer_class



class Login(generics.GenericAPIView):

	"""
		login a existing user to system
	"""
	serializer_class = LoginSerializer

	
	def post(self,request):
		# import ipdb; ipdb.set_trace()
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			user = authenticate(username=serializer.data['username'],
								password = serializer.data['password'])

			if user and user.is_authenticated():
				if user.is_active:
					return Response({'first_name':user.first_name,
									  'last_name': user.last_name,

									  },status= status.HTTP_200_OK)
				else:
					return Response({'error':['Invalid Username/Password']},status = status.HTTP_401_UNAUTHORIZED)

						
			else:
				return Response({'error': ['Invalid Username/Password.']},status=status.HTTP_401_UNAUTHORIZED)
				
		else:
			return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def get(self,request):
		# import ipdb; ipdb.set_trace()
		try:
			logout(request)
			return Response({'sucsess':'Sucessfully Logged out.'},status= status.HTTP_200_OK)
		except Exception, e:
			print e
		return Response (status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmailVerify(generics.GenericAPIView):
	"""
	Verify Email
	"""
	serializer_class = EmailVerifySerializer
	def post(self, request):
		serializer = self.serializer_class(data.request.DATA)
		if serializer.is_valid():
			try:
				user = User.objects.get(email=serializer.data['email'])
			except:
				return Response({'error':'Email id does not exist'})
			q = UserEmailVerify()
			q.delay(ctx={'user':user,'email':user.email,'uid':urlsafe_base64_encode(force_bytes(user.pk)),
				'token':tg.make_token(user),'protocol':settings.PROTOCOL})
			return Response({'success':'Email Verification mail has been sent'})
		else:
			return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
			

# class ProfileCreate(generics.CreateAPIView):
# 	"""
# 	Create a profile
# 	"""
# 	serializer_class = PersonSerializer
# 	queryset = Person.objects.all()

class ProfileUpdate(generics.GenericAPIView):
	"""
	Update a Profile

	"""
	model = Person
	serializer_class = PersonSerializer

	def get(self,request,pk):
		person = Person.objects.get(pk=request.user.pk)
		serializer = PersonSerializer(person)
		return Response(data=serializer.data,status=status.HTTP_200_OK)

class ProfileCreate(generics.GenericAPIView):
	"""
	Create A User Profile

	"""
	model = Person
	serializer_class = PersonSerializer

	def post(self,request):
		serializer = self.serializer_class(data=request.data)
		
		if serializer.is_valid():
			serializer.save()
			return Response(data=serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileImageView(generics.GenericAPIView):
    """
        Add and remove person profile image
    """

    model = ProfileImage
    serializer_class = ProfileImageSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # def get(self, request):
    #     profile_image = self.model.objects.get(owner__owner=request.user)
    #     serializer = self.serializer_class(profile_image)
    #     return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        profile_image = self.model.objects.get(owner__owner=request.user)
        serializer = self.serializer_class(profile_image, data=request.DATA,
                                           files=request.FILES)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request):
        obj = get_object_or_404(ProfileImage,owner__owner=self.request.user)
        obj.image = ""
        obj.save()
        data = {"Details": "Profile Image is deleted successfully"}
        return Response(data)

