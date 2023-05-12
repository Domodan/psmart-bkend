from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from api.models import Attendance, Profile, School, Student, Teacher, Subject, Timetable


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    # verbose_name = "User Profile"
    verbose_name_plural = "User Profile"


# Defining New Custom User Admin
class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline, ]

# Re-register User Admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# Register Subject model.
class Subject_Admin(admin.ModelAdmin):
    fields = [ 'name', ]

    list_display = ( 'name', 'created_at', 'updated_at' )

admin.site.register(Subject, Subject_Admin)



# Register Teacher model.
class Teacher_Admin(admin.ModelAdmin):
    fields = [
        'first_name', 'last_name', 'phone', 'subject', 'unique_id', 'gender', 'avatar'
    ]

    list_display = (
        'first_name', 'last_name', 'phone', 'get_subject', 'unique_id', 'gender', 'avatar'
    )


    def get_subject(self, obj):
        return [subject.name for subject in obj.subject.all()]

admin.site.register(Teacher, Teacher_Admin)


# Register Student model.
class Student_Admin(admin.ModelAdmin):
    fields = [
        'first_name', 'last_name', 'birthday', 'student_class', 'unique_id', 'gender', 'level', 'avatar'
    ]

    list_display = (
        'first_name', 'last_name', 'birthday', 'student_class', 'unique_id', 'gender', 'level', 'avatar'
    )

admin.site.register(Student, Student_Admin)


# Register School model.
class School_Admin(admin.ModelAdmin):
    fields = [ 'name', 'type', 'headteacher', 'district' ]

    list_display = ( 'name', 'type', 'headteacher', 'district' )

admin.site.register(School, School_Admin)


# Register Attendance model.
class Attendance_Admin(admin.ModelAdmin):
    fields = [ 'name', 'unique_id', 'user_type', 'subject', 'status', 'time_in', 'time_out' ]

    list_display = (
        'name', 'unique_id', 'user_type', 'subject', 'status', 'time_in', 'time_out',
        'created_at', 'updated_at'
    )

admin.site.register(Attendance, Attendance_Admin)


# Register Timetable model.
class Timetable_Admin(admin.ModelAdmin):
    fields = [
        'title', 'guestsField', 'eventDescriptionLabel', 'eventLocationLabel', 'repeatField',
        'image', 'className', 'start', 'end'
    ]

    list_display = (
        'title', 'guestsField', 'eventDescriptionLabel', 'eventLocationLabel', 'repeatField',
        'image', 'className', 'start', 'end', 'created_at', 'updated_at'
    )

admin.site.register(Timetable, Timetable_Admin)
