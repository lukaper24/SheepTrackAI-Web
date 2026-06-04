from django import forms

from .models import Lambing, Lamb


class LambingForm(forms.ModelForm):
    father = forms.CharField(
        required=False,
        label="Otac / ovan",
        help_text="Unesi 9 brojeva. HR se dodaje automatski.",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "123456789",
            "inputmode": "numeric",
        })
    )

    class Meta:
        model = Lambing
        fields = [
            "mother",
            "lambing_date",
            "father",
            "lamb_count",
            "notes",
        ]

        widgets = {
            "mother": forms.Select(attrs={"class": "form-select"}),
            "lambing_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),
            "lamb_count": forms.Select(attrs={"class": "form-select"}),
            "notes": forms.Textarea(attrs={
                "rows": 3,
                "class": "form-control"
            }),
        }

    def clean_father(self):
        father = self.cleaned_data.get("father", "").strip()

        if not father:
            return ""

        father = father.upper().replace("HR", "").replace(" ", "")

        if not father.isdigit():
            raise forms.ValidationError("Za oca unesi samo brojeve.")

        if len(father) != 9:
            raise forms.ValidationError("Broj oca mora imati točno 9 brojeva.")

        return f"HR {father}"


class LambForm(forms.ModelForm):
    initial_tag = forms.CharField(
        label="Inicijalna oznaka",
        max_length=3,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "001",
            "inputmode": "numeric",
            "pattern": "[0-9]{3}",
        })
    )

    official_tag = forms.CharField(
        required=False,
        label="Službena markica",
        help_text="Unesi 9 brojeva. HR se dodaje automatski.",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "123456789",
            "inputmode": "numeric",
            "pattern": "[0-9]{9}",
        })
    )

    class Meta:
        model = Lamb
        fields = [
            "initial_tag",
            "official_tag",
            "sex",
            "marking_date",
            "notes",
        ]

        widgets = {
            "sex": forms.Select(attrs={"class": "form-select"}),
            "marking_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),
            "notes": forms.Textarea(attrs={
                "rows": 2,
                "class": "form-control"
            }),
        }

    def clean_initial_tag(self):
        tag = self.cleaned_data.get("initial_tag", "").strip()

        if not tag.isdigit():
            raise forms.ValidationError("Inicijalna oznaka mora sadržavati samo brojeve.")

        if len(tag) != 3:
            raise forms.ValidationError("Inicijalna oznaka mora imati točno 3 broja.")

        return tag

    def clean_official_tag(self):
        tag = self.cleaned_data.get("official_tag", "").strip()

        if not tag:
            return ""

        tag = tag.upper().replace("HR", "").replace(" ", "")

        if not tag.isdigit():
            raise forms.ValidationError("Službena markica mora sadržavati samo brojeve.")

        if len(tag) != 9:
            raise forms.ValidationError("Službena markica mora imati točno 9 brojeva.")

        return f"HR {tag}"

    def clean(self):
        cleaned_data = super().clean()

        official_tag = cleaned_data.get("official_tag")
        marking_date = cleaned_data.get("marking_date")

        if official_tag and not marking_date:
            raise forms.ValidationError(
                "Ako je unesena službena markica, mora biti unesen datum službenog markiranja."
            )

        return cleaned_data