from push_notifications.models import GCMDevice,APNSDevice
from rest_framework import serializers

class GCMDeviceSerializer(serializers.ModelSerializer):
	class Meta:
		model = GCMDevice
		fields = ('id','name','user','registration_id','active')
		read_only_fields =('id','user')

	def create(self, validated_data):
		gcm_obj,created = GCMDevice.objects.get_or_create(**validated_data)
		return gcm_obj	


class APNSDeviceSerializer(serializers.ModelSerializer):
	class Meta:
		model = APNSDevice
		fields = ('id','user','registration_id','user','active')
		read_only_fields = ('id',)

	# def create(self, validated_data):
	# 	import pdb;pdb.set_Trace()
	# 	apns_obj,created = APNSDevice.objects.create(**validated_data)
	# 	print apns_obj
	# 	return apns_obj	

	# def update(self,instance,validated_data):
	# 	import pdb;pdb.set_trace()
	# 	instance.registration_id = validated_data.get('registration_id', instance.registration_id)
	# 	instance.name = validated_data.get('name',instance.name)
	# 	instance.user = self.request.user
	# 	instance.save()
	# 	return instance	