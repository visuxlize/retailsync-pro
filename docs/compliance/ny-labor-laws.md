# NY Labor Law Compliance Guide

## Overview

New York has some of the strictest labor laws in the United States. **Violating these laws can result in penalties of $50,000+ per violation, class-action lawsuits, and criminal charges in severe cases.**

RetailSync Pro's compliance engine automatically enforces all NY labor regulations to protect both employees and employers.

---

## Critical Compliance Rules

### 1. Meal Breaks (NY Labor Law § 162)

**The Rule:**
Employees working more than 6 hours in a shift **must** receive a 30-minute unpaid meal break.

**When the break must occur:**
- For shifts starting before 11am and continuing past 7pm: break between 11am-2pm
- For shifts starting between 1pm-6am: break in middle of shift
- Cannot be at the start or end of the shift

**Penalties for violation:**
- $1,000 per violation per day
- Employee entitled to 1 hour of pay for each day break was missed

**How RetailSync Pro enforces this:**
```python
# Pseudocode from our compliance engine
if shift.duration > 6 hours:
    if not shift.has_meal_break:
        raise ComplianceViolation(
            "Missing required 30-minute meal break",
            penalty_per_day=1000,
            fix="Add 30-min break between hours 3-4 of shift"
        )
```

**Example:**
❌ **Illegal:** 9am-5pm shift (8 hours) with no break
✅ **Legal:** 9am-12:30pm work, 12:30pm-1pm break, 1pm-5pm work

---

### 2. Overtime Pay (NY Labor Law § 650)

**The Rule:**
Employees working more than **40 hours in a workweek** must be paid 1.5x their regular rate for overtime hours.

**What counts as a "workweek":**
- 7 consecutive 24-hour periods (168 hours total)
- Defined by employer (e.g., Sunday-Saturday or Monday-Sunday)
- Must be consistent

**Exemptions (who doesn't get overtime):**
- Executive, administrative, professional employees earning >$1,125/week
- Outside salespeople
- *Most retail workers ARE eligible for overtime*

**Penalties for violation:**
- Back pay for unpaid overtime (going back 6 years!)
- Liquidated damages (2x the unpaid amount)
- Attorney fees

**How RetailSync Pro enforces this:**
```python
def calculate_weekly_hours(employee, week_start):
    total_hours = sum(shift.duration for shift in employee.shifts_in_week(week_start))
    
    if total_hours > 40:
        regular_hours = 40
        overtime_hours = total_hours - 40
        overtime_pay = overtime_hours * employee.hourly_rate * 1.5
        
        return {
            "overtime_hours": overtime_hours,
            "additional_cost": overtime_pay,
            "warning": f"{employee.name} has {overtime_hours}h OT"
        }
```

**Example:**
Employee rate: $18/hour
| Day | Hours | Pay |
|-----|-------|-----|
| Mon-Fri | 8h each = 40h | 40h × $18 = $720 |
| Sat | 5h | 5h × $27 (1.5x) = $135 |
| **Total** | **45h** | **$855** |

---

### 3. Spread of Hours (NY Hospitality Industry Regulation)

**The Rule:**
If the time between an employee's **start and end time** (including breaks) exceeds **10 hours in a single day**, the employee is entitled to **one additional hour of pay at minimum wage**.

**Who this applies to:**
- Hospitality workers (restaurants, hotels)
- Retail workers in some cases
- *Check with your legal team if unsure*

**Example scenarios:**

**Scenario 1: Spread >10 hours**
- Shift: 8am-7pm (11-hour spread)
- Worked: 9 hours (with 2-hour unpaid lunch break)
- Penalty: 1 hour × minimum wage = **$15 extra pay**

**Scenario 2: Spread ≤10 hours (no penalty)**
- Shift: 9am-6pm (9-hour spread)
- Worked: 8 hours (with 1-hour lunch)
- Penalty: **$0**

**Penalties for violation:**
- Employee entitled to extra hour of pay
- Potential DOL investigation

**How RetailSync Pro enforces this:**
```python
def check_spread_of_hours(shift):
    spread_hours = (shift.end_time - shift.start_time).total_seconds() / 3600
    
    if spread_hours > 10:
        extra_pay = MINIMUM_WAGE  # $15 in NY
        return SpreadPenalty(
            spread=spread_hours,
            penalty=extra_pay,
            suggestion="Split into two shorter shifts to avoid penalty"
        )
```

---

### 4. Day of Rest (NY Labor Law § 161)

**The Rule:**
Employees must receive at least **24 consecutive hours off every calendar week**.

**What is a "calendar week":**
- Sunday through Saturday
- Or employer-defined workweek

**Exemptions:**
- Farm workers
- Domestic workers
- Some healthcare workers

**Penalties for violation:**
- $500 per violation
- Employee can refuse to work 7th consecutive day

**How RetailSync Pro enforces this:**
```python
def validate_day_of_rest(employee, week_shifts):
    days_worked = set(shift.date.weekday() for shift in week_shifts)
    
    if len(days_worked) == 7:  # Worked all 7 days
        return ComplianceViolation(
            type="NO_DAY_OF_REST",
            message=f"{employee.name} scheduled all 7 days",
            penalty=500,
            fix="Remove one shift to provide 24-hour rest period"
        )
```

**Example:**
❌ **Illegal:** Mon, Tue, Wed, Thu, Fri, Sat, Sun shifts
✅ **Legal:** Mon, Tue, Wed, Thu, Fri, Sat shifts (Sunday off)

---

### 5. Minor Employee Restrictions (NY Labor Law § 142)

**The Rule:**
Employees under 18 have strict work hour limitations to protect their education and health.

**School days (when school is in session):**
| Age | Max Hours/Day | Max Hours/Week | Latest End Time |
|-----|---------------|----------------|-----------------|
| 14-15 | 3 hours | 18 hours | 7pm |
| 16-17 | 4 hours | 28 hours | 10pm |

**Non-school days (summer, weekends, holidays):**
| Age | Max Hours/Day | Max Hours/Week | Latest End Time |
|-----|---------------|----------------|-----------------|
| 14-15 | 8 hours | 40 hours | 9pm (7pm June-Labor Day) |
| 16-17 | 8 hours | 48 hours | Midnight (10pm school nights) |

**Additional restrictions:**
- Cannot work before 7am
- Cannot work during school hours
- Must have work permit

**Penalties for violation:**
- $1,000-$3,000 per violation
- Potential criminal charges
- Loss of employment certificate

**How RetailSync Pro enforces this:**
```python
def validate_minor_shift(employee, shift, is_school_day):
    if employee.age < 18:
        # Check end time
        if is_school_day and shift.end_time > time(22, 0):  # 10pm
            raise ComplianceViolation("Minors can't work past 10pm on school nights")
        
        # Check daily hours
        if is_school_day and shift.duration > 4:
            raise ComplianceViolation("Minors can't work >4 hours on school days")
        
        # Check weekly hours (14-15 year olds)
        if employee.age < 16:
            weekly_hours = calculate_weekly_hours(employee, shift.week)
            if is_school_day and weekly_hours > 18:
                raise ComplianceViolation("Minors 14-15 can't work >18 hours during school week")
```

**Example:**
16-year-old employee during school year:
❌ **Illegal:** Monday 6pm-11pm shift (ends too late)
✅ **Legal:** Monday 4pm-8pm shift (4 hours, ends before 10pm)

---

### 6. Predictive Scheduling (NYC Fair Workweek Law)

**The Rule (NYC only, may expand statewide):**
Schedules must be posted **14 days in advance**. Changes made with less than 14 days notice trigger premium pay.

**Premium pay schedule:**
| Notice Period | Premium Pay |
|---------------|-------------|
| <14 days notice | $10 |
| <7 days notice | $15 |
| <24 hours notice | $45 |
| Shift cancelled <72 hours before | $75 |

**Additional requirements:**
- Good faith estimate of schedule at time of hire
- Right to decline shifts added with <72 hours notice
- No retaliation for declining last-minute shifts

**Who this applies to:**
- Fast food workers (definitely)
- Retail workers in chains with 20+ locations (sometimes)
- *Check if your business is covered*

**Penalties for violation:**
- Premium pay owed to employees
- $500-$1,000 fines per violation
- Potential class-action lawsuits

**How RetailSync Pro enforces this:**
```python
def check_predictive_scheduling(schedule, publish_date):
    days_notice = (schedule.week_start - publish_date).days
    
    if days_notice < 14:
        total_penalty = 0
        violations = []
        
        for shift in schedule.shifts:
            if days_notice < 1:
                penalty = 45
            elif days_notice < 7:
                penalty = 15
            else:
                penalty = 10
            
            total_penalty += penalty
            violations.append({
                "employee": shift.employee,
                "shift": shift,
                "penalty": penalty
            })
        
        return {
            "total_penalty": total_penalty,
            "violations": violations,
            "recommendation": f"Wait until {schedule.week_start - timedelta(days=14)} to publish"
        }
```

**Example:**
Schedule for week of Feb 10-16:
- ❌ Published on Feb 9 (1 day notice): $45/employee penalty
- ⚠️ Published on Feb 5 (5 days notice): $15/employee penalty
- ✅ Published on Jan 27 (14 days notice): No penalty

---

## RetailSync Pro Compliance Workflow

### Step 1: Real-Time Validation
As manager creates schedule in UI:
```
Manager adds shift → Compliance engine validates → Show warning if violated
```

### Step 2: Pre-Publish Check
Before publishing schedule:
```
Manager clicks "Publish" → Run full compliance audit → Block if critical violations
```

### Step 3: Ongoing Monitoring
After schedule is live:
```
Employee requests shift swap → Re-validate compliance → Approve/deny swap
```

---

## Common Compliance Mistakes (and how we prevent them)

### Mistake #1: "Clopening"
**What it is:** Closing shift followed by opening shift the next day
**Example:** Work until 11pm, then start at 6am (7-hour gap)
**NY Law:** Not explicitly illegal, but violates "spread of hours" if combined spread >10 hours
**RetailSync Pro:** Warns when gap between shifts <10 hours, suggests alternative assignments

### Mistake #2: Forgetting meal breaks in long shifts
**What it is:** Scheduling 8-hour shift without designating break time
**RetailSync Pro:** Auto-inserts 30-min break at midpoint of shifts >6 hours

### Mistake #3: Accidentally scheduling minors late
**What it is:** Giving 16-year-old a shift that ends at 11pm
**RetailSync Pro:** Hard block - won't allow shift creation for minors past legal end times

### Mistake #4: Publishing schedules too late
**What it is:** Creating next week's schedule on Friday (9 days notice)
**RetailSync Pro:** Calculates premium pay penalty, suggests earlier publish date

---

## Audit Trail & Reporting

Every schedule change is logged for compliance audits:

```python
# What we track
{
    "timestamp": "2026-02-03T14:23:11Z",
    "user": "manager@store1247.com",
    "action": "publish_schedule",
    "schedule_id": 1234,
    "compliance_status": "COMPLIANT",
    "violations": [],
    "employees_affected": 14
}
```

**Exportable reports:**
- Weekly compliance summary (for district managers)
- Violation history (for legal team)
- Audit logs (for DOL investigations)

---

## Additional Resources

- [NY Department of Labor](https://dol.ny.gov/)
- [NYC Fair Workweek Law Full Text](https://www1.nyc.gov/site/dca/workers/workersrights/fairworkweek-retail-workers.page)
- [NFIB NY Labor Law Guide](https://www.nfib.com/foundations/legal-center/legal-compliance/newyork-labor-law/)

---

**⚠️ Legal Disclaimer:**
This guide is for educational purposes and does not constitute legal advice. RetailSync Pro automates compliance checks based on our interpretation of NY labor laws, but you should consult with an employment attorney to ensure full compliance with all applicable laws and regulations.
