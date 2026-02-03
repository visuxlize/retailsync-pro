from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Employee, Skill, Availability
from .serializers import (
    EmployeeSerializer,
    EmployeeListSerializer,
    SkillSerializer,
    AvailabilitySerializer
)


class SkillViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing skills.
    
    Provides CRUD operations for skills that employees can have.
    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing employees.
    
    Provides:
    - List: GET /api/employees/
    - Create: POST /api/employees/
    - Retrieve: GET /api/employees/{id}/
    - Update: PUT /api/employees/{id}/
    - Partial Update: PATCH /api/employees/{id}/
    - Delete: DELETE /api/employees/{id}/ (soft delete - sets is_active=False)
    - Availability: GET/POST /api/employees/{id}/availability/
    """
    queryset = Employee.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'skills']
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['first_name', 'last_name', 'hire_date', 'hourly_rate']
    ordering = ['last_name', 'first_name']
    
    def get_serializer_class(self):
        """Use lightweight serializer for list view."""
        if self.action == 'list':
            return EmployeeListSerializer
        return EmployeeSerializer
    
    def get_queryset(self):
        """Optimize queries with select_related and prefetch_related."""
        queryset = super().get_queryset()
        if self.action == 'list':
            queryset = queryset.prefetch_related('skills')
        elif self.action == 'retrieve':
            queryset = queryset.prefetch_related('skills', 'availability')
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        """
        Soft delete - set is_active to False instead of deleting.
        """
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(
            {"detail": "Employee deactivated successfully."},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['get', 'post'])
    def availability(self, request, pk=None):
        """
        Get or set employee availability.
        
        GET: Returns all availability records for the employee
        POST: Creates new availability records (can accept list)
        """
        employee = self.get_object()
        
        if request.method == 'GET':
            availabilities = employee.availability.all()
            serializer = AvailabilitySerializer(availabilities, many=True)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            # Support both single object and list of objects
            data = request.data
            is_many = isinstance(data, list)
            
            # Ensure employee is set
            if is_many:
                for item in data:
                    item['employee'] = employee.id
            else:
                data['employee'] = employee.id
            
            serializer = AvailabilitySerializer(data=data, many=is_many)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class AvailabilityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing employee availability.
    
    Usually accessed via /api/employees/{id}/availability/
    but also available at /api/availability/ for bulk operations.
    """
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['employee', 'day_of_week', 'is_available']
    ordering_fields = ['day_of_week', 'start_time']
    ordering = ['employee', 'day_of_week', 'start_time']
    
    def get_queryset(self):
        """Optimize queries."""
        return super().get_queryset().select_related('employee')
