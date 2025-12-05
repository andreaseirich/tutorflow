# Development Phases – TutorFlow

## Overview

The TutorFlow project is developed in several phases to ensure structured and controlled development.

## Phase 1 – Project Setup & Architecture Foundations

**Status**: ✅ Started

**Goal**: Initialize repository, create Django base project, define first app structure, write basic documentation.

**Acceptance Criteria**:
- ✅ Django project functional
- ✅ Basic folder structure present
- ✅ README, ARCHITECTURE, ETHICS, CHANGELOG created and filled
- ✅ PHASES.md and CHECKPOINTS.md created

**Tests**:
- Start dev server
- At least 1 simple smoke test (e.g., `python manage.py check`)

**Progress**:
- Basic structure created
- Django project initialized
- Documentation created

---

## Phase 2 – Domain Data Model & Migrations

**Status**: ✅ Completed

**Goal**: Define and migrate central models (Student, Contract, Lesson, BlockedTime, Location, User extension).

**Acceptance Criteria**:
- ✅ All models defined (7 models: Location, Student, Contract, Lesson, BlockedTime, LessonPlan, UserProfile)
- ✅ Migrations created and executed successfully
- ✅ ARCHITECTURE.md updated with data model details
- ✅ IncomeSelector implemented as service layer

**Tests**:
- ✅ 14 unit tests implemented and successful
- ✅ Tests for model logic (CRUD, relationships, income calculation)

**Progress**:
- All 7 Django apps created (locations, students, contracts, lessons, blocked_times, lesson_plans, core)
- Models with correct fields, relationships, and meta options
- Admin interfaces for all models
- IncomeSelector with monthly/yearly income calculation

---

## Phase 3 – Core Features (Planning & Income)

**Status**: ✅ Completed

**Goal**: CRUD for students, contracts, lessons, blocked times; month view + income calculations; simple conflict detection.

**Acceptance Criteria**:
- ✅ Complete CRUD views for all core entities (Student, Contract, Lesson, BlockedTime, Location)
- ✅ Conflict detection with travel times and blocked times implemented
- ✅ Month view & income overview functional
- ✅ Dashboard with overview of today's/upcoming lessons and conflicts
- ✅ Basic UI with navigation

**Tests**:
- ✅ 7 new tests for conflict detection and services
- ✅ Tests for planning logic, conflict detection including travel times and blocked times
- ✅ All tests run successfully

**Progress**:
- LessonConflictService implemented for conflict detection
- LessonQueryService implemented for queries
- CRUD views for all entities with Django class-based views
- Dashboard and income overview implemented
- Basic templates created

---

## Phase 4 – Premium & AI Features

**Status**: ✅ Completed

**Goal**: Premium flag on user, integration of LLM API for lesson plan creation, clean separation of base and premium features.

**Acceptance Criteria**:
- ✅ Premium flag fully integrated (`apps.core.utils.is_premium_user()`)
- ✅ AI lesson plan can be generated for premium users
- ✅ LLM integration encapsulated (client/prompts/services)
- ✅ API keys configured via environment variables
- ✅ Error handling for LLM calls implemented
- ✅ ETHICS.md contains notes on AI usage and privacy

**Tests**:
- ✅ 12 tests for premium gating, prompt building, service layer and client
- ✅ Mock tests for AI calls (no real API calls in tests)
- ✅ Error scenarios tested

**Progress**:
- AI app created (`apps.ai`) with modular structure
- LLMClient for API communication (OpenAI-compatible)
- Prompt building for structured lesson plans
- LessonPlanService for high-level generation
- UI integration in lesson detail view
- Premium gating in views and templates

---

## Phase 5 – Polishing, Validation & Hackathon Refinement

**Status**: ✅ Completed

**Goal**: Improve UI, integrate demo data, finalize documentation, stabilize tests, trim everything for hackathon submission.

**Acceptance Criteria**:
- ✅ UI is simple but clear and demo-ready
- ✅ Reproducible demo scenario (seed data) available
- ✅ Validation script exists and runs
- ✅ README, ARCHITECTURE, ETHICS, API, PHASES, CHECKPOINTS, DEVPOST are current and consistent
- ✅ Tests run without errors
- ✅ Codebase appears clean, structured, and comprehensible for hackathon jurors

**Tests**:
- ✅ Validation script checks Django Check, Tests, TODO comments, Debug output
- ✅ All tests run successfully

**Progress**:
- UI/UX polishing: Templates improved, consistent navigation, clear conflict display, premium badges
- Demo/Seed data: Management command `seed_demo_data` created with 3 students, contracts, lessons (including conflict), blocked times, premium user with LessonPlan
- Validation script: `scripts/validate.sh` created for automatic checks
- Documentation finalized: README revised, ETHICS extended (demo data), DEVPOST.md created
- Code cleanup: No TODOs, no debug output, clean structure

---

## Phase 6 – Monthly Contract Planning

**Status**: ✅ Completed

**Goal**: Explicit monthly planning of planned units per contract instead of equal distribution.

**Acceptance Criteria**:
- ✅ ContractMonthlyPlan model implemented
- ✅ Formset integration for monthly planning in contract views
- ✅ Automatic generation of month rows when creating/editing
- ✅ IncomeSelector extended with planned vs. actual comparison
- ✅ Income overview shows planned vs. actual
- ✅ Tests for all new functions

**Tests**:
- ✅ 8 tests for ContractMonthlyPlan, generation and IncomeSelector comparison
- ✅ All tests run successfully

**Progress**:
- ContractMonthlyPlan model with unique_together constraint
- Formsets for monthly planning integrated
- Automatic generation and cleanup of monthly plans
- IncomeSelector extended with get_monthly_planned_vs_actual()
- UI extended with planned vs. actual comparison

---

## Phase 7 – Recurring Lessons and Calendar View

**Status**: ✅ Completed

**Goal**: Support for repeating lessons (recurring lessons) and monthly calendar view.

**Acceptance Criteria**:
- ✅ RecurringLesson model implemented
- ✅ RecurringLessonService for generating lessons
- ✅ UI for recurring lessons (CRUD)
- ✅ Calendar view with lessons and blocked times
- ✅ Tests for recurring lessons and calendar

**Tests**:
- ✅ 8 tests for RecurringLesson, service and calendar
- ✅ All tests run successfully

**Progress**:
- RecurringLesson model with weekday selection
- RecurringLessonService for automatic generation
- CalendarService for month view
- CalendarView with HTML calendar grid
- Integration in navigation and existing logic

---

## Phase Transitions

Before transitioning to a new phase:
1. All acceptance criteria of the current phase fulfilled
2. Tests run successfully
3. Documentation updated
4. Git commits created
5. Checkpoint documented in CHECKPOINTS.md
