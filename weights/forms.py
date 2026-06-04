from django import forms
from .models import WeightRecord


class WeightRecordForm(forms.ModelForm):
    class Meta:
        model = WeightRecord
        fields = [
            "sheep",
            "lamb",
            "date",
            "weight",
            "notes",
        ]

        widgets = {
            "sheep": forms.Select(attrs={"class": "form-select"}),
            "lamb": forms.Select(attrs={"class": "form-select"}),
            "date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),
            "weight": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "placeholder": "npr. 12.50"
            }),
            "notes": forms.Textarea(attrs={
                "rows": 3,
                "class": "form-control"
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        sheep = cleaned_data.get("sheep")
        lamb = cleaned_data.get("lamb")

        if not sheep and not lamb:
            raise forms.ValidationError(
                "Moraš odabrati grlo ili janje."
            )

        if sheep and lamb:
            raise forms.ValidationError(
                "Odaberi ili grlo ili janje, ne oboje."
            )

        return cleaned_data