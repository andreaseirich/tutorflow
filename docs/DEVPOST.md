# TutorFlow – Devpost Submission

## Short Description

TutorFlow is a web application for tutors to manage students, contracts, lessons, and income in a structured way. The application offers intelligent conflict detection, income analysis, and optional AI-powered lesson planning.

## Problem & Motivation

Tutors face the challenge of organizing their work professionally:
- **Scheduling**: Avoiding overlaps, considering travel times, planning blocked times
- **Management**: Structurally managing students, contracts, fees, and lessons
- **Income Overview**: Tracking monthly and yearly income by status (planned, taught, paid)
- **Lesson Preparation**: Time-consuming creation of lesson plans

TutorFlow solves these problems with a user-friendly, structured solution.

## What TutorFlow Does

### Core Features

1. **Student Management**
   - Centralized management with contact data, school, grade, subjects
   - Standard lesson location per student

2. **Contract Management**
   - Fee per unit, duration, contract period
   - Planned units per month
   - Distinction between private and institute contracts

3. **Intelligent Lesson Planning**
   - **Calendar View**: Central UI for scheduling - lessons are primarily planned and edited via the calendar view
   - Planning with date, time, location
   - **Recurring Lessons**: Support for repeating lessons (e.g., every Monday at 2 PM)
   - **Automatic Conflict Detection**: Detects overlaps including travel times
   - **Blocked Times**: Personal appointments (university, job, etc.) are marked as occupied
   - **Travel Times**: Before and after the lesson are considered

4. **Income Overview**
   - Monthly and yearly reports
   - Filtering by status (planned, taught, paid)
   - Breakdown by contracts/students

5. **Dashboard**
   - Overview of today's and upcoming lessons
   - Conflict warnings
   - Current monthly income

### Premium Feature: AI-Powered Lesson Plans

- **Automatic Generation**: Detailed lesson plans via LLM API
- **Human-in-the-Loop**: Generated plans can be adjusted and verified
- **Privacy**: Only necessary data is sent to the API (name, grade, subject, duration)
- **Transparency**: Used model is documented

## Tech Stack

### Backend
- **Framework**: Django 6.0
- **Database**: SQLite (development), PostgreSQL (production)
- **Python**: 3.12+
- **Timezone**: Europe/Berlin (consistent across all components)

### Premium Features (AI)
- **LLM Integration**: OpenAI-compatible API
- **Configuration**: API keys via environment variables
- **Model**: Configurable (default: gpt-3.5-turbo)

### Frontend
- **Templates**: Django templates with modern, responsive design
- **Styling**: Inline CSS for easy maintenance

## Special Features

### 1. Intelligent Conflict Detection
- Considers not only lesson time but also travel times before and after the lesson
- Detects overlaps with other lessons and blocked times
- Visual highlighting of conflicts in the UI

### 2. Travel Time Integration
- Each lesson can have individual travel times before and after
- The "total time block" is automatically calculated
- Conflicts are detected based on the total time block

### 3. Income Calculation
- Flexible calculation by status (planned, taught, paid)
- Monthly and yearly overviews
- Breakdown by contracts/students

### 4. AI Integration with Privacy
- Minimal data collection: Only necessary information is sent to the LLM API
- No sensitive data (addresses, phone numbers, emails) is transmitted
- Generated plans are stored locally

### 5. Ethical-Christian Guidelines
- Transparency and honesty
- Order and clarity
- Service to the user
- No data misuse
- Responsible AI usage

## Challenges & Learnings

### Challenges

1. **Conflict Detection with Travel Times**
   - Problem: Travel times must be included in time block calculation
   - Solution: Central service function `LessonConflictService` calculates total time block including travel times

2. **Timezone Handling**
   - Problem: Consistent use of Europe/Berlin across all components
   - Solution: Django `TIME_ZONE` configured, all DateTime operations timezone-aware

3. **Modular Architecture**
   - Problem: Code files should not become too large (< 300-400 lines)
   - Solution: Clear separation into services, selectors, views, models

4. **AI Integration with Privacy**
   - Problem: Balance between functionality and privacy
   - Solution: Minimal data collection, clear documentation, Human-in-the-Loop

### Learnings

- **Django Best Practices**: Clear app structure, service layer for business logic
- **Timezone Handling**: Consistent use of timezone-aware datetime objects
- **Modularity**: Small, focused files facilitate maintainability
- **Ethics in Development**: Integrate ethical principles from the start

## Demo

### Load Demo Data

```bash
cd backend
python manage.py seed_demo_data
```

**Demo Login:**
- Username: `demo_premium`
- Password: `demo123`

### Demo Scenario

The demo shows:
- 3 students with different profiles
- Contracts (private and via institute)
- Multiple lessons
- **One conflict** between two lessons (for demonstration)
- Blocked times (e.g., university lecture)
- Premium user with AI-generated lesson plan

## Setup

See `README.md` for detailed installation instructions.

Summary:
1. Clone repository
2. Create virtual environment
3. Install dependencies
4. Migrate database
5. Load demo data (optional)
6. Start server

## Validation

A validation script is available:

```bash
./scripts/validate.sh
```

Checks: Django Check, Tests, TODO comments, Debug output, Documentation.

## Documentation

- **README.md**: Project overview, setup, features
- **docs/ARCHITECTURE.md**: Technical architecture, domain model, use cases
- **docs/ETHICS.md**: Ethical-Christian guidelines, privacy
- **docs/API.md**: API documentation
- **docs/PHASES.md**: Development phases
- **docs/CHECKPOINTS.md**: Progress log

## Future Vision

- Mobile App (React Native)
- Calendar Integration (iCal, Google Calendar)
- PDF Upload for order confirmations with data extraction
- Extended AI features (e.g., adaptation to learning progress)
- Multi-User Support (multiple tutors in one instance)

## Team

Developed as part of the Teca-Hacks Hackathon.

## License

This project is licensed under the Apache License 2.0 – see [LICENSE](../LICENSE) for details.

Copyright (c) 2025 Andreas Eirich
