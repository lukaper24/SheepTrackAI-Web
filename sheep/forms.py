from django import forms
from .models import Sheep


class SheepForm(forms.ModelForm):
    eid_number = forms.CharField(
        label="Životni broj",
        max_length=9,
        help_text="Unesi samo 9 brojeva. Oznaka HR dodaje se automatski.",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "123456789",
            "inputmode": "numeric",
            "pattern": "[0-9]{9}",
        })
    )
    class Meta:
        model = Sheep
        fields = [
            "eid_number",
            "breed",
            "sex",
            "birth_date",
            "is_breeding_ram",
            "notes",
        ]

        widgets = {
            "breed": forms.Select(attrs={"class": "form-select"}),
            "sex": forms.Select(attrs={"class": "form-select"}),
            "birth_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),
            "is_breeding_ram": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
            "notes": forms.Textarea(attrs={
                "rows": 3,
                "class": "form-control",
                "placeholder": "Napomena..."
            }),
        }
    def clean_eid_number(self):
        eid = self.cleaned_data.get("eid_number", "").strip()

        if eid.startswith("HR"):
            eid = eid.replace("HR", "").strip()

        eid = eid.replace(" ", "")

        if not eid.isdigit():
            raise forms.ValidationError("Unesi samo brojeve.")

        if len(eid) != 9:
            raise forms.ValidationError("Životni broj mora imati točno 9 brojeva.")

        return f"HR {eid}"
    def clean(self):
        cleaned_data = super().clean()

        sex = cleaned_data.get("sex")
        is_breeding_ram = cleaned_data.get("is_breeding_ram")

        if sex == "Z" and is_breeding_ram:
            cleaned_data["is_breeding_ram"] = False

        return cleaned_data
    
class SheepExitForm(forms.ModelForm):
        class Meta:
            model = Sheep
            fields = [
                "exit_date",
                "exit_reason",
            ]

            widgets = {
                "exit_date": forms.DateInput(attrs={
                    "type": "date",
                    "class": "form-control"
                }),
                "exit_reason": forms.Textarea(attrs={
                    "rows": 3,
                    "class": "form-control",
                    "placeholder": "Razlog, kupac, napomena..."
                }),
            }
class SheepImportForm(forms.Form):
    pdf_file = forms.FileField(
        label="PDF iz e-Posjednika",
        widget=forms.FileInput(attrs={
            "class": "form-control",
            "accept": ".pdf"
        })
    )