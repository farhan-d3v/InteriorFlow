
from django import forms
from .models import Project, SiteUpdate, Worker, ProjectWorker, Expense



class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "name",
            "client",
            "location",
            "description",
            "start_date",
            "target_end_date",
            "estimated_budget",
            "status",
            "progress",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "target_end_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        target_end_date = cleaned_data.get("target_end_date")
        status = cleaned_data.get("status")
        progress = cleaned_data.get("progress")

        if start_date and target_end_date and target_end_date < start_date:
            self.add_error(
                "target_end_date",
                "Target completion date cannot be before the start date.",
            )

        if status == "Completed" and progress is not None and progress != 100:
            self.add_error(
                "progress",
                "A completed project must have 100% progress.",
            )

        return cleaned_data

class SiteUpdateForm(forms.ModelForm):
    class Meta:
        model = SiteUpdate
        fields = [
            "title",
            "notes",
            "progress",
            "posted_by",
            "update_date",
        ]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 4}),
            "update_date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_progress(self):
        progress = self.cleaned_data["progress"]

        if not 0 <= progress <= 100:
            raise forms.ValidationError(
                "Progress must be between 0 and 100."
            )
        return progress
class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ["name", "role", "contact"]


class AssignWorkerForm(forms.Form):
    worker = forms.ModelChoiceField(
        queryset=Worker.objects.all(),
        empty_label="Select a worker",
        label="Team member",
    )


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["description", "amount", "expense_date"]
        widgets = {
            "expense_date": forms.DateInput(attrs={"type": "date"}),
        }
