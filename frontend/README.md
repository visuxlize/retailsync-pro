# RetailSync Pro - Frontend

React web dashboard for retail managers.

## Phase 1 Development Status

- [ ] Project initialized (Create React App)
- [ ] Employee management pages
- [ ] Schedule calendar (FullCalendar)
- [ ] Compliance widget
- [ ] Budget tracking widget
- [ ] Deployed to Netlify/Vercel

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm start
```

Visit http://localhost:3000

## Project Structure

```
frontend/
├── public/
├── src/
│   ├── components/         # Reusable UI components
│   │   ├── employees/     # Employee-related components
│   │   ├── schedule/      # Schedule/shift components
│   │   └── common/        # Shared components
│   ├── pages/             # Full page components
│   │   ├── Dashboard.jsx
│   │   ├── EmployeesPage.jsx
│   │   └── SchedulePage.jsx
│   ├── services/          # API integration
│   │   ├── api.js        # Axios config
│   │   └── employeeService.js
│   ├── App.jsx
│   └── index.jsx
├── package.json
└── README.md
```

## Available Scripts

```bash
# Development server
npm start

# Run tests
npm test

# Build for production
npm run build

# Lint code
npm run lint
```

## Key Libraries

- **React 18** - UI framework
- **Material-UI** - Component library
- **FullCalendar** - Schedule visualization
- **Axios** - API client
- **React Router** - Navigation
- **React Query** - Data fetching (Phase 2+)

## Environment Variables

Create `.env.local`:

```
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_ENVIRONMENT=development
```

## Component Examples

### Employee List
```jsx
import { EmployeeList } from './components/employees/EmployeeList';

<EmployeeList onEmployeeClick={handleClick} />
```

### Schedule Calendar
```jsx
import { ScheduleCalendar } from './components/schedule/ScheduleCalendar';

<ScheduleCalendar 
  scheduleId={scheduleId}
  onShiftCreate={handleShiftCreate}
/>
```

## Phase 1 Goals

Build the manager's primary interface:
1. Employee management (CRUD)
2. Interactive schedule calendar
3. Real-time compliance feedback
4. Budget tracking display

See [Phase 1 Roadmap](../docs/architecture/phase-1-roadmap.md) for details.
