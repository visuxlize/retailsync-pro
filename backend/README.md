# RetailSync Pro - Backend

Django REST API for retail workforce management.

## Phase 1 Development Status

- [ ] Project initialized
- [ ] Employee management API
- [ ] Scheduling API
- [ ] NY labor law compliance engine
- [ ] Unit tests (>80% coverage)
- [ ] Deployed to Heroku

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
