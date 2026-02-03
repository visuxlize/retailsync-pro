import pytest
from datetime import date, time
from decimal import Decimal
from django.core.exceptions import ValidationError
from apps.employees.models import Employee, Skill, Availability


@pytest.mark.django_db
class TestSkillModel:
    """Tests for Skill model."""
    
    def test_create_skill(self):
        """Test creating a skill."""
        skill = Skill.objects.create(
            name="Register",
            description="Cash register operations"
        )
        assert skill.name == "Register"
        assert skill.description == "Cash register operations"
        assert str(skill) == "Register"
    
    def test_skill_unique_name(self):
        """Test that skill names must be unique."""
        Skill.objects.create(name="Register")
        with pytest.raises(Exception):  # IntegrityError
            Skill.objects.create(name="Register")


@pytest.mark.django_db
class TestEmployeeModel:
    """Tests for Employee model."""
    
    def test_create_employee(self):
        """Test creating an employee."""
        employee = Employee.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="555-0100",
            hourly_rate=Decimal("15.50"),
            hire_date=date(2024, 1, 15),
            birth_date=date(2000, 5, 20),
        )
        assert employee.full_name == "John Doe"
        assert str(employee) == "John Doe"
        assert employee.is_active is True
    
    def test_employee_age_calculation(self):
        """Test employee age calculation."""
        employee = Employee.objects.create(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            phone_number="555-0101",
            hourly_rate=Decimal("16.00"),
            hire_date=date(2024, 1, 1),
            birth_date=date(2000, 1, 1),
        )
        age = employee.get_age()
        assert age >= 24  # Will be 24 or more depending on current date
    
    def test_employee_is_minor(self):
        """Test minor detection."""
        # Create a minor (born 10 years ago)
        minor = Employee.objects.create(
            first_name="Teen",
            last_name="Worker",
            email="teen@example.com",
            phone_number="555-0102",
            hourly_rate=Decimal("12.00"),
            hire_date=date(2024, 1, 1),
            birth_date=date(2014, 1, 1),
        )
        assert minor.is_minor() is True
        
        # Create an adult (born 25 years ago)
        adult = Employee.objects.create(
            first_name="Adult",
            last_name="Worker",
            email="adult@example.com",
            phone_number="555-0103",
            hourly_rate=Decimal("18.00"),
            hire_date=date(2024, 1, 1),
            birth_date=date(1999, 1, 1),
        )
        assert adult.is_minor() is False
    
    def test_employee_with_skills(self):
        """Test adding skills to employee."""
        skill1 = Skill.objects.create(name="Register")
        skill2 = Skill.objects.create(name="Stock")
        
        employee = Employee.objects.create(
            first_name="Multi",
            last_name="Skilled",
            email="multi@example.com",
            phone_number="555-0104",
            hourly_rate=Decimal("17.00"),
            hire_date=date(2024, 1, 1),
            birth_date=date(2000, 1, 1),
        )
        employee.skills.add(skill1, skill2)
        
        assert employee.skills.count() == 2
        assert skill1 in employee.skills.all()


@pytest.mark.django_db
class TestAvailabilityModel:
    """Tests for Availability model."""
    
    def test_create_availability(self):
        """Test creating availability."""
        employee = Employee.objects.create(
            first_name="Available",
            last_name="Worker",
            email="available@example.com",
            phone_number="555-0105",
            hourly_rate=Decimal("15.00"),
            hire_date=date(2024, 1, 1),
            birth_date=date(2000, 1, 1),
        )
        
        availability = Availability.objects.create(
            employee=employee,
            day_of_week=0,  # Monday
            start_time=time(9, 0),
            end_time=time(17, 0),
            is_available=True
        )
        
        assert availability.employee == employee
        assert availability.day_of_week == 0
        assert "Monday" in str(availability)
    
    def test_availability_unique_together(self):
        """Test that employee can't have duplicate availability for same day/time."""
        employee = Employee.objects.create(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            phone_number="555-0106",
            hourly_rate=Decimal("15.00"),
            hire_date=date(2024, 1, 1),
            birth_date=date(2000, 1, 1),
        )
        
        Availability.objects.create(
            employee=employee,
            day_of_week=0,
            start_time=time(9, 0),
            end_time=time(17, 0),
        )
        
        with pytest.raises(Exception):  # IntegrityError
            Availability.objects.create(
                employee=employee,
                day_of_week=0,
                start_time=time(9, 0),
                end_time=time(17, 0),
            )
