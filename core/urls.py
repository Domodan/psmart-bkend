from django.urls import path
from core.views import *


urlpatterns = [
    path('', index, name='index'),
    path('attendance/<str:user_type>', attendance, name='attendance'),
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
    path('user_profile/<int:pk>', user_profile, name='user_profile'),
    path('teacher_profile/<int:pk>', teacher_profile, name='teacher_profile'),
    path('student_profile/<int:pk>', student_profile, name='student_profile'),
]