from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.backends import ModelBackend


# Schools models.
class School(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    level = models.CharField(max_length=20)
    headteacher = models.CharField(max_length=20, blank=True)
    district = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "School"
        verbose_name_plural = "School"


# Teachers models
class Teacher(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=20)
    gender = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to="teacher", default="user.png")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teacher"


# Students models
class Student(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    birthday = models.DateField()
    student_class = models.CharField(max_length=20)
    level = models.CharField(max_length=20)
    gender = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to="student", default="user.png")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Student"


# Users models | Profile.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    positions = models.CharField(max_length=20)


# Attendance models
class Attendance(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    user_type = models.CharField(max_length=10, default="Student") # Student | Teacher
    status = models.CharField(max_length=10, default="Absent") # Present | Absent | Late
    time_in = models.DateTimeField()
    time_out = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Attendance"
        verbose_name_plural = "Attendance"


# Custom Authentication
class EmailAuthBackend(ModelBackend):
    def authenticate(self, username, password):
        print("Auth Username:", username)
        print("Auth Password:", password)
        # if '@' in username:
        #     kwargs = { 'email': username }
        # else:
        #     kwargs = { 'username': username }
        
        # try:
        #     user = User.objects.get(**kwargs)
        #     if check_password(password):
        #         return user
        # except User.DoesNotExist:
        #     return None
        try:
            user = User.objects.get(email=username)
            if user.check_passwrd(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
