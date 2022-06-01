from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.views import UserViewSet


router = DefaultRouter()
router.register(r'', UserViewSet, basename="UserViewSet")


urlpatterns = [
    path('', include(router.urls))
]