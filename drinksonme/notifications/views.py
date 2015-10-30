from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from push_notifications.models import GCMDevice, APNSDevice
from .serializers import GCMDeviceSerializer, APNSDeviceSerializer
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ObjectDoesNotExist

class AndroidView(generics.ListCreateAPIView):
    """
        Get registered android device data
    """
   
    model = GCMDevice
    serializer_class = GCMDeviceSerializer
    permission_classes = (permissions.IsAuthenticated,)
   
    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id)
   
    def post(self, request, format=None):
        """
            Register Android Device
        """
        try:
        	obj = GCMDevice.objects.get(registration_id=request.data['registration_id'])
        	serializer = self.serializer_class(obj, data=request.data)
        except ObjectDoesNotExist:
        	serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)



class AppleView(generics.ListCreateAPIView):
    """
        Get registered apple device data
    """
    model = APNSDevice
    serializer_class = APNSDeviceSerializer
    permission_classes = (permissions.IsAuthenticated,)


    def post(self, request, format=None):
        """
            Register Apple Device
        """
        try:
        	obj = APNSDevice.objects.get(registration_id=request.data['registration_id'])
        	serializer = self.serializer_class(obj,data=request.data)
        except ObjectDoesNotExist:
        	serializer=self.serializer_class(data=request.data)	
        
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
           

