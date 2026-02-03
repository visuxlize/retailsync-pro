# Contributing to RetailSync Pro

Thank you for considering contributing to RetailSync Pro! This document outlines the process for contributing to this project.

## 🎯 Project Philosophy

RetailSync Pro is built with these principles:

1. **Learning First** - Every feature should teach us something new
2. **Real-World Problem Solving** - Features must solve actual retail scheduling pain points
3. **Code Quality** - Clean, documented, testable code
4. **User-Centric** - Always think about the manager using this at 6am or the employee checking their phone

## 🚀 Getting Started

### Setting Up Your Development Environment

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub, then:
   git clone https://github.com/YOUR_USERNAME/retailsync-pro.git
   cd retailsync-pro
   ```

2. **Set up upstream remote**
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/retailsync-pro.git
   ```

3. **Install dependencies**
   ```bash
   # Backend
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Dev dependencies (pytest, black, etc.)
   
   # Frontend
   cd ../frontend
   npm install
   ```

4. **Set up pre-commit hooks**
   ```bash
   # From project root
   pre-commit install
   ```

## 📋 Development Workflow

### 1. Pick an Issue or Create One

- Browse [open issues](https://github.com/YOUR_USERNAME/retailsync-pro/issues)
- Look for issues tagged `good-first-issue` if you're new
- Comment on the issue to claim it: "I'd like to work on this!"

### 2. Create a Feature Branch

```bash
git checkout main
git pull upstream main
git checkout -b feature/your-feature-name
```

**Branch naming conventions:**
- `feature/` - New features (e.g., `feature/shift-swapping`)
- `fix/` - Bug fixes (e.g., `fix/overtime-calculation`)
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Adding tests

### 3. Write Code

#### Backend (Django/Python)

**Style Guide:**
- Follow PEP 8 with Black formatting
- 4 spaces indentation
- Max line length: 88 characters (Black default)
- Detailed docstrings for all functions/classes

**Example:**
```python
def calculate_overtime_hours(employee: Employee, shifts: List[Shift]) -> Decimal:
    """
    Calculate total overtime hours for an employee in a given week.
    
    NY Labor Law requires overtime pay (1.5x) for hours worked over 40 in a week.
    
    Args:
        employee: Employee instance
        shifts: List of Shift instances for the week
    
    Returns:
        Decimal: Number of overtime hours (0 if under 40 total hours)
    
    Example:
        >>> shifts = [Shift(duration=8), Shift(duration=8), ...]  # 42 total hours
        >>> calculate_overtime_hours(employee, shifts)
        Decimal('2.00')
    """
    total_hours = sum(shift.duration for shift in shifts)
    overtime_hours = max(Decimal('0'), total_hours - Decimal('40'))
    return overtime_hours
```

**Testing:**
```bash
# Run all tests
pytest

# Run specific test file
pytest backend/apps/scheduling/tests/test_compliance.py

# Run with coverage
pytest --cov=backend --cov-report=html
```

#### Frontend (React/JavaScript)

**Style Guide:**
- Standard style, 2 spaces indentation
- Functional components with hooks (no class components)
- Descriptive variable names

**Example:**
```javascript
/**
 * ShiftCard component displays a single shift with employee and time details.
 * 
 * @param {Object} shift - Shift object from API
 * @param {Function} onEdit - Callback when edit button clicked
 * @param {Function} onDelete - Callback when delete button clicked
 */
const ShiftCard = ({ shift, onEdit, onDelete }) => {
  const [isHovered, setIsHovered] = useState(false);
  
  return (
    <Card 
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <Typography variant="h6">{shift.employee.name}</Typography>
      <Typography variant="body2">
        {shift.start_time} - {shift.end_time}
      </Typography>
      {isHovered && (
        <CardActions>
          <Button onClick={() => onEdit(shift)}>Edit</Button>
          <Button onClick={() => onDelete(shift)}>Delete</Button>
        </CardActions>
      )}
    </Card>
  );
};
```

**Testing:**
```bash
# Run tests
npm test

# Run with coverage
npm test -- --coverage
```

### 4. Commit Your Changes

**Commit message format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation changes
- `style` - Code style changes (formatting, no logic change)
- `refactor` - Code refactoring
- `test` - Adding tests
- `chore` - Maintenance tasks

**Example:**
```bash
git add .
git commit -m "feat(scheduling): add NY spread of hours compliance check

- Implement calculation for shifts spanning >10 hours
- Add automatic penalty cost to budget
- Include unit tests for edge cases

Closes #42"
```

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then go to GitHub and create a Pull Request with:
- **Clear title** describing what you did
- **Description** explaining why and how
- **Screenshots** if UI changes
- **Testing steps** for reviewers

**PR Template:**
```markdown
## What does this PR do?
Brief description of changes

## Why are we making this change?
Link to issue or explain the problem

## How has this been tested?
- [ ] Unit tests added/updated
- [ ] Manual testing completed
- [ ] All tests passing

## Screenshots (if applicable)
[Add screenshots here]

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes (or clearly documented)
```

## 🧪 Testing Guidelines

### Backend Testing

**What to test:**
- All compliance rules (critical!)
- API endpoints
- Model methods
- Edge cases

**Example test:**
```python
import pytest
from decimal import Decimal
from apps.scheduling.compliance import check_meal_breaks

def test_shift_over_6_hours_requires_meal_break():
    """Shifts over 6 hours must have a 30-minute meal break."""
    shift = Shift(
        start_time=time(9, 0),
        end_time=time(17, 0),  # 8-hour shift
        meal_break=None
    )
    
    violation = check_meal_breaks(shift)
    
    assert violation is not None
    assert violation.type == 'MISSING_MEAL_BREAK'
    assert '30-min break' in violation.fix_suggestion
```

### Frontend Testing

**What to test:**
- Component rendering
- User interactions
- API integration
- Error handling

**Example test:**
```javascript
import { render, screen, fireEvent } from '@testing-library/react';
import ShiftCard from './ShiftCard';

test('displays employee name and shift time', () => {
  const shift = {
    employee: { name: 'John Doe' },
    start_time: '09:00',
    end_time: '17:00'
  };
  
  render(<ShiftCard shift={shift} />);
  
  expect(screen.getByText('John Doe')).toBeInTheDocument();
  expect(screen.getByText('09:00 - 17:00')).toBeInTheDocument();
});

test('calls onEdit when edit button clicked', () => {
  const mockOnEdit = jest.fn();
  const shift = { id: 1, employee: { name: 'John' } };
  
  render(<ShiftCard shift={shift} onEdit={mockOnEdit} />);
  
  fireEvent.click(screen.getByText('Edit'));
  
  expect(mockOnEdit).toHaveBeenCalledWith(shift);
});
```

## 📖 Documentation

### When to Update Documentation

- **New features** - Update README and API docs
- **Breaking changes** - Update migration guide
- **Bug fixes** - Add to changelog
- **Configuration changes** - Update deployment docs

### Documentation Standards

- Use clear, simple language
- Include code examples
- Add screenshots for UI features
- Keep docs in sync with code

## 🔍 Code Review Process

### As a Contributor

- Respond to feedback promptly
- Don't take criticism personally (we're all learning!)
- Ask questions if feedback is unclear
- Make requested changes in new commits (don't force-push)

### As a Reviewer

- Be kind and constructive
- Explain the "why" behind suggestions
- Approve PRs that improve the codebase (perfect is the enemy of good)
- Test the changes locally if possible

## 🎨 Design Decisions

When making significant architectural decisions:

1. **Open an issue first** to discuss the approach
2. **Document the decision** in `/docs/architecture/decisions/`
3. **Consider future phases** - Will this work in Phase 4?
4. **Think about scale** - What happens with 1000 stores?

## 🐛 Bug Reports

**Use the bug report template and include:**
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots/error logs
- Environment (OS, Python version, etc.)

## 💡 Feature Requests

**Use the feature request template and include:**
- User story: "As a [manager], I want [feature] so that [benefit]"
- Business impact: How does this save time or prevent problems?
- Proposed solution (optional)

## 📞 Getting Help

- **Questions?** Open a discussion on GitHub
- **Stuck?** Comment on your PR and tag maintainers
- **Found a security issue?** Email privately (don't open public issue)

## 🎓 Learning Resources

### Django
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework Tutorial](https://www.django-rest-framework.org/tutorial/quickstart/)

### React
- [React Documentation](https://react.dev/)
- [React Testing Library](https://testing-library.com/react)

### General
- [Git Workflow](https://guides.github.com/introduction/flow/)
- [Writing Good Commit Messages](https://chris.beams.io/posts/git-commit/)

---

**Remember: Every contribution, no matter how small, is valuable. We're all learning together! 🚀**
