"""
Tests für ContractMonthlyPlan und monatliche Planung.
"""
from django.test import TestCase
from datetime import date
from decimal import Decimal
from apps.students.models import Student
from apps.contracts.models import Contract, ContractMonthlyPlan
from apps.contracts.formsets import generate_monthly_plans_for_contract
from apps.core.selectors import IncomeSelector
from apps.lessons.models import Lesson


class ContractMonthlyPlanTest(TestCase):
    """Tests für ContractMonthlyPlan Model."""
    
    def setUp(self):
        self.student = Student.objects.create(
            first_name="Max",
            last_name="Mustermann",
            email="max@example.com"
        )
        self.contract = Contract.objects.create(
            student=self.student,
            hourly_rate=Decimal('25.00'),
            unit_duration_minutes=60,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 3, 31),
            is_active=True
        )
    
    def test_create_monthly_plan(self):
        """Test: Erstellen eines monatlichen Plans."""
        plan = ContractMonthlyPlan.objects.create(
            contract=self.contract,
            year=2025,
            month=1,
            planned_units=8
        )
        self.assertEqual(plan.contract, self.contract)
        self.assertEqual(plan.year, 2025)
        self.assertEqual(plan.month, 1)
        self.assertEqual(plan.planned_units, 8)
    
    def test_unique_together_constraint(self):
        """Test: unique_together Constraint verhindert doppelte Einträge."""
        ContractMonthlyPlan.objects.create(
            contract=self.contract,
            year=2025,
            month=1,
            planned_units=8
        )
        # Zweiter Eintrag für denselben Monat sollte fehlschlagen
        with self.assertRaises(Exception):
            ContractMonthlyPlan.objects.create(
                contract=self.contract,
                year=2025,
                month=1,
                planned_units=10
            )


class GenerateMonthlyPlansTest(TestCase):
    """Tests für generate_monthly_plans_for_contract."""
    
    def setUp(self):
        self.student = Student.objects.create(
            first_name="Anna",
            last_name="Schmidt",
            email="anna@example.com"
        )
    
    def test_generate_plans_for_date_range(self):
        """Test: Generierung von Plänen für einen Zeitraum."""
        contract = Contract.objects.create(
            student=self.student,
            hourly_rate=Decimal('30.00'),
            start_date=date(2025, 1, 15),
            end_date=date(2025, 3, 15),
            is_active=True
        )
        
        plans = generate_monthly_plans_for_contract(contract)
        
        # Sollte Pläne für Januar, Februar, März erstellen
        self.assertEqual(len(plans), 3)
        self.assertEqual(plans[0].year, 2025)
        self.assertEqual(plans[0].month, 1)
        self.assertEqual(plans[1].month, 2)
        self.assertEqual(plans[2].month, 3)
    
    def test_generate_plans_unlimited_contract(self):
        """Test: Generierung für unbefristeten Vertrag (1 Jahr voraus)."""
        contract = Contract.objects.create(
            student=self.student,
            hourly_rate=Decimal('25.00'),
            start_date=date(2025, 1, 1),
            end_date=None,
            is_active=True
        )
        
        plans = generate_monthly_plans_for_contract(contract)
        
        # Sollte mindestens 12 Monate generieren
        self.assertGreaterEqual(len(plans), 12)
    
    def test_generate_plans_preserves_existing(self):
        """Test: Vorhandene Pläne werden nicht überschrieben."""
        contract = Contract.objects.create(
            student=self.student,
            hourly_rate=Decimal('25.00'),
            start_date=date(2025, 1, 1),
            end_date=date(2025, 2, 28),
            is_active=True
        )
        
        # Erstelle manuell einen Plan
        existing_plan = ContractMonthlyPlan.objects.create(
            contract=contract,
            year=2025,
            month=1,
            planned_units=10
        )
        
        # Generiere Pläne erneut
        plans = generate_monthly_plans_for_contract(contract)
        
        # Existierender Plan sollte erhalten bleiben
        existing_plan.refresh_from_db()
        self.assertEqual(existing_plan.planned_units, 10)


class IncomeSelectorPlannedVsActualTest(TestCase):
    """Tests für IncomeSelector mit geplanten vs. tatsächlichen Einheiten."""
    
    def setUp(self):
        self.student = Student.objects.create(
            first_name="Tom",
            last_name="Weber",
            email="tom@example.com"
        )
        self.contract = Contract.objects.create(
            student=self.student,
            hourly_rate=Decimal('28.00'),
            unit_duration_minutes=60,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 12, 31),
            is_active=True
        )
    
    def test_planned_vs_actual_month_with_plan(self):
        """Test: Vergleich geplant vs. tatsächlich mit Plan-Einträgen."""
        # Erstelle Plan-Einträge
        ContractMonthlyPlan.objects.create(
            contract=self.contract,
            year=2025,
            month=1,
            planned_units=8
        )
        ContractMonthlyPlan.objects.create(
            contract=self.contract,
            year=2025,
            month=2,
            planned_units=4
        )
        
        # Erstelle tatsächliche Lessons
        Lesson.objects.create(
            contract=self.contract,
            date=date(2025, 1, 10),
            start_time='14:00',
            duration_minutes=60,
            status='paid'
        )
        Lesson.objects.create(
            contract=self.contract,
            date=date(2025, 1, 20),
            start_time='15:00',
            duration_minutes=60,
            status='paid'
        )
        # Februar: mehr tatsächliche als geplante
        Lesson.objects.create(
            contract=self.contract,
            date=date(2025, 2, 5),
            start_time='14:00',
            duration_minutes=60,
            status='paid'
        )
        Lesson.objects.create(
            contract=self.contract,
            date=date(2025, 2, 12),
            start_time='15:00',
            duration_minutes=60,
            status='paid'
        )
        Lesson.objects.create(
            contract=self.contract,
            date=date(2025, 2, 19),
            start_time='16:00',
            duration_minutes=60,
            status='paid'
        )
        
        # Test Januar: geplant 8, tatsächlich 2
        result_jan = IncomeSelector.get_monthly_planned_vs_actual(2025, 1)
        self.assertEqual(result_jan['planned_units'], 8)
        self.assertEqual(result_jan['actual_units'], 2)
        self.assertEqual(result_jan['difference_units'], -6)
        
        # Test Februar: geplant 4, tatsächlich 3
        result_feb = IncomeSelector.get_monthly_planned_vs_actual(2025, 2)
        self.assertEqual(result_feb['planned_units'], 4)
        self.assertEqual(result_feb['actual_units'], 3)
        self.assertEqual(result_feb['difference_units'], -1)
    
    def test_planned_vs_actual_month_without_plan(self):
        """Test: Monat ohne Plan-Einträge."""
        # Keine Plan-Einträge für März
        Lesson.objects.create(
            contract=self.contract,
            date=date(2025, 3, 10),
            start_time='14:00',
            duration_minutes=60,
            status='paid'
        )
        
        result = IncomeSelector.get_monthly_planned_vs_actual(2025, 3)
        self.assertEqual(result['planned_units'], 0)
        self.assertEqual(result['actual_units'], 1)
        self.assertEqual(result['difference_units'], 1)
        self.assertEqual(result['planned_amount'], Decimal('0.00'))
        self.assertGreater(result['actual_amount'], Decimal('0.00'))
    
    def test_planned_amount_calculation(self):
        """Test: Berechnung des geplanten Betrags."""
        ContractMonthlyPlan.objects.create(
            contract=self.contract,
            year=2025,
            month=1,
            planned_units=10
        )
        
        result = IncomeSelector.get_monthly_planned_vs_actual(2025, 1)
        # 10 Einheiten * 28€ * 1 Stunde = 280€
        expected = Decimal('28.00') * Decimal('10')
        self.assertEqual(result['planned_amount'], expected)

