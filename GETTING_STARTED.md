# Getting Started with RetailSync Pro

Welcome to your retail scheduling journey! This guide will help you set up the project and start coding.

## 🎯 Your Mission

Transform retail scheduling from a manual nightmare into an automated, intelligent system. By the end of Phase 1, managers should be able to create NY-compliant schedules in <30 minutes instead of 2+ hours.

---

## 📚 Before You Code

### 1. Understand the Problem
Read: `README.md`
- What pain points are we solving?
- How will our solution help managers?

### 2. Study the Architecture
Read: `docs/architecture/system-design.md`
- How do all the pieces fit together?
- Why did we choose Django + React?

### 3. Learn the Rules
Read: `docs/compliance/ny-labor-laws.md`
- What are the 6 NY labor law rules?
- Why is compliance so critical?

### 4. Review the Roadmap
Read: `docs/architecture/phase-1-roadmap.md`
- What are we building in Phase 1?
- What comes in later phases?

---

## 🚀 Setup Your Development Environment

### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/retailsync-pro.git
cd retailsync-pro

# Run setup script
./scripts/setup.sh
```

This script will:
- ✅ Check for Python, Node.js, PostgreSQL
- ✅ Create Python virtual environment
- ✅ Install all dependencies
- ✅ Set up database
- ✅ Create .env file

### Option 2: Manual Setup

#### Backend Setup

```bash
# Create virtual environment
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies (when requirements.txt exists)
pip install -r requirements.txt

# Set up database
createdb retailsync_dev
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Run server
python manage.py runserver
```

#### Frontend Setup

```bash
# Install dependencies
cd frontend
npm install

# Start development server
npm start
```

---

## 📖 Learning Path

### Week 1: Backend Foundation

**Day 1-2: Django Basics**
- What are Django models?
- How do migrations work?
- What is Django REST Framework?

**Day 3-4: Building the Employee API**
- Create Employee model
- Build serializers
- Create API endpoints
- Write tests

**Day 5-7: Compliance Engine**
- Implement meal break validation
- Code overtime calculations
- Test, test, test!

### Week 2: Frontend Development

**Day 8-9: React Fundamentals**
- Components and props
- State management with hooks
- API integration with Axios

**Day 10-12: Schedule Calendar**
- FullCalendar integration
- Drag-and-drop shifts
- Real-time compliance feedback

**Day 13-14: Polish & Deploy**
- Error handling
- Testing
- Deployment to Heroku

---

## 🛠 Development Workflow

### 1. Pick a Task

Look at the Phase 1 roadmap and choose a task for the day.

Example: "Build Employee Model"

### 2. Create a Branch

```bash
git checkout -b feature/employee-model
```

### 3. Write Code

Follow the coding standards:
- **Python:** PEP 8 with Black formatting
- **JavaScript:** Standard style
- **Always:** Write tests!

### 4. Test Your Code

```bash
# Backend tests
pytest

# Frontend tests
npm test
```

### 5. Commit Your Changes

```bash
git add .
git commit -m "feat(employees): create Employee model with validation

- Add Employee model with all required fields
- Implement age validation for minor restrictions
- Add unit tests for model methods

Relates to #1"
```

### 6. Push and Create PR

```bash
git push origin feature/employee-model
```

Then create a Pull Request on GitHub.

---

## 📝 Daily Coding Routine

### Start of Day
1. Review yesterday's progress
2. Check the roadmap - what's next?
3. Read any relevant documentation
4. Pull latest changes: `git pull origin main`

### During Development
1. Write code in small increments
2. Test frequently
3. Commit often (every feature/fix)
4. Ask questions if stuck!

### End of Day
1. Push your changes
2. Update CHANGELOG.md if needed
3. Document any blockers or questions
4. Celebrate progress! 🎉

---

## 🎓 Key Concepts to Learn

### Django Concepts
- **Models:** How data is structured
- **Migrations:** How schema changes are tracked
- **Serializers:** Converting data to JSON
- **ViewSets:** Organizing API logic
- **Tests:** Ensuring code works correctly

### React Concepts
- **Components:** Reusable UI pieces
- **Hooks:** State management (useState, useEffect)
- **Props:** Passing data between components
- **API Integration:** Fetching data from backend
- **Testing:** React Testing Library

### General Concepts
- **REST APIs:** How frontend and backend communicate
- **Authentication:** JWT tokens
- **Version Control:** Git workflow
- **Testing:** Unit tests, integration tests

---

## 🤔 When You're Stuck

### 1. Read the Documentation
- Django docs: https://docs.djangoproject.com/
- React docs: https://react.dev/
- Our docs: `docs/` folder

### 2. Check the Examples
- Look at similar code in the codebase
- Review the code examples in roadmap

### 3. Ask for Help
- Open a GitHub discussion
- Add comments to your PR
- Explain what you've tried

### 4. Debug Systematically
- Add print statements / console.logs
- Use debugger (pdb for Python, Chrome DevTools for React)
- Check error messages carefully

---

## 📊 Tracking Progress

### GitHub Issues
Create issues for:
- Bugs you find
- Features you want to add
- Questions you have

### GitHub Projects
Use the project board to track:
- To Do
- In Progress
- Done

### CHANGELOG.md
Update the changelog when you:
- Complete a feature
- Fix a bug
- Make a significant change

---

## 🎯 Phase 1 Success Criteria

You'll know Phase 1 is complete when:

1. ✅ Backend has full Employee + Schedule APIs
2. ✅ All 6 NY labor law rules are enforced
3. ✅ Frontend has working calendar interface
4. ✅ Compliance violations show in real-time
5. ✅ Budget tracking is accurate
6. ✅ All tests are passing
7. ✅ App is deployed and accessible

---

## 🌟 Beyond Phase 1

Once you complete Phase 1, you'll:
- Have a solid foundation in full-stack development
- Understand how to build complex business logic
- Know how to integrate AI/ML (Phase 2)
- Be ready to build mobile apps (Phase 3)

---

## 💡 Remember

**You're learning as you go - that's the point!**

- Don't expect to understand everything immediately
- Ask questions
- Make mistakes (that's how you learn)
- Celebrate small wins
- Take breaks when stuck
- Enjoy the process!

**This is your passion project. Make it something you're proud of!**

---

## 📬 Next Steps

1. ✅ Read all the documentation
2. ✅ Run the setup script
3. ✅ Start coding Day 1 of Phase 1
4. 🚀 Build something amazing!

Happy coding! 🎉
