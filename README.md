# TutorFlow

## Project Description

TutorFlow is a web application for tutors that enables structured management of students, contracts, and tutoring lessons. The application supports planning with blocked times and travel times, evaluation of income by months and status, and optionally uploading order confirmations (PDF) for data extraction.

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
- **Automatic Status Management**: Past lessons are automatically marked as taught
- **Billing System**: Create invoices from selected lessons with HTML document generation
- **Premium Feature**: AI-powered generation of lesson plans using an LLM API

## Features

### Basic Features
- **Student Management**: Centralized management with contact information, school, subjects
- **Contract Management**: Rates, duration, contract period, planned units
- **Lesson Planning**: Planning with date, time, travel times
  - **Week View**: Interactive week view (Mon-Sun, 08:00-22:00) as central UI for appointment planning
    - **Drag-to-Create**: Drag a time range to create a new appointment (tutoring or blocked time)
    - **Appointment Display**: Lessons (blue), blocked times (orange), conflicts (red border)
    - **Click on Appointment**: Opens edit form
  - **Month Calendar**: Alternative view for monthly overview
  - **Recurring Lessons**: Recurring lessons (e.g., every Monday/Thursday) with automatic generation
  - **Automatic Status Management**: Lesson status (planned/taught) is automatically set based on date
- **Blocked Times**: Management of personal appointments (university, job, etc.)
  - **Calendar Integration**: Blocked times are managed exclusively via the calendar (create, edit, display)
  - **Multi-day Blocked Times**: Support for multi-day blocks (e.g., vacation/travel)
  - **Recurring Blocked Times**: Recurring blocked times (e.g., every Tuesday 6-8 PM) with automatic generation
- **Conflict Detection**: Automatic detection of overlaps (including travel times)
  - **Scheduling**: Overlaps with other lessons and blocked times
  - **Contract Quota**: Detection of violations against agreed lesson quota (based on ContractMonthlyPlan)
- **Income Overview**: Monthly and yearly evaluations by status (planned, taught, paid)
- **Dashboard**: Overview of today's/upcoming lessons, conflicts, income

### Premium Features
- **AI-powered Lesson Plans**: Automatic generation of detailed lesson plans via LLM API
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
  export LLM_MODEL_NAME="gpt-3.5-turbo"  # Optional
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

**Demo Login:**
- Login URL: `http://127.0.0.1:8000/admin/`
- Username: `demo_premium`
- Password: `demo123`

**Note:** Login is done via the Django Admin interface. After successful login, you can access the various areas of the application via the navigation.

**Demo Scenario:**
The demo data shows a realistic scenario with:
- Multiple students in different grade levels
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
```bash
cd backend
python manage.py makemessages -l de
# Edit locale/de/LC_MESSAGES/django.po
python manage.py compilemessages
```

## Projektstruktur

```
tutorflow/
├── backend/              # Django-Projekt
│   ├── apps/            # Feature-spezifische Apps
│   ├── config/          # Projektkonfiguration
│   ├── tutorflow/       # Django-Projektkonfiguration
│   └── manage.py
├── docs/                # Dokumentation
│   ├── ARCHITECTURE.md
│   ├── ETHICS.md
│   ├── PHASES.md
│   ├── CHECKPOINTS.md
│   └── API.md
├── scripts/             # Validierungsskripte
├── venv/                # Virtuelles Environment
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

This project is developed as part of the Teca-Hacks Hackathon.

## Contact

For questions or suggestions, please create an issue in the repository.

