from datetime import timedelta

from django import forms

from .models import Lambing, Lamb


class LambingForm(forms.ModelForm):
    father = forms.CharField(
        required=False,
        label="Otac / ovan izvan stada",
        help_text="Unesi 9 brojeva. HR se dodaje automatski.",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "123456789",
            "inputmode": "numeric",
            "maxlength": "9",
            "pattern": "[0-9]{9}",
        })
    )

    class Meta:
        model = Lambing
        fields = [
            "mother",
            "lambing_date",
            "father_sheep",
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
            "father_sheep": forms.Select(attrs={"class": "form-select"}),
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

    def clean(self):
        cleaned_data = super().clean()

        mother = cleaned_data.get("mother")
        lambing_date = cleaned_data.get("lambing_date")
        father_sheep = cleaned_data.get("father_sheep")
        father = cleaned_data.get("father")

        if father_sheep and father:
            raise forms.ValidationError(
                "Odaberi ili oca iz stada ili upiši oca izvan stada, ne oboje."
            )

        if mother and lambing_date:
            min_age_date = mother.birth_date + timedelta(days=304)

            if lambing_date < min_age_date:
                raise forms.ValidationError(
                    "Ovca ne može imati janjenje ako nije stara barem 10 mjeseci."
                )

            existing_lambings = Lambing.objects.filter(mother=mother)

            if self.instance and self.instance.pk:
                existing_lambings = existing_lambings.exclude(pk=self.instance.pk)

            for item in existing_lambings:
                difference = abs((lambing_date - item.lambing_date).days)

                if 0 < difference < 180:
                    raise forms.ValidationError(
                        "Za istu ovcu ne može se unijeti novo janjenje unutar 180 dana."
                    )

        return cleaned_data


class LambForm(forms.ModelForm):
    initial_tag = forms.CharField(
        required=False,
        label="Inicijalna oznaka",
        max_length=3,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "001",
            "inputmode": "numeric",
            "pattern": "[0-9]{1,3}",
            "maxlength": "3",
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
            "maxlength": "9",
        })
    )

    breed = forms.ChoiceField(
        required=False,
        label="Pasmina janjeta",
        choices=[],
        widget=forms.Select(attrs={"class": "form-select lamb-breed-select"})
    )

    class Meta:
        model = Lamb
        fields = [
            "initial_tag",
            "official_tag",
            "sex",
            "breed",
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["sex"].required = False
        self.fields["breed"].choices = [
            ("", "Automatski / odaberi pasminu")
        ] + list(Lamb._meta.get_field("breed").choices)

    def clean_initial_tag(self):
        tag = self.cleaned_data.get("initial_tag", "").strip()

        if not tag:
            return ""

        if not tag.isdigit():
            raise forms.ValidationError("Inicijalna oznaka mora sadržavati samo brojeve.")

        if len(tag) > 3:
            raise forms.ValidationError("Inicijalna oznaka može imati najviše 3 broja.")

        return tag.zfill(3)

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

        initial_tag = cleaned_data.get("initial_tag")
        official_tag = cleaned_data.get("official_tag")
        sex = cleaned_data.get("sex")
        marking_date = cleaned_data.get("marking_date")

        if not initial_tag and not official_tag and not sex and not marking_date:
            return cleaned_data

        if not initial_tag:
            raise forms.ValidationError(
                "Za uneseno janje moraš unijeti inicijalnu oznaku."
            )

        if not sex:
            raise forms.ValidationError(
                "Za uneseno janje moraš odabrati spol."
            )

        if official_tag and not marking_date:
            raise forms.ValidationError(
                "Ako je unesena službena markica, mora biti unesen datum službenog markiranja."
            )

        if marking_date and not official_tag:
            raise forms.ValidationError(
                "Datum službenog markiranja ne može biti unesen bez službene markice."
            )

        return cleaned_data