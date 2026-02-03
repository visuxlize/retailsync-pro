from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, SkillViewSet, AvailabilityViewSet

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'skills', SkillViewSet, basename='skill')
router.register(r'availability', AvailabilityViewSet, basename='availability')

urlpatterns = [
    path('', include(router.urls)),
]
