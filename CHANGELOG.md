# Changelog – TutorFlow

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.9.0] - 2025-12-04

### Changed
- **Documentation**: All public-facing documentation (README, ARCHITECTURE, PHASES, CHECKPOINTS, ETHICS, DEPLOYMENT, DEVPOST) rewritten in English for jury-readiness
- **README**: Enhanced screenshot section with placeholder structure and 2-minute demo tour
- **ARCHITECTURE.md**: German section headers translated to English

### Added
- **Linting & Formatting**: Added `ruff` and `black` configuration in `pyproject.toml`
- **Linting Script**: Created `scripts/lint.sh` for automated code quality checks
- **CI/CD**: Added GitHub Actions workflow (`.github/workflows/ci.yml`) for automated testing and linting
- **Screenshot Placeholders**: Created `docs/images/` directory structure for screenshots

### Technical Debt
- Code quality improvements: Linting configuration ensures consistent code style
- CI pipeline: Automated quality checks on every push/pull request

## [0.8.9] - 2025-12-04

### Fixed
- **Income calculation consistent with billing system**:
  - IncomeSelector now uses the same calculation logic as InvoiceService
  - Formula: `units = lesson_duration_minutes / contract_unit_duration_minutes`, `amount = units * hourly_rate`
  - For lessons in invoices: amounts are taken from InvoiceItems (Single Source of Truth)
  - All calculation methods updated: `get_monthly_income`, `get_income_by_status`, `get_billing_status`, `get_monthly_planned_vs_actual`
- **Correct Euro formatting**:
  - New template filter `|euro` for currency formatting
  - Format: 2 decimal places, German notation (comma, thousand separators)
  - Example: `Decimal('90')` → "90,00 €", `Decimal('1234.56')` → "1.234,56 €"
  - All amounts in income overview and dashboard now use `|euro` filter
- **Billing status logic corrected**:
  - `get_billing_status()`: Billed lessons regardless of status (from InvoiceItems)
  - Not billed: Lessons with status TAUGHT without InvoiceItem

### Tests
- 8 new tests for income calculation and formatting
- Tests verify: calculation matches InvoiceService, amounts from InvoiceItems are used, formatting correct

---

## [0.8.8] - 2025-12-04

### Fixed
- **Status reset when deleting invoices**:
  - `Invoice.delete()` method overridden to automatically reset all lessons with status PAID to TAUGHT
  - Works both with direct `invoice.delete()` and via `InvoiceService.delete_invoice()`
  - Simplified logic: Since a lesson can only appear in one invoice, no check for other invoices is needed
  - `InvoiceService.delete_invoice()` simplified, as logic is now in the model

### Tests
- 5 new tests for status reset when deleting
- Tests for: single lesson, multiple lessons, direct delete() call, only PAID lessons are reset

---

## [0.8.7] - 2025-12-04

### Added
- **Management command `reset_paid_lessons`**:
  - Resets all lessons with status PAID to TAUGHT
  - Option `--delete-invoices`: Also deletes associated invoices and InvoiceItems
  - Option `--dry-run`: Only shows what would be changed without making changes
  - Usage: `python manage.py reset_paid_lessons [--delete-invoices] [--dry-run]`
  - Useful for bulk operations or corrections

### Tests
- 4 tests for `reset_paid_lessons` command
- Tests for: status reset, deleting invoices, dry-run, no PAID lessons

---

## [0.8.6] - 2025-12-04

### Changed
- **Automatic invoice creation**:
  - No more manual individual selection of lessons (no checkbox selection)
  - All TAUGHT lessons in the period are automatically included in the invoice
  - Form only shows period and optional contract filter
  - Preview shows all available lessons that are automatically included
- **Restriction: One lesson only in one invoice**:
  - `get_billable_lessons()` excludes lessons that are already in an InvoiceItem
  - Technically via `exclude(invoice_items__isnull=False)`
  - A lesson cannot appear in two invoices

### Fixed
- **Only TAUGHT lessons billable**:
  - `get_billable_lessons()` only filters lessons with status TAUGHT
  - Lessons with status PLANNED or PAID are excluded
  - `create_invoice_from_lessons()` automatically uses `get_billable_lessons()`

### Tests
- 6 new tests for automatic invoice creation
- Tests for: only TAUGHT lessons, automatic selection of all lessons, no double assignment, status transitions

---

## [0.8.5] - 2025-12-04

### Fixed
- **Invoice calculation corrected**:
  - Calculation now based on units instead of hours
  - Formula: `units = lesson_duration_minutes / contract_unit_duration_minutes`, `amount = units * hourly_rate`
  - Example: 90 min at 45 min/unit and 12€/unit → 24€ (instead of previous hour calculation)
  - Total amount is the sum of all InvoiceItems

### Added
- **Status transitions for invoices**:
  - Lessons are automatically set to PAID when creating an invoice
  - Lessons are reset to TAUGHT when deleting an invoice (only if not in other invoices)
- **Invoices deletable**:
  - InvoiceDeleteView with confirmation page
  - Delete button in invoice detail view
  - Safe delete view (POST only, CSRF)

### Tests
- 5 new tests for invoice calculation and status transitions
- Tests for correct unit calculation (90 min / 45 min = 2 units)
- Tests for status transitions TAUGHT → PAID and PAID → TAUGHT
- Tests for correct handling of lessons in multiple invoices

---

## [0.8.4] - 2025-12-04

### Added
- **Extended recurrence patterns for recurring lessons**:
  - `recurrence_type` field in RecurringLesson (weekly/biweekly/monthly)
  - Weekly: as before, every week on marked weekdays
  - Every 2 weeks: every second week on marked weekdays
  - Monthly: every month on the same calendar day, if that day is a selected weekday
  - RecurringLessonService supports all three recurrence types
  - Form extended with recurrence type selection with explanations

### Tests
- 6 tests for various recurrence patterns (weekly, biweekly, monthly)
- Tests for automatic status setting for all recurrence types

---

## [0.8.3] - 2025-12-04

### Added
- **Conflict detail view**: 
  - ConflictDetailView shows all colliding lessons and blocked times
  - Clickable "Details" link in calendar for conflicts
  - Clear list with date, time, student, location and edit links
- **Lesson detail view**:
  - LessonDetailView with complete lesson information
  - "Conflicts" section shows all colliding lessons
  - Links to edit colliding lessons

### Changed
- **Calendar shows all lessons**: 
  - Filtering for past lessons removed
  - Past and future lessons are displayed
  - Past lessons visually grayed out (opacity: 0.7), but clickable
  - All lessons are editable

### Tests
- 4 tests for conflict details and calendar with past lessons

---

## [0.8.2] - 2025-12-04

### Fixed
- **Calendar month display**: CalendarView now uses exclusively year/month from URL parameters
  - Central variable `current_month_date = date(year, month, 1)` for all calculations
  - Month name (month_label) is correctly derived from displayed month
  - No more use of 'today' for month calculation
  - Template uses month_label instead of month_names slice
  - CreateView uses year/month from request as fallback for initial date

### Tests
- 3 new tests for calendar month display (including December test)

---

## [0.8.1] - 2025-12-04

### Changed
- **Status automation for all lesson creations**:
  - RecurringLessonService now uses LessonStatusService for automatic status setting
  - Lessons from recurring lessons automatically get correct status (past → TAUGHT, future → PLANNED)
  - Removed: Hard-set status 'planned' for recurring lessons
- **Status no longer manually selectable**:
  - Status field removed from LessonForm (only automatically set)
  - Status is no longer displayed in normal lesson form
  - Only automatic mechanism decides status when saving
- **Calendar date synchronization**:
  - Month name in calendar corresponds to displayed month (year/month parameter)
  - Default date in create form corresponds to clicked day (date parameter)
  - Redirect after create/update leads back to correct month (year/month from request)

### Tests
- 6 new tests for status automation for recurring lessons and manual creation
- 3 tests for calendar date synchronization

### Documentation
- ARCHITECTURE.md: Status automation for all lesson creations documented
- ARCHITECTURE.md: Note that status is not manually selectable in form
- README.md: Automatic status management mentioned

---

## [0.8.0] - 2025-12-04

### Added
- **LessonStatusService**: Automatic status setting for lessons
  - Past lessons (end_datetime < now) with status PLANNED → TAUGHT
  - Future lessons without status → PLANNED
  - PAID/CANCELLED are not overwritten
  - Integration in LessonCreateView and LessonUpdateView
  - bulk_update_past_lessons() for batch updates
- **Billing system**: Billing system with invoices
  - Invoice and InvoiceItem models
  - InvoiceService for billing workflow
  - UI for selecting lessons and creating invoices
  - InvoiceDocumentService for HTML document generation
  - Lessons are set to status PAID after invoice assignment
- **Extended financial view**:
  - Distinction between billed and unbilled lessons
  - get_billing_status() in IncomeSelector
  - Display in IncomeOverviewView

### Tests
- 5 tests for LessonStatusService (past/future lessons, PAID/CANCELLED protection, bulk_update)
- 5 tests for billing (Invoice model, InvoiceService, InvoiceItems persistence)

### Documentation
- ARCHITECTURE.md: LessonStatusService, Invoice/InvoiceItem, InvoiceService, InvoiceDocumentService documented
- ARCHITECTURE.md: Billing workflow described
- README.md: Automatic status management and billing system mentioned

---

## [0.7.1] - 2025-12-04

### Changed
- **Calendar as central UI**: Calendar is now the primary interface for lesson management
  - Lesson list view removed from navigation (endpoints remain for API/debugging)
  - Click on day in calendar opens form to create with pre-filled date
  - Click on existing lesson opens edit form
  - Redirect back to calendar after create/update
- **Calendar shows only future lessons**: 
  - Lessons in the past are no longer displayed in the calendar
  - Blocked times in the past are also hidden
  - Financial/income views continue to show all lessons (including past)
- **Recurring lessons better integrated**:
  - Button "Create recurring lesson" in calendar header
  - Link "Create recurring lesson" on contract detail page
  - Automatic generation of lessons after creating a RecurringLesson
  - Redirect to calendar after generation
  - Note in RecurringLesson form explains functionality

### Tests
- 3 new tests for calendar filtering (past lessons are hidden)
- Tests for calendar integration (create with date parameter, redirect)

### Documentation
- ARCHITECTURE.md: Calendar as central UI documented
- README.md: Calendar view and recurring lessons mentioned
- API.md: Calendar endpoints documented

---

## [0.7.0] - 2025-12-04

### Added
- **RecurringLesson model**: New entity for repeating lessons (recurring lessons)
  - Weekday selection (Mon-Sun as boolean fields)
  - Period (start_date, end_date)
  - Automatic generation of lessons over a period
- **RecurringLessonService**: Service for generating lessons from recurring lessons
  - Generates lessons for all activated weekdays in the period
  - Skips already existing lessons
  - Optionally checks conflicts
  - Preview function without saving
- **Calendar view**: Monthly calendar for lessons and blocked times
  - CalendarView with month grid (7 columns: Mon-Sun)
  - Display of lessons with time and student
  - Conflict marking
  - Display of blocked times
  - Navigation between months
- **UI for recurring lessons**: CRUD views and templates
  - List, detail, form, delete
  - Button to generate lessons from series
  - Preview of lessons to be created

### Tests
- 8 new tests for RecurringLesson, RecurringLessonService and CalendarService
- Tests for single/multiple weekdays, contract boundaries, conflicts, calendar grouping

### Documentation
- ARCHITECTURE.md: RecurringLesson and CalendarService documented
- API.md: Endpoints for recurring lessons and calendar added

---

## [0.6.2] - 2025-12-04

### Removed
- **Contract.planned_units_per_month**: Field completely removed
  - Migration created to remove field from database
  - Removed from ContractForm, templates and seed_demo_data
  - Planned units are managed exclusively via ContractMonthlyPlan

---

## [0.6.1] - 2025-12-04

### Fixed
- **Monthly contract planning**: Removal of limitation to current date
  - Planned units can now be recorded for all months between start_date and end_date
  - Regardless of whether the month is in the past or future
  - New helper function `iter_contract_months()` for consistent month generation
  - Correction of logic for deleting plans outside contract period

### Tests
- 5 new tests for future, past and overlapping contracts
- Tests explicitly check that no limitation to current date exists

### Documentation
- ARCHITECTURE.md: Clarification that monthly plans are generated for the entire contract period

---

## [0.6.0] - 2025-12-04

### Added
- **ContractMonthlyPlan model**: New entity for explicit monthly planning of planned units per contract
  - Allows uneven distribution over the year (e.g., more units during exam periods)
  - Unique constraint on (contract, year, month)
- **Monthly planning in contract views**: 
  - Formset integration for editing planned units per month
  - Automatic generation of month rows when creating/editing contracts
  - Handling of period changes (new months are added, old ones removed)
- **IncomeSelector extension**:
  - New method `get_monthly_planned_vs_actual()` for comparison of planned vs. actual
  - Calculation of planned_units, planned_amount, actual_units, actual_amount per month
- **Income overview extended**: 
  - Display of planned vs. actual units and income in monthly view
  - Difference calculation (difference_units, difference_amount)

### Changed
- `Contract.planned_units_per_month`: Marked as deprecated (use ContractMonthlyPlan)
- `IncomeOverviewView`: Extended with planned_vs_actual data
- `contract_form.html`: Template extended with formset for monthly planning

### Tests
- 8 new tests for ContractMonthlyPlan, generation of monthly plans and IncomeSelector comparison

### Documentation
- `docs/ARCHITECTURE.md`: ContractMonthlyPlan documented, IncomeSelector extended
- Planned units are no longer evenly distributed, but explicitly recorded per month

### Phase
- New functionality: Monthly contract planning

---

## [0.5.0] - 2025-12-04

### Added
- UI/UX polishing: Improved templates with consistent navigation, clear conflict display, premium badges
- Demo/Seed data: Management command `seed_demo_data` for demo scenario
  - 3 demo students with different profiles
  - Associated contracts (private and via institute)
  - Multiple lessons (including conflict for demonstration)
  - Blocked times
  - 1 premium user with generated lesson plan
- Validation script: `scripts/validate.sh` for automatic checks (Django Check, Tests, TODO comments, Debug output)
- Documentation: DEVPOST.md created for hackathon submission

### Changed
- README.md: Revised with demo data instructions, validation script, improved feature description
- docs/ETHICS.md: Extended with section on demo data and privacy
- docs/PHASES.md: Phase 5 marked as completed
- docs/CHECKPOINTS.md: Checkpoint 5 added
- Templates: Improved display of conflicts, premium badges, consistent buttons

### Phase
- Phase 5 – Polishing, Validation & Hackathon Refinement completed

---

## [0.4.0] - 2025-12-04

### Added
- **Premium features**:
  - `apps.core.utils.is_premium_user()` - Utility function for premium checks
  - Premium gating in views and templates
  - UI notices for non-premium users
- **AI app** (`apps.ai`):
  - `apps.ai.client.LLMClient` - Low-level client for LLM API communication (OpenAI-compatible)
  - `apps.ai.prompts` - Prompt building for structured lesson plans
  - `apps.ai.services.LessonPlanService` - High-level service for lesson plan generation
- **LessonPlan generation**:
  - Context collection (student, lesson, previous lessons)
  - Structured prompt building with system and user prompts
  - LLM API integration with error handling
  - Storage as LessonPlan model with metadata (model name, creation timestamp)
- **UI integration**:
  - Button "Generate lesson plan with AI" in lesson detail view (premium only)
  - Display of generated plans
  - Premium notice for non-premium users
- **Configuration**:
  - LLM settings via environment variables (LLM_API_KEY, LLM_API_BASE_URL, LLM_MODEL_NAME, LLM_TIMEOUT_SECONDS)
  - No secrets in code
- **Tests**:
  - 12 tests for premium gating, prompt building, services and client
  - Mock tests for LLM calls (no real API calls in tests)
  - Error scenarios tested
- **Dependencies**:
  - `requests` for HTTP API communication

### Changed
- `backend/tutorflow/settings.py` - LLM configuration added
- `apps/lessons/views.py` - LessonDetailView extended with lesson plan display
- `apps/lessons/templates/lessons/lesson_detail.html` - Template for lesson plan generation
- `docs/ARCHITECTURE.md` - AI architecture documented
- `docs/ETHICS.md` - AI usage, privacy and Human-in-the-Loop documented
- `docs/API.md` - Premium endpoint documented
- `docs/PHASES.md` - Phase 4 marked as completed
- `docs/CHECKPOINTS.md` - Checkpoint 4 documented
- `requirements.txt` - requests added

### Phase
- Phase 4 – Premium & AI Features completed

---

## [0.3.0] - 2025-12-04

### Added
- **CRUD functions** for all core entities:
  - Student (List, Detail, Create, Update, Delete Views)
  - Contract (List, Detail, Create, Update, Delete Views)
  - Lesson (List, Detail, Create, Update, Delete, Month View)
  - BlockedTime (List, Detail, Create, Update, Delete Views)
  - Location (List, Detail, Create, Update, Delete Views)
- **Conflict detection**:
  - `apps.lessons.services.LessonConflictService` - Central service class for conflict detection
  - Time block calculation including travel times
  - Check for overlap with other lessons and blocked times
  - Conflict marking in Lesson model (`has_conflicts` property, `get_conflicts()` method)
- **Planning logic**:
  - `apps.lessons.services.LessonQueryService` - Service for lesson queries
  - Month view for lessons
  - Queries for today's and upcoming lessons
- **Income overview**:
  - Dashboard view with overview of today's/upcoming lessons and conflicts
  - IncomeOverview view with monthly/yearly view
  - Integration of IncomeSelector in views
- **Basic UI**:
  - Navigation between all areas
  - Basic templates for all CRUD operations
  - Dashboard template with conflict display
- **Tests**:
  - 7 new tests for conflict detection and services
  - Tests for time block calculation, conflicts with lessons and blocked times, queries

### Changed
- `apps.lessons.models.Lesson` - Extended with conflict detection methods
- `backend/tutorflow/urls.py` - URLs for all apps included
- `docs/ARCHITECTURE.md` - Conflict logic and income calculation documented
- `docs/API.md` - Implemented views documented
- `docs/PHASES.md` - Phase 3 marked as completed
- `docs/CHECKPOINTS.md` - Checkpoint 3 documented

### Phase
- Phase 3 – Core Features (Planning & Income) completed

---

## [0.2.1] - 2025-12-04

### Changed
- Correction of incorrect dates: All occurrences of `2025-01-27` in documentation were corrected to the correct date `2025-12-04` (Europe/Berlin)
- `docs/CHECKPOINTS.md` - Dates in Checkpoint 1 and 2 corrected
- `CHANGELOG.md` - Version dates corrected

---

## [0.2.0] - 2025-12-04

### Added
- Domain models implemented:
  - `apps.locations.Location` - Lesson location management with optional coordinates
  - `apps.students.Student` - Student management with contact data, school, subjects
  - `apps.contracts.Contract` - Contract management with fee, duration, period
  - `apps.lessons.Lesson` - Lesson planning with status tracking and travel times
  - `apps.blocked_times.BlockedTime` - Blocked time management
  - `apps.lesson_plans.LessonPlan` - AI-generated lesson plans
  - `apps.core.UserProfile` - User extension with premium flag
- `apps.core.selectors.IncomeSelector` - Service layer for income calculations
- Admin interfaces for all models
- Migrations for all apps
- 14 unit tests for models and services

### Changed
- `docs/ARCHITECTURE.md` - Data model details added
- `docs/PHASES.md` - Phase 2 marked as completed
- `docs/CHECKPOINTS.md` - Checkpoint 2 documented
- `backend/tutorflow/settings.py` - All apps registered in INSTALLED_APPS

### Phase
- Phase 2 – Domain Data Model & Migrations completed

---

## [0.1.0] - 2025-12-04

### Added
- Initial project setup
- Django 5.2.9 project initialized
- Basic repository structure created:
  - `backend/` - Django project
  - `backend/apps/` - Placeholder for feature apps
  - `backend/config/` - Project configuration
  - `docs/` - Documentation
  - `scripts/` - Validation scripts
- Documentation created:
  - `README.md` - Project description and setup instructions
  - `docs/ARCHITECTURE.md` - Architecture overview
  - `docs/ETHICS.md` - Ethical-Christian guidelines
  - `docs/PHASES.md` - Development phases overview
  - `docs/CHECKPOINTS.md` - Progress log
  - `docs/API.md` - API documentation (placeholder)
- `requirements.txt` with Django 5.2.9
- Virtual environment setup
- `CHANGELOG.md` - This file

### Phase
- Phase 1 – Project Setup & Architecture Foundations started
