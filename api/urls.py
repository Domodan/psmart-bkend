from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet, AttendanceViewSet


router = DefaultRouter()
router.register(r'user', UserViewSet, basename="UserViewSet")
router.register(r'attendance', AttendanceViewSet, basename="AttendanceViewSet")


urlpatterns = [
    path('', include(router.urls))
]