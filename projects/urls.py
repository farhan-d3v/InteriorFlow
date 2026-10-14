
from django.urls import path
from . import views
from .views import task_create, task_edit

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("projects/", views.project_list, name="project_list"),
    path("projects/new/", views.project_create, name="project_create"),
    path("projects/<int:pk>/", views.project_detail, name="project_detail"),
    path("projects/<int:pk>/edit/", views.project_edit, name="project_edit"),
path(
    "projects/<int:pk>/updates/new/",
    views.site_update_create,
    name="site_update_create",
),
path("workers/", views.worker_list, name="worker_list"),
path("workers/new/", views.worker_create, name="worker_create"),
path(
    "projects/<int:pk>/workers/assign/",
    views.assign_worker,
    name="assign_worker",
),
path(
    "projects/<int:pk>/workers/<int:assignment_id>/remove/",
    views.remove_assignment,
    name="remove_assignment",
),
path(
    "projects/<int:pk>/expenses/new/",
    views.expense_create,
    name="expense_create",
),
path(
    "projects/<int:pk>/tasks/add/",
    task_create,
    name="task_create",
),
path(
    "projects/<int:pk>/tasks/<int:task_pk>/edit/",
    task_edit,
    name="task_edit",
),

]
