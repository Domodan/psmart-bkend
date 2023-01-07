from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response

from api.serializers import *


# User ModelViewset.
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = User_Serializer


class UserViewSet(viewsets.ViewSet):

    def list(self, request): # GET
        queryset = User.objects.all()
        serializer = User_Serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request): # POST
        print("Request Data:", request.data)
        if request.data.get("action") is not None:
            action = request.data.get("action")
            if action == "getUser":
                user_type = request.data.get("user_type")
                unique_id = request.data.get("unique_id")
                if user_type == "teacher":
                    teacher = Teacher.objects.get(unique_id=unique_id)
                    serializer = Teacher_Serializer(teacher)
                elif user_type == "student":
                    student = Student.objects.get(unique_id=unique_id)
                    serializer = Student_Serializer(student)
                return Response(serializer.data, status=status.HTTP_200_OK)

                # action = request.data.get("action")
                # username = request.data.get("username")

                # email = request.data.get("email")
                # password = request.data.get("password")

                # if '@' in email:
                #     try:
                #         user = User.objects.get(email=email)
                #     except User.DoesNotExist:
                #         return Response(status=status.HTTP_404_NOT_FOUND)
                # else:
                #     try:
                #         user = User.objects.get(username=email)
                #     except User.DoesNotExist:
                #         return Response(status=status.HTTP_404_NOT_FOUND)
                
                # user = authenticate(username=email, password=password)
                # print("User:", user)

                # if user.check_password(password):
                #     serializer = User_Serializer(user)
                #     return Response(serializer.data, status=status.HTTP_200_OK)
                # else:
                #     return Response(data=None, status=status.HTTP_400_BAD_REQUEST)
        else:
            # serializer = User_Serializer(data=request.data)
            # if serializer.is_valid():
            #     serializer.save()
            #     return Response(serializer.data, status=status.HTTP_201_CREATED)
            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None): # GET
        try:
            queryset = get_object_or_404(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = User_Serializer(queryset)
        return Response(serializer.data, status.HTTP_302_FOUND)


    def update(self, request, pk=None): # PUT
        try:
            queryset = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = User_Serializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def partial_update(self, request, pk=None):
        pass


    def destroy(self, request, pk=None): # DELETE
        try:
            queryset = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AttendanceViewSet(viewsets.ViewSet):

    def list(self, request): # GET
        queryset = Attendance.objects.all()
        serializer = Attendance_Serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request): # POST
        print("Request Data:", request.data)

        action = request.data.get("action")
        user_action = request.data.get("user_action")
        user_type = request.data.get("user_type")
        username = request.data.get("username")
        unique_id = request.data.get("unique_id")

        if action == "old":
            if user_action == "Check In":
                queryset = Attendance.objects.filter(name=username, user_type=user_type).first()

                time_now = datetime.now()
                queryset.time_in = time_now

                queryset.save()

            elif user_action == "Check Out":
                queryset = Attendance.objects.filter(name=username, user_type=user_type).first()

                time_now = datetime.now()
                queryset.time_out = time_now

                queryset.save()
            
            else:
                queryset = Attendance.objects.filter(name=username, user_type=user_type).first()
            
            serializer = Attendance_Serializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            if Attendance.objects.filter(unique_id=unique_id, user_type=user_type).exists():
                if user_action == "Check In":
                    queryset = Attendance.objects.get(unique_id=unique_id, user_type=user_type)
                    time_now = datetime.now()
                    queryset.time_in = time_now
                    queryset.save()
                elif user_action == "Check Out":
                    queryset = Attendance.objects.get(unique_id=unique_id, user_type=user_type)
                    time_now = datetime.now()
                    queryset.time_out = time_now
                    queryset.save()
                # else:
                #     queryset = Attendance.objects.get(unique_id=unique_id, user_type=user_type)
                serializer = Attendance_Serializer(queryset)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                request_data = {}

                request_data["name"] = username
                request_data["unique_id"] = unique_id
                request_data["user_type"] = user_type
                request_data["status"] = "Present"

                time_now = datetime.now()
                time_out = time_now + timedelta(hours=1)

                request_data["time_in"] = time_now
                request_data["time_out"] = time_out

                serializer = Attendance_Serializer(data=request_data)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None): # GET
        try:
            queryset = get_object_or_404(pk=pk)
        except Attendance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = Attendance_Serializer(queryset)
        return Response(serializer.data, status.HTTP_302_FOUND)


    def update(self, request, pk=None): # PUT
        try:
            queryset = Attendance.objects.get(pk=pk)
        except Attendance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = Attendance_Serializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def partial_update(self, request, pk=None):
        pass


    def destroy(self, request, pk=None): # DELETE
        try:
            queryset = Attendance.objects.get(pk=pk)
        except Attendance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


