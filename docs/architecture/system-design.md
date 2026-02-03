# RetailSync Pro - System Architecture

## Overview

RetailSync Pro is a full-stack retail workforce management platform designed to automate scheduling, ensure labor law compliance, and optimize labor costs through AI-powered predictions.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACES                          │
├────────────────────┬────────────────────┬───────────────────────┤
│   Web Dashboard    │   Manager Mobile   │   Employee Mobile    │
│   (React)          │   (React Native)   │   (React Native)     │
└────────────────────┴────────────────────┴───────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                        API GATEWAY                               │
│                    (Django REST Framework)                       │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ↓                     ↓                     ↓
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Business   │    │  Background  │    │  Real-time   │
│    Logic     │    │    Tasks     │    │   Updates    │
│   (Django)   │    │   (Celery)   │    │  (Channels)  │
└──────────────┘    └──────────────┘    └──────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                        DATA LAYER                                │
├────────────────────┬────────────────────┬───────────────────────┤
│   PostgreSQL +     │      Redis         │   External APIs      │
│   TimescaleDB      │   (Cache/Queue)    │ (Omni Analytics)     │
└────────────────────┴────────────────────┴───────────────────────┘
```

## Complete Project Structure

This shows how all pieces fit together across the full codebase.

```
retailsync-pro/
│
├── backend/                              # Django Backend Application
│   ├── config/                           # Project settings
│   │   ├── settings/
│   │   │   ├── base.py                  # Shared settings
│   │   │   ├── development.py           # Dev-specific settings
│   │   │   ├── production.py            # Prod settings
│   │   │   └── test.py                  # Test settings
│   │   ├── urls.py                      # URL routing
│   │   ├── wsgi.py                      # WSGI config
│   │   └── asgi.py                      # ASGI config (for Channels)
│   │
│   ├── apps/                            # Django apps (modular features)
│   │   ├── employees/                   # Employee management
│   │   │   ├── models.py               # Employee, Availability, Skills
│   │   │   ├── serializers.py          # DRF serializers
│   │   │   ├── views.py                # API endpoints
│   │   │   ├── urls.py                 # App routing
│   │   │   ├── admin.py                # Django admin config
│   │   │   └── tests/                  # Unit tests
│   │   │
│   │   ├── scheduling/                  # Schedule & shift management
│   │   │   ├── models.py               # Schedule, Shift models
│   │   │   ├── compliance.py           # NY labor law engine
│   │   │   ├── generators.py           # AI schedule generation
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   └── tests/
│   │   │       ├── test_compliance.py  # Critical compliance tests
│   │   │       └── test_generators.py
│   │   │
│   │   ├── stores/                      # Store management
│   │   │   ├── models.py               # Store, Department
│   │   │   └── ...
│   │   │
│   │   ├── analytics/                   # Omni Analytics integration
│   │   │   ├── models.py               # SalesData, Forecast
│   │   │   ├── omni_client.py          # API client
│   │   │   ├── forecasting.py          # ML models
│   │   │   └── ...
│   │   │
│   │   └── notifications/               # Push notifications
│   │       ├── models.py
│   │       ├── firebase_client.py
│   │       └── ...
│   │
│   ├── requirements.txt                 # Python dependencies
│   ├── requirements-dev.txt             # Dev dependencies (pytest, etc.)
│   ├── manage.py                        # Django management script
│   ├── pytest.ini                       # Pytest configuration
│   └── Dockerfile                       # Backend Docker image
│
├── frontend/                            # React Web Dashboard
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/                  # Reusable UI components
│   │   │   ├── common/
│   │   │   │   ├── Button.jsx
│   │   │   │   ├── Card.jsx
│   │   │   │   └── Modal.jsx
│   │   │   ├── schedule/
│   │   │   │   ├── ScheduleCalendar.jsx  # Main calendar view
│   │   │   │   ├── ShiftCard.jsx         # Individual shift display
│   │   │   │   └── ComplianceWidget.jsx  # Compliance status
│   │   │   └── employees/
│   │   │       ├── EmployeeList.jsx
│   │   │       └── EmployeeForm.jsx
│   │   │
│   │   ├── pages/                       # Full page components
│   │   │   ├── Dashboard.jsx            # Manager home screen
│   │   │   ├── SchedulePage.jsx         # Schedule creation
│   │   │   ├── EmployeesPage.jsx
│   │   │   └── BudgetPage.jsx
│   │   │
│   │   ├── services/                    # API integration
│   │   │   ├── api.js                   # Axios base config
│   │   │   ├── scheduleService.js       # Schedule API calls
│   │   │   ├── employeeService.js
│   │   │   └── authService.js
│   │   │
│   │   ├── hooks/                       # Custom React hooks
│   │   │   ├── useSchedule.js
│   │   │   ├── useEmployees.js
│   │   │   └── useWebSocket.js
│   │   │
│   │   ├── utils/                       # Helper functions
│   │   │   ├── dateUtils.js
│   │   │   ├── validation.js
│   │   │   └── formatters.js
│   │   │
│   │   ├── App.jsx                      # Root component
│   │   └── index.jsx                    # Entry point
│   │
│   ├── package.json                     # Node dependencies
│   ├── .eslintrc.js                     # Linting config
│   └── Dockerfile                       # Frontend Docker image
│
├── mobile/                              # React Native Mobile Apps
│   ├── src/
│   │   ├── screens/                     # App screens
│   │   │   ├── employee/
│   │   │   │   ├── ScheduleScreen.jsx
│   │   │   │   ├── TimeOffScreen.jsx
│   │   │   │   └── ShiftSwapScreen.jsx
│   │   │   └── manager/
│   │   │       ├── DashboardScreen.jsx
│   │   │       └── ApprovalsScreen.jsx
│   │   │
│   │   ├── components/
│   │   ├── services/
│   │   └── navigation/
│   │
│   ├── app.json                         # Expo configuration
│   └── package.json
│
├── docs/                                # Documentation
│   ├── architecture/
│   │   ├── system-design.md            # This file
│   │   ├── database-schema.md
│   │   └── api-design.md
│   ├── api/
│   │   └── README.md                    # API documentation
│   ├── compliance/
│   │   └── ny-labor-laws.md            # Legal requirements
│   └── deployment/
│       ├── local-setup.md
│       ├── heroku.md
│       └── aws.md
│
├── scripts/                             # Utility scripts
│   ├── setup.sh                         # Initial project setup
│   ├── deploy.sh                        # Deployment automation
│   └── seed-data.py                     # Sample data for testing
│
├── .github/                             # GitHub configuration
│   ├── workflows/
│   │   ├── backend-ci.yml               # Backend CI/CD
│   │   └── frontend-ci.yml              # Frontend CI/CD
│   └── ISSUE_TEMPLATE/
│
├── docker-compose.yml                   # Local dev environment
├── .env.example                         # Environment template
├── .gitignore
├── LICENSE
└── README.md
```

## Phase-by-Phase Build Plan

### Phase 1 Focus (Weeks 1-2)
Build only these parts first:
```
backend/
  ├── apps/employees/      # Employee CRUD
  ├── apps/scheduling/     # Manual scheduling + compliance
  └── apps/stores/         # Basic store model

frontend/
  ├── pages/Dashboard      # Manager home
  ├── pages/SchedulePage   # Calendar interface
  └── components/schedule/ # Shift creation UI
```

### Phase 2 Additions (Weeks 3-4)
```
backend/
  └── apps/analytics/      # Omni integration + AI

frontend/
  └── pages/BudgetPage     # Budget tracking
```

### Phase 3 Additions (Weeks 5-8)
```
mobile/                    # Entire mobile app
backend/
  └── apps/notifications/  # Push notifications
```

### Phase 4 Additions (Weeks 9-12)
```
backend/
  ├── apps/integrations/   # Payroll, POS
  └── apps/reporting/      # Analytics dashboard
```

---

**Why This Structure Matters:**

Every folder has a clear purpose. When you need to add a feature, you'll know exactly where it goes. Employee-related code? `apps/employees/`. Schedule logic? `apps/scheduling/`. This modularity makes the codebase scalable and maintainable as we grow from Phase 1 to Phase 4.
