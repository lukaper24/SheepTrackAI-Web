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
            "performed_by",
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
            "performed_by": forms.Select(attrs={"class": "form-select"}),
            "vet_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ime i prezime veterinara"
            }),
            "withdrawal_period": forms.NumberInput(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()

        performed_by = cleaned_data.get("performed_by")
        vet_name = cleaned_data.get("vet_name")

        if performed_by == "VET" and not vet_name:
            raise forms.ValidationError(
                "Ako je zahvat obavio veterinar, moraš upisati ime veterinara."
            )

        if performed_by == "SELF":
            cleaned_data["vet_name"] = ""

        return cleaned_data