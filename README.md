# 🚀 RetailSync Pro

> **An open-source retail workforce management platform that saves managers 6-8 hours weekly through AI-powered scheduling and automated compliance.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Django 5.0+](https://img.shields.io/badge/django-5.0+-green.svg)](https://www.djangoproject.com/)
[![React 18+](https://img.shields.io/badge/react-18+-61dafb.svg)](https://reactjs.org/)

---

## 📖 Table of Contents

- [The Problem We're Solving](#the-problem-were-solving)
- [Our Solution](#our-solution)
- [Current Phase](#current-phase)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Development Roadmap](#development-roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 The Problem We're Solving

Retail store managers currently spend **6-8 hours every week** creating employee schedules in Excel. They struggle with:

- ❌ **Manual scheduling chaos** - Juggling 15+ employee availability requests via text/paper
- ❌ **Labor law violations** - Missing NY meal breaks, overtime rules, spread of hours penalties
- ❌ **Budget overruns** - No real-time visibility into labor costs vs budget
- ❌ **Employee dissatisfaction** - Unfair schedules that ignore preferences and availability

**Result:** Frustrated managers, compliance risks, and wasted time on administrative tasks instead of actually managing the store.

---

## ✨ Our Solution

RetailSync Pro transforms scheduling from a manual nightmare into an automated, intelligent system:

### Core Features

#### 🤖 **AI-Powered Schedule Generation**
- Automatically generates optimal schedules based on sales forecasts from Omni Analytics
- Considers employee preferences, skills, and availability
- Generates schedules in seconds vs hours

#### ⚖️ **100% NY Labor Law Compliance**
- Automatic enforcement of all NY labor regulations:
  - Meal breaks for shifts >6 hours
  - Overtime calculations (>40 hours/week)
  - Spread of hours pay
  - Day of rest requirements
  - Minor employee restrictions
  - Predictive scheduling (Fair Workweek Law)
- Real-time compliance warnings with auto-fix suggestions

#### 💰 **Real-Time Budget Tracking**
- Live labor cost calculations
- Budget variance alerts
- Overtime cost forecasting

#### 📱 **Employee Mobile App**
- View schedules instantly
- Request time off
- Swap shifts with coworkers
- Push notifications for schedule changes

#### 📊 **Business Intelligence Integration**
- Connects to Omni Analytics for sales forecasting
- Aligns staffing with actual business needs
- Historical performance tracking

---

## 🚦 Current Phase

### **Phase 1: Foundation & Compliance** (Weeks 1-2) - 🟢 IN PROGRESS

**Goal:** Build the foundation and eliminate labor law violations.

**What We're Building:**
- ✅ Django backend with PostgreSQL database
- ✅ Employee management system
- ✅ Manual schedule creation interface
- ✅ NY labor law compliance engine
- ✅ React dashboard with calendar UI

**Success Metric:** Manager can create a compliant schedule in <30 minutes (vs 2 hours in Excel)

---

## 🛠 Tech Stack

### Backend
- **Django 5.0+** - Web framework (chosen for admin panel, ORM, Python ecosystem)
- **Django REST Framework** - API layer
- **PostgreSQL 16** - Primary database
- **TimescaleDB** - Time-series extension for sales data (Phase 2+)
- **Celery** - Background task processing (Phase 2+)
- **Redis** - Cache and message broker (Phase 2+)

### Frontend
- **React 18** - Web dashboard
- **React Native** - Mobile apps (Phase 3+)
- **Material-UI** - Component library
- **FullCalendar** - Schedule visualization
- **Axios** - API client

### AI/ML (Phase 2+)
- **scikit-learn** - Sales forecasting models
- **pandas** - Data processing
- **NumPy** - Numerical computing

### DevOps
- **Docker** - Containerization
- **GitHub Actions** - CI/CD
- **Heroku** - Hosting (Phase 1), migrate to AWS (Phase 4)

---

## 📁 Project Structure

```
retailsync-pro/
├── backend/                    # Django application
│   ├── config/                # Django settings
│   ├── apps/
│   │   ├── employees/         # Employee management
│   │   ├── scheduling/        # Schedule creation & compliance
│   │   ├── stores/            # Store management
│   │   └── analytics/         # Omni Analytics integration (Phase 2)
│   ├── requirements.txt       # Python dependencies
│   └── manage.py
│
├── frontend/                  # React web dashboard
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── pages/             # Page-level components
│   │   ├── services/          # API integration
│   │   └── utils/             # Helper functions
│   ├── package.json
│   └── README.md
│
├── mobile/                    # React Native apps (Phase 3)
│   ├── ios/
│   ├── android/
│   └── src/
│
├── docs/                      # Documentation
│   ├── architecture/          # System design docs
│   ├── api/                   # API documentation
│   ├── compliance/            # NY labor law references
│   └── deployment/            # Deployment guides
│
├── scripts/                   # Utility scripts
│   ├── setup.sh               # Initial setup
│   ├── deploy.sh              # Deployment automation
│   └── seed-data.py           # Sample data generation
│
├── .github/                   # GitHub configuration
│   ├── workflows/             # CI/CD pipelines
│   └── ISSUE_TEMPLATE/        # Issue templates
│
├── docker-compose.yml         # Local development environment
├── .env.example               # Environment variables template
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **PostgreSQL 16** - [Download](https://www.postgresql.org/download/)
- **Git** - [Download](https://git-scm.com/downloads)

### Quick Start (Local Development)

#### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/retailsync-pro.git
cd retailsync-pro
```

#### 2. Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Set up database
createdb retailsync_dev
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

Backend will be running at `http://localhost:8000`

#### 3. Frontend Setup
```bash
# In a new terminal
cd frontend
npm install

# Start development server
npm start
```

Frontend will be running at `http://localhost:3000`

### Using Docker (Recommended)

```bash
# Start all services
docker-compose up

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser
```

Access the application:
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000/api/`
- Django Admin: `http://localhost:8000/admin/`

---

## 🗺 Development Roadmap

### ✅ Phase 1: Foundation & Compliance (Weeks 1-2)
- Basic schedule creation
- Employee management
- NY labor law compliance engine
- React dashboard

### 🔄 Phase 2: Intelligence Layer (Weeks 3-4)
- Omni Analytics integration
- AI-powered sales forecasting
- Automatic schedule generation
- Real-time budget tracking

### 📱 Phase 3: Mobile Apps (Weeks 5-8)
- Employee mobile app (React Native)
- Manager mobile app
- Push notifications
- Shift swapping

### 🚀 Phase 4: Advanced Features (Weeks 9-12)
- Advanced AI predictions
- Multi-store management
- Analytics dashboard
- Payroll integrations

---

## 📚 Documentation

Detailed documentation is available in the `/docs` folder:

- [Architecture Overview](docs/architecture/system-design.md)
- [API Reference](docs/api/README.md)
- [NY Labor Law Compliance Guide](docs/compliance/ny-labor-laws.md)
- [Deployment Guide](docs/deployment/heroku.md)

---

## 🤝 Contributing

This is a learning project, but contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) before submitting pull requests.

### Development Workflow

1. Create a feature branch: `git checkout -b feature/amazing-feature`
2. Make your changes
3. Run tests: `pytest` (backend), `npm test` (frontend)
4. Commit: `git commit -m 'Add amazing feature'`
5. Push: `git push origin feature/amazing-feature`
6. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built as a passion project to solve real retail scheduling problems
- Inspired by the need to save managers' time and prevent labor law violations
- Learning journey documented at each phase

---

## 📬 Contact

**Project Maintainer:** [Andres Marte]

- GitHub: [@Visuxlize](https://github.com/Visuxlize)
- Email: mAndres1994@gmail.com

---

**⭐ Star this repo if you find it helpful! ⭐**
