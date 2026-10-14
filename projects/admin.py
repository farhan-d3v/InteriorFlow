
from django.contrib import admin
from .models import Project, SiteUpdate, Worker, ProjectWorker, Expense

admin.site.register(Project)
admin.site.register(SiteUpdate)
admin.site.register(Worker)
admin.site.register(ProjectWorker)
admin.site.register(Expense)
