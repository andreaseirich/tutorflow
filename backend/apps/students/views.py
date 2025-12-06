"""
Views für Student-CRUD-Operationen.
"""

from apps.students.forms import StudentForm
from apps.students.models import Student
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView


class StudentListView(ListView):
    """Liste aller Schüler."""

    model = Student
    template_name = "students/student_list.html"
    context_object_name = "students"
    paginate_by = 20


class StudentDetailView(DetailView):
    """Detailansicht eines Schülers."""

    model = Student
    template_name = "students/student_detail.html"
    context_object_name = "student"


class StudentCreateView(CreateView):
    """Neuen Schüler erstellen."""

    model = Student
    form_class = StudentForm
    template_name = "students/student_form.html"
    success_url = reverse_lazy("students:list")

    def form_valid(self, form):
        messages.success(self.request, "Schüler erfolgreich erstellt.")
        return super().form_valid(form)


class StudentUpdateView(UpdateView):
    """Schüler bearbeiten."""

    model = Student
    form_class = StudentForm
    template_name = "students/student_form.html"
    success_url = reverse_lazy("students:list")

    def form_valid(self, form):
        messages.success(self.request, "Schüler erfolgreich aktualisiert.")
        return super().form_valid(form)


class StudentDeleteView(DeleteView):
    """Schüler löschen."""

    model = Student
    template_name = "students/student_confirm_delete.html"
    success_url = reverse_lazy("students:list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Schüler erfolgreich gelöscht.")
        return super().delete(request, *args, **kwargs)
