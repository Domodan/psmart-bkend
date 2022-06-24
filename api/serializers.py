from rest_framework import serializers
from api.models import *


# User Serializer Class
class User_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['groups', 'user_permissions']
        
        # fields = [
        #     'username', 'first_name', 'last_name', 'email', 'last_login', 'date_joined',
        #     'is_staff', 'is_active', 'is_superuser', 'password', 'id'
        # ]


# Attendance Serializer Class
class Attendance_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
    
    def create(self, validated_data):
        print("Validated Data:", validated_data)
        name = validated_data.pop("name")
        user_type = validated_data.pop("user_type")

        if Attendance.objects.filter(name=name, user_type=user_type).exists():
            attendance = Attendance.objects.get(name=name, user_type=user_type)
        else:
            attendance = Attendance.objects.create(name=name, user_type=user_type, **validated_data)
        
        return attendance


# Create User Serializer Class
# class User_Creation_Serializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         exclude = ['groups', 'user_permissions']

#     def create(self, validated_data):
#         print("Validated Data:", validated_data)
#         username = validated_data.pop("username")

#         return True
