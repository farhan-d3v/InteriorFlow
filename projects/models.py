
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Project(models.Model):
    STATUS_CHOICES = [
        ("Planning", "Planning"),
        ("Ongoing", "Ongoing"),
        ("On Hold", "On Hold"),
        ("Completed", "Completed"),
    ]

    name = models.CharField(max_length=200)
    client = models.CharField(max_length=150)
    location = models.CharField(max_length=200)
    description = models.TextField()

    start_date = models.DateField()
    target_end_date = models.DateField()

    estimated_budget = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Planning",
    )

    progress = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class SiteUpdate(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="site_updates",
    )
    title = models.CharField(max_length=200)
    notes = models.TextField()
    progress = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    posted_by = models.CharField(max_length=150)
    update_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-update_date", "-created_at"]

    def __str__(self):
        return self.title


class Worker(models.Model):
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=100)
    contact = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.name} - {self.role}"


class ProjectWorker(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="assignments",
    )
    worker = models.ForeignKey(
        Worker,
        on_delete=models.CASCADE,
        related_name="assignments",
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project", "worker"],
                name="unique_project_worker",
            )
        ]

    def __str__(self):
        return f"{self.worker} - {self.project}"


class Expense(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="expenses",
    )
    description = models.CharField(max_length=200)
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    expense_date = models.DateField()

    def __str__(self):
        return f"{self.description} - {self.amount}"
