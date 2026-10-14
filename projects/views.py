
from django.contrib import messages
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (
    ProjectForm,
    SiteUpdateForm,
    WorkerForm,
    AssignWorkerForm,
    ExpenseForm,
    TaskForm
)
from .models import Project, SiteUpdate, Worker, ProjectWorker, Expense,Task
from .models import Project, SiteUpdate


def dashboard(request):
    today = timezone.localdate()
    projects = Project.objects.all()

    context = {
        "total_projects": projects.count(),
        "ongoing_projects": projects.filter(status="Ongoing").count(),
        "completed_projects": projects.filter(status="Completed").count(),
        "overdue_projects": projects.filter(
            target_end_date__lt=today
        ).exclude(status="Completed").count(),
        "recent_projects": projects.order_by("-updated_at")[:5],
        "total_budget": projects.aggregate(
            total=Sum("estimated_budget")
        )["total"] or 0,
    }
    return render(request, "projects/dashboard.html", context)


def project_list(request):
    projects = Project.objects.all()
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "")
    sort = request.GET.get("sort", "recent")

    if query:
        projects = projects.filter(
            Q(name__icontains=query)
            | Q(client__icontains=query)
            | Q(location__icontains=query)
        )

    if status in dict(Project.STATUS_CHOICES):
        projects = projects.filter(status=status)

    if sort == "deadline":
        projects = projects.order_by("target_end_date")
    else:
        projects = projects.order_by("-updated_at")

    return render(request, "projects/project_list.html", {
        "projects": projects,
        "query": query,
        "selected_status": status,
        "selected_sort": sort,
        "status_choices": Project.STATUS_CHOICES,
    })

def project_create(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        if form.cleaned_data["status"] == "Completed":
            form.add_error(
                "status",
                "A project can only be completed when its tasks reach 100% progress."
            )
        else:
            project = form.save()
            project.update_progress()

            messages.success(request, "Project created successfully.")
            return redirect("project_list")

    return render(request, "projects/project_form.html", {
        "form": form,
        "page_title": "Create Project",
    })

def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectForm(request.POST or None, instance=project)

    if request.method == "POST" and form.is_valid():
        calculated_progress = project.calculate_progress()

        if (
            form.cleaned_data["status"] == "Completed"
            and calculated_progress < 100
        ):
            form.add_error(
                "status",
                "A project can only be completed when its tasks reach 100% progress."
            )
        else:
            project = form.save()
            project.update_progress()

            messages.success(request, "Project updated successfully.")
            return redirect("project_detail", pk=project.pk)

    return render(request, "projects/project_form.html", {
        "form": form,
        "page_title": "Edit Project",
    })

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)

    actual_spending = project.expenses.aggregate(
        total=Sum("amount")
    )["total"] or 0

    return render(request, "projects/project_detail.html", {
        "project": project,
        "assign_form": AssignWorkerForm(),
        "actual_spending": actual_spending,
        "remaining_budget": project.estimated_budget - actual_spending,
    })



def site_update_create(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = SiteUpdateForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        site_update = form.save(commit=False)
        site_update.project = project

        # Save the overall progress as a historical snapshot.
        site_update.progress = project.progress
        site_update.save()

        messages.success(request, "Site update added successfully.")
        return redirect("project_detail", pk=project.pk)

    return render(request, "projects/site_update_form.html", {
        "form": form,
        "project": project,
    })



def worker_list(request):
    workers = Worker.objects.all().order_by("name")
    return render(request, "projects/worker_list.html", {
        "workers": workers,
    })


def worker_create(request):
    form = WorkerForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Team member added successfully.")
        return redirect("worker_list")

    return render(request, "projects/worker_form.html", {
        "form": form,
        "page_title": "Add Team Member",
    })


def assign_worker(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == "POST":
        form = AssignWorkerForm(request.POST)

        if form.is_valid():
            worker = form.cleaned_data["worker"]

            if ProjectWorker.objects.filter(
                project=project, worker=worker
            ).exists():
                messages.warning(
                    request,
                    "This team member is already assigned to the project.",
                )
            else:
                ProjectWorker.objects.create(
                    project=project,
                    worker=worker,
                )
                messages.success(request, "Team member assigned successfully.")

    return redirect("project_detail", pk=project.pk)


def remove_assignment(request, pk, assignment_id):
    project = get_object_or_404(Project, pk=pk)

    if request.method == "POST":
        assignment = get_object_or_404(
            ProjectWorker,
            pk=assignment_id,
            project=project,
        )
        assignment.delete()
        messages.success(request, "Team member removed from the project.")

    return redirect("project_detail", pk=project.pk)


def expense_create(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ExpenseForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        expense = form.save(commit=False)
        expense.project = project
        expense.save()

        messages.success(request, "Expense recorded successfully.")
        return redirect("project_detail", pk=project.pk)

    return render(request, "projects/expense_form.html", {
        "form": form,
        "project": project,
    })

def task_create(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = TaskForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        task = form.save(commit=False)
        task.project = project
        task.save()

        project.update_progress()

        messages.success(request, "Task created successfully.")
        return redirect("project_detail", pk=project.pk)

    return render(request, "projects/task_form.html", {
        "form": form,
        "project": project,
        "page_title": "Add Task",
    })


def task_edit(request, pk, task_pk):
    project = get_object_or_404(Project, pk=pk)
    task = get_object_or_404(
        Task,
        pk=task_pk,
        project=project,
    )

    form = TaskForm(request.POST or None, instance=task)

    if request.method == "POST" and form.is_valid():
        form.save()

        project.update_progress()

        messages.success(request, "Task updated successfully.")
        return redirect("project_detail", pk=project.pk)

    return render(request, "projects/task_form.html", {
        "form": form,
        "project": project,
        "page_title": "Edit Task",
    })
