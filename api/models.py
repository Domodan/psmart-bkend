from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


# Subjects.
class Subjects:
    english = "English"
    math = "Mathematics"
    science = "Science"
    sst = "Social Studies"

    CHOICES = (
        ("ENG", english),
        ("MTC", math),
        ("SCI", science),
        ("SST", sst)
    )

# Subjects models 
class Subject(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


# Users models | Profile.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    position = models.CharField(max_length=20, default="admin")
    email_verified_at = models.DateTimeField(default=timezone.now)
    avatar = models.ImageField(upload_to="profile", default="user.png")


# Schools models.
class School(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    level = models.CharField(max_length=20)
    headteacher = models.CharField(max_length=20, blank=True)
    district = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "School"
        verbose_name_plural = "School"


# Teachers models
class Teacher(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    unique_id = models.CharField(max_length=50, default="2022/TR/1")
    email = models.EmailField(max_length=50, blank=True)
    phone = models.CharField(max_length=15)
    school = models.CharField(max_length=50, default="Makerere Primary")
    subject = models.CharField(max_length=20)
    subject2 = models.CharField(max_length=20, choices=Subjects.CHOICES, default=Subjects.english)
    subject3 = models.ManyToManyField(to="api.Subject", related_name="teachers", verbose_name="Subjects")
    gender = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to="teacher", default="user.png")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.first_name

    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teacher"


# Students models
class Student(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    unique_id = models.CharField(max_length=50, default="2022/STD/1")
    birthday = models.DateField()
    student_class = models.CharField(max_length=20)
    school = models.CharField(max_length=50, default="Makerere Primary")
    level = models.CharField(max_length=20)
    gender = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to="student", default="user.png")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.first_name

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Student"


# Attendance models
class Attendance(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    unique_id = models.CharField(max_length=50, default="2022/TR/10")
    user_type = models.CharField(max_length=10, default="Student") # Student | Teacher
    status = models.CharField(max_length=10, default="Absent") # Present | Absent | Late
    subject = models.CharField(max_length=20, default="English")
    time_in = models.DateTimeField()
    time_out = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Attendance"
        verbose_name_plural = "Attendance"


# Timetable Schedule models
class Timetable(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50, verbose_name="Event Title")
    guestsField = models.ForeignKey(Teacher, on_delete=models.CASCADE,
                                    verbose_name="teacher", related_name="teacher")
    eventDescriptionLabel = models.CharField(max_length=50, verbose_name="Description")
    eventLocationLabel = models.CharField(max_length=20, verbose_name="Venue")
    repeatField = models.CharField(max_length=10, verbose_name="Repeat Field")
    image = models.ImageField(upload_to="timetable", default="figma-icon.svg")
    className = models.CharField(max_length=50, verbose_name="Class Theme", default="fullcalendar-custom-event-holidays")
    start = models.DateTimeField(verbose_name="Start Time")
    end = models.DateTimeField(verbose_name="End Time")
    allDays = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Timetable"
        verbose_name_plural = "Timetable"


# Post Save Signals

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()