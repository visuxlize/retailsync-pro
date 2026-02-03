from django.contrib import admin
from .models import Employee, Skill, Availability


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """Admin interface for Skill model."""
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


class AvailabilityInline(admin.TabularInline):
    """Inline admin for employee availability."""
    model = Availability
    extra = 1
    fields = ['day_of_week', 'start_time', 'end_time', 'is_available']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """Admin interface for Employee model."""
    list_display = [
        'full_name',
        'email',
        'hourly_rate',
        'hire_date',
        'is_active',
        'is_minor'
    ]
    list_filter = ['is_active', 'hire_date', 'skills']
    search_fields = ['first_name', 'last_name', 'email']
    filter_horizontal = ['skills']
    inlines = [AvailabilityInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number')
        }),
        ('Employment Details', {
            'fields': ('hourly_rate', 'hire_date', 'birth_date', 'skills')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def is_minor(self, obj):
        """Display if employee is a minor."""
        return obj.is_minor()
    is_minor.boolean = True
    is_minor.short_description = 'Minor (<18)'


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    """Admin interface for Availability model."""
    list_display = [
        'employee',
        'day_of_week',
        'start_time',
        'end_time',
        'is_available'
    ]
    list_filter = ['day_of_week', 'is_available']
    search_fields = ['employee__first_name', 'employee__last_name']
    ordering = ['employee', 'day_of_week', 'start_time']
