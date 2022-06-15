from rest_framework import serializers
from core.models import *


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


# Create User Serializer Class
# class User_Creation_Serializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         exclude = ['groups', 'user_permissions']

#     def create(self, validated_data):
#         print("Validated Data:", validated_data)
#         username = validated_data.pop("username")

#         return True
