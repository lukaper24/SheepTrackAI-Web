from django import forms
from .models import Breeding


class BreedingForm(forms.ModelForm):
    class Meta:
        model = Breeding
        fields = [
            "ewe",
            "ram",
            "breeding_date",
            "notes",
        ]

        widgets = {
            "ewe": forms.Select(attrs={"class": "form-select"}),
            "ram": forms.Select(attrs={"class": "form-select"}),
            "breeding_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "notes": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        }