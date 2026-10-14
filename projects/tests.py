
from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse

from .models import Project, Task


class ProjectProgressTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name="Test Interior Project",
            client="Test Client",
            location="Kochi",
            start_date=date.today(),
            target_end_date=date.today() + timedelta(days=30),
            estimated_budget=100000,
            status="Ongoing",
        )

    def test_project_without_tasks_has_zero_progress(self):
        self.assertEqual(self.project.calculate_progress(), 0)

    def test_weighted_task_progress(self):
        Task.objects.create(
            project=self.project,
            name="Flooring",
            weight=60,
            progress=100,
        )
        Task.objects.create(
            project=self.project,
            name="Electrical Work",
            weight=40,
            progress=25,
        )

        self.assertEqual(self.project.calculate_progress(), 70)

    def test_update_progress_saves_calculated_value(self):
        Task.objects.create(
            project=self.project,
            name="Painting",
            weight=100,
            progress=50,
        )

        self.project.update_progress()
        self.project.refresh_from_db()

        self.assertEqual(self.project.progress, 50)
