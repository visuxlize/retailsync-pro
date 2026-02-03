from rest_framework import serializers
from .models import Employee, Skill, Availability


class SkillSerializer(serializers.ModelSerializer):
    """Serializer for Skill model."""
    
    class Meta:
        model = Skill
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class AvailabilitySerializer(serializers.ModelSerializer):
    """Serializer for Availability model."""
    day_of_week_display = serializers.CharField(source='get_day_of_week_display', read_only=True)
    
    class Meta:
        model = Availability
        fields = [
            'id',
            'employee',
            'day_of_week',
            'day_of_week_display',
            'start_time',
            'end_time',
            'is_available',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def validate(self, data):
        """Ensure end_time is after start_time."""
        if data.get('start_time') and data.get('end_time'):
            if data['end_time'] <= data['start_time']:
                raise serializers.ValidationError({
                    'end_time': 'End time must be after start time.'
                })
        return data


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for Employee model with full details."""
    full_name = serializers.CharField(read_only=True)
    age = serializers.IntegerField(source='get_age', read_only=True)
    is_minor = serializers.BooleanField(read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    skill_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=Skill.objects.all(),
        source='skills',
        required=False
    )
    availability = AvailabilitySerializer(many=True, read_only=True)
    
    class Meta:
        model = Employee
        fields = [
            'id',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'phone_number',
            'hourly_rate',
            'hire_date',
            'birth_date',
            'age',
            'is_minor',
            'skills',
            'skill_ids',
            'availability',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_hourly_rate(self, value):
        """Ensure hourly rate is positive."""
        if value <= 0:
            raise serializers.ValidationError("Hourly rate must be greater than 0.")
        return value
    
    def validate_email(self, value):
        """Ensure email is unique (case-insensitive)."""
        email = value.lower()
        instance = self.instance
        
        # Check if updating existing employee
        if instance:
            if Employee.objects.exclude(pk=instance.pk).filter(email__iexact=email).exists():
                raise serializers.ValidationError("An employee with this email already exists.")
        else:
            if Employee.objects.filter(email__iexact=email).exists():
                raise serializers.ValidationError("An employee with this email already exists.")
        
        return value


class EmployeeListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for employee lists."""
    full_name = serializers.CharField(read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    
    class Meta:
        model = Employee
        fields = [
            'id',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'hourly_rate',
            'skills',
            'is_active'
        ]
