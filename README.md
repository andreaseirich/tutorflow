# TutorFlow

## Project Overview

TutorFlow is a comprehensive web application designed for tutors to manage their tutoring business efficiently. It solves the challenge of organizing students, contracts, and lessons while avoiding scheduling conflicts and maintaining clear financial oversight. The application is built for tutors who need a structured, reliable tool to manage their teaching activities, track income, and generate invoices—all with intelligent conflict detection and AI-powered lesson planning support.

## Key Features

- **📅 Intelligent Scheduling**: Interactive week view with drag-to-create appointments, automatic conflict detection (time overlaps & contract quotas), and recurring lesson support
- **👥 Student & Contract Management**: Centralized management of students, contracts, and monthly planning with flexible contract structures
- **💰 Billing & Income Tracking**: Automated invoice generation from lessons, monthly/yearly income overviews, and planned vs. actual comparisons
- **🚫 Blocked Time Management**: Personal appointment blocking (vacations, university, etc.) with multi-day and recurring support, fully integrated in calendar
- **🤖 AI-Powered Lesson Plans**: Premium feature for automatic generation of structured lesson plans using LLM APIs (OpenAI-compatible) with automatic retry on rate limits
- **🌍 Full Internationalization**: Complete i18n/l10n support with English (default) and German, including proper date, number, and currency formatting

## Quick Start

### Prerequisites
- Python 3.11 or higher
- pip

### Installation

1. **Clone repository:**
```bash
git clone <repository-url>
cd tutorflow
```

2. **Create and activate virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Setup database:**
```bash
cd backend
python manage.py migrate
python manage.py compilemessages  # For i18n support
```

5. **Start development server:**
```bash
python manage.py runserver
```

The application is available at `http://127.0.0.1:8000/`.

### Demo Login & Quick Tour

**Load demo data:**
```bash
cd backend
python manage.py seed_demo_data
```

Or clear existing data and create fresh demo data:

```bash
python manage.py seed_demo_data --clear
```

**Demo Data Includes:**
- 4 students with different profiles
- Contracts with monthly plans (for quota conflict examples)
- Multiple lessons (including time conflicts, quota conflicts, and recurring lessons)
- Recurring lessons (weekly patterns with weekday selection: Mo+We for student4, Tu+Th for student2)
- Blocked times (including multi-day vacation and conflict examples)
- Premium user with generated lesson plans
- Non-premium user for comparison

**Logins:**
- **Premium User:**
  - URL: `http://127.0.0.1:8000/admin/`
  - Username: `demo_premium`
  - Password: `demo123`
- **Standard User:**
  - URL: `http://127.0.0.1:8000/admin/`
  - Username: `demo_standard`
  - Password: `demo123`

**Demo Features to Explore:**
- Recurring lessons: Check student4's lessons (Monday and Wednesday pattern)
- Quota conflicts: Contract1 has 3 planned units in November, but 4 lessons created (lesson8 shows quota conflict)
- Time conflicts: Lesson1 and Lesson2 overlap, lesson_conflict overlaps with blocked_time3
- Lesson plans: lesson1 has a lesson plan (click on lesson in week view), lesson3 can be used to test AI generation

**See main features in 2 minutes:**
1. **Dashboard** (`/`): Overview of today's lessons, upcoming appointments, and conflicts
2. **Week View** (`/lessons/week/`): Interactive calendar - drag time ranges to create appointments, click to edit
3. **Income Overview** (`/income/`): Monthly/yearly financial tracking with planned vs. actual comparisons
4. **Billing** (`/billing/invoices/`): Create invoices from taught lessons with HTML document generation

## Screenshots / Demo

### Screenshots

![Dashboard](docs/screenshots/dashboard.png)
*Dashboard showing today's lessons, upcoming appointments, and conflicts*

![Weekly Calendar](docs/screenshots/weekly_calendar.png)
*Interactive week view with drag-to-create functionality for lessons and blocked times*

![Invoice Overview](docs/screenshots/invoice_overview.png)
*Invoice list and detail view with automatic generation from taught lessons*

### Full Demo GIF

> **TODO**: Add animated GIF showing complete workflow:
> - Creating a student and contract
> - Scheduling lessons via drag-to-create in week view
> - Detecting and resolving conflicts
> - Generating invoices from taught lessons
> - Viewing income overview

### How It Works

TutorFlow follows a simple 3-step workflow:

1. **📅 Scheduling**: Plan lessons via the interactive week view. Drag time ranges to create appointments, set up recurring lessons, and block personal time. The system automatically detects scheduling conflicts and contract quota violations.

2. **⚠️ Conflict Detection**: Real-time conflict detection ensures you never double-book. The system checks for:
   - Time overlaps with other lessons (including travel times)
   - Overlaps with blocked times
   - Contract quota violations (planned vs. actual units)

3. **💰 Billing**: Once lessons are marked as "taught", generate invoices automatically. The system calculates amounts based on contract rates and unit durations, creates invoice documents, and tracks income with planned vs. actual comparisons.

## Problem

Tutors need a reliable tool for managing their students, contracts, and lessons. Planning must avoid scheduling conflicts, income must be clearly presented, and management should be structured and traceable.

## Solution

TutorFlow provides a complete solution for managing tutoring activities:

- **Student Management**: Centralized management of students with contact information, school/grade, subjects
- **Contract Management**: Management of contracts with rates, duration, contract period
- **Lesson Planning**: Planning of tutoring lessons with date, time, and travel times
  - **Calendar View**: Central UI for lesson planning - Lessons are primarily planned and edited via the calendar view
  - **Recurring Lessons**: Support for recurring lessons (e.g., every Monday at 2 PM)
- **Blocked Times**: Management of personal appointments and blocked times (e.g., university, job, community)
- **Income Evaluation**: Monthly and yearly evaluations of income by status
- **Automatic Status Management**: Lessons with status 'planned' are automatically set to 'taught' when their end time is in the past. Updates happen automatically when accessing Dashboard, Week View, or Income Overview. Can also be run manually via `python manage.py update_past_lessons`
- **Billing System**: Create invoices from selected lessons with HTML document generation
- **Premium Feature**: AI-powered generation of lesson plans using an LLM API

## Features

### Basic Features
- **Student Management**: Centralized management with contact information, school, subjects
- **Contract Management**: Rates, duration, contract period, planned units
- **Lesson Planning**: Planning with date, time, travel times
  - **Week View**: Interactive week view (Mon-Sun, 08:00-22:00) as central UI for appointment planning
    - **Default calendar view**: Week view is the default calendar view
    - **Drag-to-Create**: Drag a time range to create a new appointment (tutoring or blocked time)
    - **Recurring option**: When creating a lesson, users can select "Repeat this lesson" with pattern (Weekly/Bi-weekly/Monthly) and weekday selection
    - **Appointment Display**: Lessons (blue), blocked times (orange), conflicts (red border/icon)
    - **Click on Lesson**: Opens lesson plan view (for viewing/creating AI lesson plans)
    - **Click on Edit Icon** (✏️) in lesson block: Opens lesson edit form
    - **Click on Blocked Time**: Opens blocked time edit form
    - **Click on Conflict Icon**: Opens conflict detail view with reasons
  - **Month Calendar**: Alternative view for monthly overview (legacy, redirects to week view)
  - **Recurring Lessons**: Recurring lessons are created exclusively via the lesson creation form in week view (no separate button/page)
  - **Automatic Status Management**: Lesson status (planned/taught) is automatically updated based on time progression. Past planned lessons become 'taught' automatically when views are accessed
- **Blocked Times**: Management of personal appointments (university, job, etc.)
  - **Calendar Integration**: Blocked times are managed exclusively via the calendar (create, edit, display)
  - **Multi-day Blocked Times**: Support for multi-day blocks (e.g., vacation/travel)
  - **Recurring Blocked Times**: Recurring blocked times (e.g., every Tuesday 6-8 PM) with automatic generation
- **Conflict Detection**: Automatic detection of overlaps (including travel times)
  - **Scheduling**: Overlaps with other lessons and blocked times
  - **Contract Quota**: Detection of violations against agreed lesson quota (based on ContractMonthlyPlan)
  - **Conflict Reasons**: Detailed conflict information with type, affected objects, and messages
  - **Automatic Recalculation**: Conflicts are automatically recalculated after any lesson or blocked time change
- **Income Overview**: Monthly and yearly evaluations by status (planned, taught, paid)
- **Dashboard**: Overview of today's/upcoming lessons, conflicts, income

### Premium Features
- **AI-powered Lesson Plans**: Automatic generation of detailed lesson plans via LLM API
  - **UI Integration**: Prominent "Generate AI Lesson Plan" button in lesson detail view for premium users
  - **Premium Badge**: Premium status is displayed in the dashboard
  - **Non-Premium Notice**: Non-premium users see a disabled button with a notice about premium availability
- **Human-in-the-Loop**: Generated plans can be adjusted and are accountable

## Tech Stack

### Backend
- **Framework**: Django 5.2.9
- **Database**: SQLite (development), PostgreSQL (optional for production)
- **Python**: 3.11+
- **Dependencies**: Django, requests (see `requirements.txt`)
- **Internationalization**: Full i18n support with English as default language and German translations

### Premium Features (AI)
- **LLM Integration**: OpenAI-compatible API for AI-generated lesson plans
- **Configuration**: API keys via environment variables:
  ```bash
  export LLM_API_KEY="your-api-key"
  export LLM_API_BASE_URL="https://api.openai.com/v1"  # Optional
  export LLM_MODEL_NAME="gpt-5-turbo"  # Optional
  ```

### Frontend
- To be defined in later phases (e.g., Django Templates, HTMX, Tailwind)

## Setup

### Prerequisites
- Python 3.11 or higher
- pip

### Installation

1. Clone repository:
```bash
git clone <repository-url>
cd tutorflow
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Migrate database:
```bash
cd backend
python manage.py migrate
```

5. Compile translations (for i18n support):
```bash
python manage.py compilemessages
```

6. Start development server:
```bash
python manage.py runserver
```

The application is then available at `http://127.0.0.1:8000/`.

### Load Demo Data

To test the application with demo data, you can run the seed command:

```bash
cd backend
python manage.py seed_demo_data
```

This creates:
- 3 demo students with different profiles
- Associated contracts
- Several lessons (including a conflict for demonstration)
- Blocked times
- 1 premium user with generated lesson plan

**Demo Logins:**
- **Premium User:**
  - Login URL: `http://127.0.0.1:8000/admin/`
  - Username: `demo_premium`
  - Password: `demo123`
- **Standard User:**
  - Login URL: `http://127.0.0.1:8000/admin/`
  - Username: `demo_standard`
  - Password: `demo123`

**Note:** Login is done via the Django Admin interface. After successful login, you can access the various areas of the application via the navigation.

**Demo Scenario:**
The demo data shows a realistic scenario with:
- 4 students in different grade levels with different contract types
- Recurring lessons: Monday+Wednesday pattern for student4, Tuesday+Thursday for student2
- Contract monthly plans: Contract1 has 3 planned units in November (quota conflict example)
- Multiple conflicts:
  - Time conflicts: Lesson1 and Lesson2 overlap, lesson_conflict overlaps with blocked_time3
  - Quota conflicts: Lesson8 exceeds planned quota (4th lesson but only 3 planned)
- Blocked times: University lecture, multi-day vacation, conflict example
- Lesson plans: lesson1 has a generated lesson plan, lesson3 can be used to test AI generation
- Premium vs. non-premium user comparison
- Different contracts (private and via institute)
- A conflict situation between two lessons (to demonstrate conflict detection)
- A blocked time (university lecture)
- A premium user with AI-generated lesson plan

## Internationalization

TutorFlow supports multiple languages with English as the default language. German translations are available as a secondary language.

- **Default Language**: English (`en`)
- **Supported Languages**: English (`en`), German (`de`)
- **Language Switching**: Available via dropdown in the navigation bar
- **Translation Files**: Located in `backend/locale/`

To update translations:

**Prerequisites for compiling translations:**
- **Linux/macOS**: GNU gettext tools are usually pre-installed. If not:
  - Debian/Ubuntu: `sudo apt-get install gettext`
  - macOS: `brew install gettext`
- **Windows**: Install GNU gettext for Windows:
  1. Download from: https://mlocati.github.io/articles/gettext-iconv-windows.html
  2. Or use Chocolatey: `choco install gettext`
  3. Or use WSL (Windows Subsystem for Linux) for a Linux-like environment
  4. Add the `bin` directory of gettext to your Windows PATH environment variable

```bash
cd backend
python manage.py makemessages -l de
# Edit locale/de/LC_MESSAGES/django.po
python manage.py compilemessages
```

## Project Structure

```
tutorflow/
├── backend/              # Django project
│   ├── apps/            # Feature-specific apps
│   ├── config/          # Project configuration
│   ├── tutorflow/       # Django project configuration
│   └── manage.py
├── docs/                # Documentation
│   ├── ARCHITECTURE.md
│   ├── ETHICS.md
│   ├── PHASES.md
│   ├── CHECKPOINTS.md
│   └── API.md
├── scripts/             # Validation scripts
├── venv/                # Virtual environment
├── requirements.txt
├── README.md
├── CHANGELOG.md
└── cursor_master_prompt.txt
```

## Development

The project is developed in phases. See `docs/PHASES.md` for details.

## Validation

A validation script is available to check the project:

```bash
./scripts/validate.sh
```

The script performs the following checks:
- Django System Check
- Test Suite
- Check for TODO comments
- Check for debug output
- Documentation check

## Documentation

- **ARCHITECTURE.md**: Architecture overview and technical details
- **ETHICS.md**: Ethical-Christian guidelines and data protection principles
- **PHASES.md**: Overview of development phases
- **CHECKPOINTS.md**: Progress log and checkpoints
- **API.md**: API documentation
- **DEVPOST.md**: Content for Devpost submission

## License

This project is licensed under the Apache License 2.0 – see the [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Andreas Eirich

## Contact

For questions or suggestions, please create an issue in the repository.

