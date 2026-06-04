from django import forms
from .models import VeterinaryRecord


class VeterinaryRecordForm(forms.ModelForm):
    class Meta:
        model = VeterinaryRecord
        fields = [
            "animal",
            "record_type",
            "date",
            "title",
            "medicine",
            "vet_name",
            "withdrawal_period",
            "notes",
        ]

        widgets = {
            "animal": forms.Select(attrs={"class": "form-select"}),
            "record_type": forms.Select(attrs={"class": "form-select"}),
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "medicine": forms.TextInput(attrs={"class": "form-control"}),
            "vet_name": forms.TextInput(attrs={"class": "form-control"}),
            "withdrawal_period": forms.NumberInput(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        }