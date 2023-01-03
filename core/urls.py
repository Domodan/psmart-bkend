from django.urls import path
from core.views import *


urlpatterns = [
    path('', index, name='index'),
    path('attendance_students', attendance_students, name='attendance_students'),
    path('attendance_teahcers', attendance_teahcers, name='attendance_teachers'),
    path('all_users', users, name='all_users'),
    path('add_user', add_user, name='add_user'),
    path('add_students', add_students, name='add_students'),
    path('add_teachers', add_teachers, name='add_teachers'),
    path('students', students, name='students'),
    path('teachers', teachers, name='teachers'),
    path('all_admin', all_admin, name='all_admin'),
    path('sign_in', sign_in, name='sign_in'),
    path('sign_out', sign_out, name='sign_out'),
    path('sign_up', sign_up, name='sign_up'),
]