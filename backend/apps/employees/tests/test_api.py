import pytest
from datetime import date, time
from decimal import Decimal
from rest_framework.test import APIClient
from rest_framework import status
from apps.employees.models import Employee, Skill, Availability


@pytest.fixture
def api_client():
    """Pytest fixture for API client."""
    return APIClient()


@pytest.fixture
def sample_skill():
    """Create a sample skill."""
    return Skill.objects.create(name="Register", description="Cash register operations")


@pytest.fixture
def sample_employee():
    """Create a sample employee."""
    return Employee.objects.create(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone_number="555-0100",
        hourly_rate=Decimal("15.50"),
        hire_date=date(2024, 1, 15),
        birth_date=date(2000, 5, 20),
    )


@pytest.mark.django_db
class TestSkillAPI:
    """Tests for Skill API endpoints."""
    
    def test_list_skills(self, api_client, sample_skill):
        """Test listing skills."""
        response = api_client.get('/api/skills/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['name'] == "Register"
    
    def test_create_skill(self, api_client):
        """Test creating a skill."""
        data = {
            'name': 'Stock',
            'description': 'Stocking shelves'
        }
        response = api_client.post('/api/skills/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'Stock'
        assert Skill.objects.filter(name='Stock').exists()
    
    def test_retrieve_skill(self, api_client, sample_skill):
        """Test retrieving a single skill."""
        response = api_client.get(f'/api/skills/{sample_skill.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == "Register"
    
    def test_update_skill(self, api_client, sample_skill):
        """Test updating a skill."""
        data = {'name': 'Register Updated', 'description': 'Updated description'}
        response = api_client.put(f'/api/skills/{sample_skill.id}/', data)
        assert response.status_code == status.HTTP_200_OK
        sample_skill.refresh_from_db()
        assert sample_skill.name == "Register Updated"
    
    def test_delete_skill(self, api_client, sample_skill):
        """Test deleting a skill."""
        response = api_client.delete(f'/api/skills/{sample_skill.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Skill.objects.filter(id=sample_skill.id).exists()


@pytest.mark.django_db
class TestEmployeeAPI:
    """Tests for Employee API endpoints."""
    
    def test_list_employees(self, api_client, sample_employee):
        """Test listing employees."""
        response = api_client.get('/api/employees/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['full_name'] == "John Doe"
    
    def test_create_employee(self, api_client, sample_skill):
        """Test creating an employee."""
        data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'phone_number': '555-0101',
            'hourly_rate': '16.00',
            'hire_date': '2024-02-01',
            'birth_date': '1998-03-15',
            'skill_ids': [sample_skill.id]
        }
        response = api_client.post('/api/employees/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['full_name'] == "Jane Smith"
        assert response.data['is_active'] is True
        assert len(response.data['skills']) == 1
        
        # Verify employee was created in database
        employee = Employee.objects.get(email='jane.smith@example.com')
        assert employee.skills.count() == 1
    
    def test_create_employee_duplicate_email(self, api_client, sample_employee):
        """Test that duplicate emails are rejected."""
        data = {
            'first_name': 'Another',
            'last_name': 'Person',
            'email': 'john.doe@example.com',  # Duplicate
            'phone_number': '555-9999',
            'hourly_rate': '15.00',
            'hire_date': '2024-02-01',
            'birth_date': '2000-01-01',
        }
        response = api_client.post('/api/employees/', data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data
    
    def test_retrieve_employee(self, api_client, sample_employee):
        """Test retrieving a single employee."""
        response = api_client.get(f'/api/employees/{sample_employee.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['full_name'] == "John Doe"
        assert response.data['email'] == "john.doe@example.com"
        assert 'age' in response.data
        assert 'is_minor' in response.data
    
    def test_update_employee(self, api_client, sample_employee):
        """Test updating an employee."""
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.updated@example.com',
            'phone_number': '555-0100',
            'hourly_rate': '17.50',
            'hire_date': '2024-01-15',
            'birth_date': '2000-05-20',
        }
        response = api_client.put(f'/api/employees/{sample_employee.id}/', data, format='json')
        assert response.status_code == status.HTTP_200_OK
        sample_employee.refresh_from_db()
        assert sample_employee.email == "john.updated@example.com"
        assert sample_employee.hourly_rate == Decimal("17.50")
    
    def test_partial_update_employee(self, api_client, sample_employee):
        """Test partially updating an employee."""
        data = {'hourly_rate': '18.00'}
        response = api_client.patch(f'/api/employees/{sample_employee.id}/', data, format='json')
        assert response.status_code == status.HTTP_200_OK
        sample_employee.refresh_from_db()
        assert sample_employee.hourly_rate == Decimal("18.00")
        assert sample_employee.email == "john.doe@example.com"  # Unchanged
    
    def test_delete_employee_soft_delete(self, api_client, sample_employee):
        """Test deleting an employee (soft delete)."""
        response = api_client.delete(f'/api/employees/{sample_employee.id}/')
        assert response.status_code == status.HTTP_200_OK
        
        # Employee still exists but is inactive
        sample_employee.refresh_from_db()
        assert sample_employee.is_active is False
        assert Employee.objects.filter(id=sample_employee.id).exists()
    
    def test_search_employees(self, api_client, sample_employee):
        """Test searching employees."""
        # Create another employee
        Employee.objects.create(
            first_name="Jane",
            last_name="Smith",
            email="jane@example.com",
            phone_number="555-0200",
            hourly_rate=Decimal("16.00"),
            hire_date=date(2024, 1, 1),
            birth_date=date(2000, 1, 1),
        )
        
        # Search by first name
        response = api_client.get('/api/employees/?search=Jane')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['first_name'] == "Jane"
    
    def test_filter_employees_by_active_status(self, api_client, sample_employee):
        """Test filtering employees by active status."""
        # Create inactive employee
        Employee.objects.create(
            first_name="Inactive",
            last_name="User",
            email="inactive@example.com",
            phone_number="555-0300",
            hourly_rate=Decimal("15.00"),
            hire_date=date(2024, 1, 1),
            birth_date=date(2000, 1, 1),
            is_active=False
        )
        
        # Filter active only
        response = api_client.get('/api/employees/?is_active=true')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['is_active'] is True


@pytest.mark.django_db
class TestEmployeeAvailabilityAPI:
    """Tests for Employee Availability nested endpoints."""
    
    def test_get_employee_availability(self, api_client, sample_employee):
        """Test getting employee availability."""
        # Create availability
        Availability.objects.create(
            employee=sample_employee,
            day_of_week=0,
            start_time=time(9, 0),
            end_time=time(17, 0),
        )
        
        response = api_client.get(f'/api/employees/{sample_employee.id}/availability/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['day_of_week'] == 0
    
    def test_create_employee_availability(self, api_client, sample_employee):
        """Test creating availability for an employee."""
        data = {
            'day_of_week': 1,
            'start_time': '10:00:00',
            'end_time': '18:00:00',
            'is_available': True
        }
        response = api_client.post(
            f'/api/employees/{sample_employee.id}/availability/',
            data,
            format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Availability.objects.filter(employee=sample_employee, day_of_week=1).exists()
    
    def test_create_multiple_availabilities(self, api_client, sample_employee):
        """Test creating multiple availabilities at once."""
        data = [
            {
                'day_of_week': 0,
                'start_time': '09:00:00',
                'end_time': '17:00:00',
            },
            {
                'day_of_week': 1,
                'start_time': '09:00:00',
                'end_time': '17:00:00',
            }
        ]
        response = api_client.post(
            f'/api/employees/{sample_employee.id}/availability/',
            data,
            format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert len(response.data) == 2
        assert Availability.objects.filter(employee=sample_employee).count() == 2
    
    def test_availability_validation(self, api_client, sample_employee):
        """Test that end_time must be after start_time."""
        data = {
            'day_of_week': 0,
            'start_time': '17:00:00',
            'end_time': '09:00:00',  # Invalid: before start_time
        }
        response = api_client.post(
            f'/api/employees/{sample_employee.id}/availability/',
            data,
            format='json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestAvailabilityAPI:
    """Tests for standalone Availability API endpoints."""
    
    def test_list_all_availability(self, api_client, sample_employee):
        """Test listing all availability records."""
        Availability.objects.create(
            employee=sample_employee,
            day_of_week=0,
            start_time=time(9, 0),
            end_time=time(17, 0),
        )
        
        response = api_client.get('/api/availability/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
    
    def test_filter_availability_by_employee(self, api_client, sample_employee):
        """Test filtering availability by employee."""
        Availability.objects.create(
            employee=sample_employee,
            day_of_week=0,
            start_time=time(9, 0),
            end_time=time(17, 0),
        )
        
        response = api_client.get(f'/api/availability/?employee={sample_employee.id}')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
