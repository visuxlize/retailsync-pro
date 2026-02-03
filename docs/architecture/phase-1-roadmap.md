# Phase 1 Development Roadmap

**Duration:** Weeks 1-2  
**Goal:** Build foundation - Manager can create a NY-compliant schedule manually  
**Success Metric:** Schedule creation in <30 minutes (vs 2 hours in Excel)

---

## Week 1: Backend Foundation

### Day 1: Project Setup
**What we're building:** Django project structure, database, basic models

**Tasks:**
- [x] Initialize Django project with `django-admin startproject`
- [x] Create apps: `employees`, `scheduling`, `stores`
- [x] Set up PostgreSQL database connection
- [x] Configure Django REST Framework
- [x] Set up pytest for testing
- [x] Create initial migrations

**Files created:**
```
backend/
├── config/settings/base.py
├── config/urls.py
├── apps/employees/models.py
├── apps/scheduling/models.py
├── apps/stores/models.py
└── requirements.txt
```

**What you'll learn:**
- How Django's modular app structure works
- Why we use PostgreSQL over SQLite
- What migrations do and why they matter

**Deliverable:** Running Django server with empty database

---

### Day 2: Employee Models & API
**What we're building:** Employee database models and CRUD API endpoints

**Tasks:**
- [ ] Create `Employee` model (name, email, hourly_rate, etc.)
- [ ] Create `Availability` model (employee preferences)
- [ ] Create `Skill` model (register, stock, manager, etc.)
- [ ] Build serializers for Employee data
- [ ] Create API endpoints: GET/POST/PUT/DELETE employees
- [ ] Write unit tests for Employee model

**Models we're creating:**
```python
# Employee Model
- id (auto-generated)
- first_name
- last_name
- email (unique)
- phone_number
- hourly_rate (Decimal)
- hire_date (Date)
- birth_date (Date)  # For minor restrictions
- store (ForeignKey to Store)
- skills (ManyToMany to Skill)
- is_active (Boolean)
- created_at / updated_at

# Availability Model
- employee (ForeignKey)
- day_of_week (0-6, Monday-Sunday)
- start_time
- end_time
- is_available (Boolean)

# Skill Model
- name (e.g., "Register", "Stock", "Manager")
- description
```

**API Endpoints:**
```
GET    /api/employees/          - List all employees
POST   /api/employees/          - Create new employee
GET    /api/employees/{id}/     - Get employee details
PUT    /api/employees/{id}/     - Update employee
DELETE /api/employees/{id}/     - Deactivate employee
GET    /api/employees/{id}/availability/ - Get availability
POST   /api/employees/{id}/availability/ - Set availability
```

**What you'll learn:**
- How Django models map to database tables
- Relationships: ForeignKey vs ManyToMany
- Serializers: Converting Python objects to JSON
- ViewSets: DRF's way of organizing API logic

**Deliverable:** Fully functional Employee API with tests

---

### Day 3: Store Models & Initial Data
**What we're building:** Store configuration and sample data

**Tasks:**
- [ ] Create `Store` model
- [ ] Create `Department` model (optional)
- [ ] Build store API endpoints
- [ ] Create data seeding script (sample employees)
- [ ] Set up Django admin for easy data viewing

**Store Model:**
```python
- id
- name (e.g., "Store #1247")
- address
- city, state, zip_code
- phone_number
- labor_budget (Decimal)  # Weekly budget
- timezone (e.g., "America/New_York")
- settings (JSONField)  # Store-specific configs
- created_at / updated_at
```

**Sample Data Script:**
```bash
python manage.py seed_data
```
Creates:
- 1 sample store
- 15 sample employees with varying skills and availability
- 5 skills (Register, Stock, Manager, Cashier, Floor)

**What you'll learn:**
- Django admin interface (super useful for debugging)
- Management commands (custom scripts)
- JSON fields for flexible data storage

**Deliverable:** Store API + ability to quickly generate test data

---

### Day 4-5: Scheduling Models
**What we're building:** Core scheduling system without AI yet

**Tasks:**
- [ ] Create `Schedule` model (weekly schedule container)
- [ ] Create `Shift` model (individual shift)
- [ ] Build shift CRUD API
- [ ] Implement shift assignment logic
- [ ] Add budget calculation (sum of all shift costs)
- [ ] Write comprehensive unit tests

**Models:**
```python
# Schedule Model
- id
- store (ForeignKey)
- week_start (Date)  # Monday of the week
- week_end (Date)    # Sunday of the week
- published (Boolean)
- published_at (DateTime)
- created_by (ForeignKey to User)
- total_hours (calculated)
- total_cost (calculated)
- status (DRAFT, PUBLISHED, ARCHIVED)

# Shift Model
- id
- schedule (ForeignKey)
- employee (ForeignKey)
- date (Date)
- start_time (Time)
- end_time (Time)
- duration (Decimal, calculated)
- meal_break_start (Time, nullable)
- meal_break_end (Time, nullable)
- position (e.g., "Register")
- notes (Text, optional)
```

**API Endpoints:**
```
GET    /api/schedules/                    - List schedules
POST   /api/schedules/                    - Create new schedule
GET    /api/schedules/{id}/               - Get schedule details
GET    /api/schedules/{id}/shifts/        - Get all shifts for schedule
POST   /api/schedules/{id}/shifts/        - Add shift to schedule
PUT    /api/schedules/{id}/shifts/{id}/   - Update shift
DELETE /api/schedules/{id}/shifts/{id}/   - Remove shift
POST   /api/schedules/{id}/publish/       - Publish schedule
```

**What you'll learn:**
- Calculated fields in models (duration = end_time - start_time)
- Aggregation queries (sum of all shift costs)
- Model properties vs database fields
- Custom model methods

**Deliverable:** Working schedule API where manager can manually create shifts

---

### Day 6-7: NY Compliance Engine
**What we're building:** THE MOST CRITICAL PART - Automated labor law validation

**Tasks:**
- [ ] Implement meal break validation
- [ ] Implement overtime calculation
- [ ] Implement spread of hours check
- [ ] Implement day of rest validation
- [ ] Implement minor restrictions
- [ ] Implement predictive scheduling check
- [ ] Create compliance violation model
- [ ] Build compliance report API
- [ ] Write extensive unit tests for EVERY rule

**Compliance Validation Flow:**
```python
def validate_schedule(schedule):
    violations = []
    
    for shift in schedule.shifts.all():
        # Check each compliance rule
        violations.extend(check_meal_breaks(shift))
        violations.extend(check_spread_of_hours(shift))
        violations.extend(check_minor_restrictions(shift))
    
    # Check week-level rules
    for employee in schedule.employees:
        violations.extend(check_overtime(employee, schedule))
        violations.extend(check_day_of_rest(employee, schedule))
    
    violations.extend(check_predictive_scheduling(schedule))
    
    return violations
```

**ComplianceViolation Model:**
```python
- id
- shift or schedule (GenericForeignKey)
- violation_type (MEAL_BREAK, OVERTIME, etc.)
- severity (WARNING, ERROR, CRITICAL)
- message (Human-readable description)
- suggested_fix (What to do)
- penalty_amount (Decimal, if applicable)
- created_at
```

**API Endpoint:**
```
GET /api/schedules/{id}/compliance/
```
Returns:
```json
{
  "is_compliant": false,
  "total_violations": 3,
  "violations": [
    {
      "type": "MISSING_MEAL_BREAK",
      "severity": "CRITICAL",
      "shift_id": 123,
      "employee": "John Martinez",
      "message": "Shift is 8 hours but has no meal break",
      "suggested_fix": "Add 30-minute break between 12pm-2pm",
      "penalty": 1000.00
    }
  ]
}
```

**Testing is CRITICAL here:**
```python
# Test cases we MUST have
def test_shift_over_6_hours_requires_meal_break()
def test_employee_over_40_hours_triggers_overtime()
def test_spread_over_10_hours_triggers_penalty()
def test_employee_working_7_days_violates_day_of_rest()
def test_minor_cannot_work_past_10pm_on_school_night()
def test_schedule_published_late_triggers_premium_pay()

# Edge cases
def test_exactly_6_hour_shift_no_meal_break_required()
def test_exactly_40_hours_no_overtime()
def test_meal_break_at_shift_start_invalid()
```

**What you'll learn:**
- How to encode complex business rules in code
- Importance of comprehensive testing
- Generic foreign keys for flexible relationships
- Decimal vs Float for money (always use Decimal!)

**Deliverable:** Compliance engine that catches ALL 6 NY labor law violations

---

## Week 2: Frontend Dashboard

### Day 8-9: React Project Setup & Employee Pages
**What we're building:** React app with employee management UI

**Tasks:**
- [ ] Initialize React app with Create React App
- [ ] Set up Material-UI
- [ ] Configure Axios for API calls
- [ ] Create routing (React Router)
- [ ] Build Employee List page
- [ ] Build Employee Form (Add/Edit)
- [ ] Connect to backend API

**Components to create:**
```
src/
├── pages/
│   ├── Dashboard.jsx
│   ├── EmployeesPage.jsx
│   └── SchedulePage.jsx
├── components/
│   ├── employees/
│   │   ├── EmployeeList.jsx
│   │   ├── EmployeeCard.jsx
│   │   └── EmployeeForm.jsx
│   └── common/
│       ├── Navigation.jsx
│       └── LoadingSpinner.jsx
├── services/
│   ├── api.js
│   └── employeeService.js
└── App.jsx
```

**What you'll learn:**
- React component structure
- State management with hooks (useState, useEffect)
- API integration with async/await
- Form handling
- Material-UI components

**Deliverable:** Working employee management interface

---

### Day 10-11: Schedule Calendar UI
**What we're building:** The heart of the UI - Calendar for creating shifts

**Tasks:**
- [ ] Install FullCalendar library
- [ ] Create ScheduleCalendar component
- [ ] Build ShiftModal for creating/editing shifts
- [ ] Implement drag-and-drop shift assignment
- [ ] Connect to schedule API
- [ ] Display employee availability overlays

**Key Component: ScheduleCalendar.jsx**
```jsx
import FullCalendar from '@fullcalendar/react'
import timeGridPlugin from '@fullcalendar/timegrid'

const ScheduleCalendar = () => {
  const [shifts, setShifts] = useState([])
  const [employees, setEmployees] = useState([])
  
  // Fetch shifts from API
  useEffect(() => {
    fetchShifts()
  }, [])
  
  const handleDateClick = (info) => {
    // Open modal to create shift at clicked time
    openShiftModal(info.date)
  }
  
  const handleShiftDrop = (info) => {
    // Update shift time when dragged
    updateShift(info.event.id, {
      start_time: info.event.start,
      end_time: info.event.end
    })
  }
  
  return (
    <FullCalendar
      plugins={[timeGridPlugin]}
      initialView="timeGridWeek"
      events={shifts}
      dateClick={handleDateClick}
      eventDrop={handleShiftDrop}
      editable={true}
    />
  )
}
```

**What you'll learn:**
- Third-party library integration
- Complex UI state management
- Event handling in React
- Optimistic UI updates

**Deliverable:** Interactive calendar where manager can create/edit shifts

---

### Day 12: Compliance Widget & Budget Display
**What we're building:** Real-time compliance and budget feedback

**Tasks:**
- [ ] Create ComplianceWidget component
- [ ] Create BudgetWidget component
- [ ] Implement live validation as shifts are added
- [ ] Show warnings/errors in UI
- [ ] Add "Fix" buttons for auto-corrections

**ComplianceWidget.jsx:**
```jsx
const ComplianceWidget = ({ scheduleId }) => {
  const [compliance, setCompliance] = useState(null)
  
  useEffect(() => {
    // Call compliance API whenever schedule changes
    checkCompliance(scheduleId).then(setCompliance)
  }, [scheduleId])
  
  if (!compliance) return <LoadingSpinner />
  
  return (
    <Card>
      <CardHeader>
        Compliance Status
        {compliance.is_compliant ? (
          <CheckCircle color="success" />
        ) : (
          <Error color="error" />
        )}
      </CardHeader>
      <CardContent>
        {compliance.violations.map(v => (
          <Alert severity={v.severity} key={v.id}>
            {v.message}
            <Button onClick={() => autoFix(v)}>Fix</Button>
          </Alert>
        ))}
      </CardContent>
    </Card>
  )
}
```

**What you'll learn:**
- Real-time data fetching
- Conditional rendering
- Error/warning UI patterns
- User feedback and actionable alerts

**Deliverable:** Live compliance feedback as manager builds schedule

---

### Day 13: Polish & Testing
**What we're building:** Production-ready Phase 1

**Tasks:**
- [ ] Add loading states everywhere
- [ ] Add error handling (what if API fails?)
- [ ] Implement form validation
- [ ] Add confirmation dialogs ("Are you sure you want to delete?")
- [ ] Write frontend tests (React Testing Library)
- [ ] Fix any bugs found
- [ ] Test entire flow: Create employees → Create schedule → Validate compliance → Publish

**Testing Checklist:**
```
✅ Can create employee with all fields
✅ Employee form shows validation errors
✅ Can edit existing employee
✅ Employee list loads correctly
✅ Can create new schedule
✅ Can add shift to schedule
✅ Can drag shift to different time
✅ Can delete shift
✅ Compliance violations show immediately
✅ Budget updates in real-time
✅ Can publish schedule
✅ All API errors are handled gracefully
```

**Deliverable:** Polished, bug-free Phase 1 MVP

---

### Day 14: Deployment & Documentation
**What we're building:** Live application on Heroku

**Tasks:**
- [ ] Set up Heroku account
- [ ] Configure Django for production
- [ ] Set up PostgreSQL on Heroku
- [ ] Deploy backend
- [ ] Deploy frontend (Netlify or Vercel)
- [ ] Test production deployment
- [ ] Write deployment documentation
- [ ] Record demo video

**What you'll learn:**
- Environment variables and secrets management
- Production vs development settings
- Database migrations in production
- Static file serving
- CORS configuration

**Deliverable:** Live URL where anyone can test RetailSync Pro Phase 1

---

## Phase 1 Definition of Done

### Backend ✅
- [x] Employee CRUD API working
- [x] Schedule CRUD API working
- [x] All 6 NY labor law rules enforced
- [x] 100% test coverage on compliance engine
- [x] API documentation complete

### Frontend ✅
- [x] Manager can create employees
- [x] Manager can create weekly schedule
- [x] Calendar shows all shifts clearly
- [x] Compliance violations display in real-time
- [x] Budget tracking shows total cost
- [x] Can publish schedule

### Quality ✅
- [x] All tests passing (backend + frontend)
- [x] No known bugs
- [x] Code reviewed
- [x] Documentation complete

### Deployment ✅
- [x] Application live on public URL
- [x] Database backed up
- [x] Environment variables secured

---

## Success Metrics

After Phase 1, we should be able to measure:
- **Time to create schedule:** <30 minutes (down from 2+ hours)
- **Compliance violations:** 0% (down from 20-30% in Excel)
- **Manager satisfaction:** "This is way better than Excel"

---

## Next Up: Phase 2

Once Phase 1 is solid, we'll add:
- Omni Analytics integration
- AI-powered schedule generation
- Budget forecasting
- Automated optimization

But first, let's master the foundation!
