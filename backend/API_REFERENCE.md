# Employee Management API Reference

## Quick Start

Start the development server:
```bash
cd backend
venv\Scripts\activate  # Windows
python manage.py runserver
```

Visit:
- **API Root**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/
- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/

## API Endpoints

### Skills

#### List Skills
```http
GET /api/skills/
```

Response:
```json
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "name": "Register",
      "description": "Cash register operations",
      "created_at": "2024-02-03T05:00:00Z",
      "updated_at": "2024-02-03T05:00:00Z"
    }
  ]
}
```

#### Create Skill
```http
POST /api/skills/
Content-Type: application/json

{
  "name": "Stock",
  "description": "Stocking shelves and inventory"
}
```

### Employees

#### List Employees
```http
GET /api/employees/
```

Optional query parameters:
- `?search=john` - Search by name or email
- `?is_active=true` - Filter by active status
- `?skills=1` - Filter by skill ID
- `?ordering=-hire_date` - Order by field (- for descending)

Response:
```json
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "first_name": "John",
      "last_name": "Doe",
      "full_name": "John Doe",
      "email": "john.doe@example.com",
      "hourly_rate": "15.50",
      "skills": [
        {
          "id": 1,
          "name": "Register",
          "description": "Cash register operations"
        }
      ],
      "is_active": true
    }
  ]
}
```

#### Create Employee
```http
POST /api/employees/
Content-Type: application/json

{
  "first_name": "Jane",
  "last_name": "Smith",
  "email": "jane.smith@example.com",
  "phone_number": "555-0101",
  "hourly_rate": "16.00",
  "hire_date": "2024-02-01",
  "birth_date": "1998-03-15",
  "skill_ids": [1, 2]
}
```

Response (201 Created):
```json
{
  "id": 2,
  "first_name": "Jane",
  "last_name": "Smith",
  "full_name": "Jane Smith",
  "email": "jane.smith@example.com",
  "phone_number": "555-0101",
  "hourly_rate": "16.00",
  "hire_date": "2024-02-01",
  "birth_date": "1998-03-15",
  "age": 26,
  "is_minor": false,
  "skills": [
    {"id": 1, "name": "Register", "description": "Cash register operations"}
  ],
  "availability": [],
  "is_active": true,
  "created_at": "2024-02-03T05:30:00Z",
  "updated_at": "2024-02-03T05:30:00Z"
}
```

#### Get Employee Details
```http
GET /api/employees/1/
```

Returns full employee details including skills and availability.

#### Update Employee
```http
PUT /api/employees/1/
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.updated@example.com",
  "phone_number": "555-0100",
  "hourly_rate": "17.50",
  "hire_date": "2024-01-15",
  "birth_date": "2000-05-20",
  "skill_ids": [1, 2, 3]
}
```

Or partial update:
```http
PATCH /api/employees/1/
Content-Type: application/json

{
  "hourly_rate": "18.00"
}
```

#### Delete Employee (Soft Delete)
```http
DELETE /api/employees/1/
```

Response (200 OK):
```json
{
  "detail": "Employee deactivated successfully."
}
```

**Note**: Employee is not deleted, just marked as `is_active: false`

### Employee Availability

#### Get Employee Availability
```http
GET /api/employees/1/availability/
```

Response:
```json
[
  {
    "id": 1,
    "employee": 1,
    "day_of_week": 0,
    "day_of_week_display": "Monday",
    "start_time": "09:00:00",
    "end_time": "17:00:00",
    "is_available": true,
    "created_at": "2024-02-03T05:00:00Z",
    "updated_at": "2024-02-03T05:00:00Z"
  }
]
```

#### Add Availability (Single)
```http
POST /api/employees/1/availability/
Content-Type: application/json

{
  "day_of_week": 1,
  "start_time": "10:00:00",
  "end_time": "18:00:00",
  "is_available": true
}
```

#### Add Multiple Availabilities
```http
POST /api/employees/1/availability/
Content-Type: application/json

[
  {
    "day_of_week": 0,
    "start_time": "09:00:00",
    "end_time": "17:00:00"
  },
  {
    "day_of_week": 1,
    "start_time": "09:00:00",
    "end_time": "17:00:00"
  }
]
```

## Models

### Employee
- `first_name` - String (required)
- `last_name` - String (required)
- `email` - Email, unique (required)
- `phone_number` - String (required)
- `hourly_rate` - Decimal, min 0.01 (required)
- `hire_date` - Date (required)
- `birth_date` - Date (required, for minor restrictions)
- `skills` - Many-to-many relationship with Skill
- `is_active` - Boolean (default: true)

Computed properties:
- `full_name` - First + Last name
- `age` - Calculated from birth_date
- `is_minor` - True if under 18

### Skill
- `name` - String, unique (required)
- `description` - Text (optional)

### Availability
- `employee` - Foreign key to Employee
- `day_of_week` - Integer 0-6 (0=Monday, 6=Sunday)
- `start_time` - Time
- `end_time` - Time (must be after start_time)
- `is_available` - Boolean (default: true)

Unique constraint: employee + day_of_week + start_time

## Testing

Run all tests:
```bash
pytest
```

With coverage report:
```bash
pytest --cov=apps --cov-report=html
```

Run specific test file:
```bash
pytest apps/employees/tests/test_api.py -v
```

## Django Admin

Create a superuser to access Django admin:
```bash
python manage.py createsuperuser
```

Then visit http://localhost:8000/admin/

## Database Schema

Tables created:
- `employees_employee` - Employee records
- `employees_skill` - Skills
- `employees_availability` - Availability schedules
- `employees_employee_skills` - Many-to-many relationship table

## Next Steps

- [ ] Add Store model (employee belongs to store)
- [ ] Build Scheduling API
- [ ] Implement NY labor law compliance engine
- [ ] Add authentication
- [ ] Deploy to production
