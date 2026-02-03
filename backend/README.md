# RetailSync Pro - Backend

Django REST API for retail workforce management.

## Phase 1 Development Status

- [x] Project initialized
- [x] Employee management API (COMPLETED)
- [ ] Scheduling API
- [ ] NY labor law compliance engine
- [x] Unit tests (97% coverage)
- [ ] Deployed to Heroku

### Employee Management API - COMPLETED ✅

**What's Built:**
- ✅ Employee CRUD (Create, Read, Update, Delete)
- ✅ Skill management (Register, Stock, Manager, etc.)
- ✅ Employee availability tracking (by day/time)
- ✅ Soft delete (deactivate instead of delete)
- ✅ Age calculation & minor detection (for labor law compliance)
- ✅ Search & filter functionality
- ✅ Comprehensive test suite (28 tests, 97% coverage)
- ✅ Django admin interface
- ✅ API documentation (Swagger/ReDoc)

**API Endpoints:**
- `GET/POST /api/employees/` - List/Create employees
- `GET/PUT/PATCH/DELETE /api/employees/{id}/` - Retrieve/Update/Delete employee
- `GET/POST /api/employees/{id}/availability/` - Get/Set availability
- `GET/POST /api/skills/` - List/Create skills
- `GET/POST /api/availability/` - Bulk availability operations

## Quick Start

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database
createdb retailsync_dev
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

Visit http://localhost:8000/admin

## Project Structure

```
backend/
├── config/              # Django project settings
├── apps/
│   ├── employees/      # Employee management
│   ├── scheduling/     # Schedule & shift logic
│   └── stores/         # Store configuration
├── requirements.txt
└── manage.py
```

## Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=apps --cov-report=html

# Specific app
pytest apps/scheduling/tests/
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/

## Environment Variables

Copy `.env.example` to `.env` and update:

```bash
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@localhost/retailsync_dev
```

## Common Commands

```bash
# Create new Django app
python manage.py startapp app_name

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Shell (for debugging)
python manage.py shell

# Seed sample data
python manage.py seed_data
```

## Phase 1 Goals

Build the foundation for automated scheduling:
1. Employee CRUD operations
2. Schedule & shift management
3. NY labor law compliance validation
4. Budget tracking

See [Phase 1 Roadmap](../docs/architecture/phase-1-roadmap.md) for details.
