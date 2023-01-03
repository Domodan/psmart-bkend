from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Users models | Profile.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    position = models.CharField(max_length=20, default="admin")
    email_verified_at = models.DateTimeField(default=datetime.today())
    avatar = models.ImageField(upload_to="profile", default="user.png")


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
    staff_number = models.CharField(max_length=50, default="2022/TR/0001")
    email = models.EmailField(max_length=50, blank=True)
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
    registration_number = models.CharField(max_length=50, default="2022/STD/0001")
    birthday = models.DateField()
    student_class = models.CharField(max_length=20)
    level = models.CharField(max_length=20)
    gender = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to="student", default="user.png")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Student"


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


# Post Save Signals

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()