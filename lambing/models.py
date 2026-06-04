from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models

from sheep.models import Sheep


class Lambing(models.Model):
    mother = models.ForeignKey(
        Sheep,
        on_delete=models.CASCADE,
        related_name="lambings",
        verbose_name="Majka"
    )

    lambing_date = models.DateField(
        verbose_name="Datum janjenja"
    )

    father = models.CharField(
        max_length=12,
        blank=True,
        verbose_name="Otac / ovan"
    )

    lamb_count = models.PositiveSmallIntegerField(
        verbose_name="Broj janjadi",
        choices=[
            (1, "1 janje"),
            (2, "2 janjeta"),
            (3, "3 janjeta"),
            (4, "4 janjeta"),
            (5, "5 janjadi"),
        ],
        default=1
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Napomena"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.mother and self.lambing_date:
            min_age_date = self.mother.birth_date + timedelta(days=304)

            if self.lambing_date < min_age_date:
                raise ValidationError(
                    "Ovca ne može imati janjenje ako nije stara barem 10 mjeseci."
                )

            existing_lambings = Lambing.objects.filter(
                mother=self.mother
            ).exclude(pk=self.pk)

            for item in existing_lambings:
                difference = abs((self.lambing_date - item.lambing_date).days)

                if difference < 180:
                    raise ValidationError(
                        "Za istu ovcu ne može se unijeti novo janjenje unutar 180 dana."
                    )

    def save(self, *args, **kwargs):
        if self.father:
            father = self.father.upper().replace("HR", "").replace(" ", "").strip()

            if father.isdigit() and len(father) == 9:
                self.father = f"HR {father}"

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.mother.eid_number} - {self.lambing_date}"


class Lamb(models.Model):

    SEX_CHOICES = [
        ("Z", "Žensko"),
        ("M", "Muško"),
    ]

    lambing = models.ForeignKey(
        Lambing,
        on_delete=models.CASCADE,
        related_name="lambs",
        verbose_name="Janjenje"
    )

    initial_tag = models.CharField(
        max_length=3,
        verbose_name="Inicijalna oznaka"
    )

    official_tag = models.CharField(
        max_length=12,
        blank=True,
        verbose_name="Službena markica"
    )

    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        verbose_name="Spol"
    )

    marking_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Datum službenog markiranja"
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Napomena"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.initial_tag:
            tag = self.initial_tag.strip()

            if not tag.isdigit() or len(tag) > 3:
                raise ValidationError(
                    "Inicijalna oznaka mora imati najviše 3 broja, npr. 001."
                )

            self.initial_tag = tag.zfill(3)

        if self.official_tag:
            official = self.official_tag.upper().replace("HR", "").replace(" ", "")

            if not official.isdigit() or len(official) != 9:
                raise ValidationError(
                    "Službena markica mora imati točno 9 brojeva."
                )
            if self.marking_date and not self.official_tag:
                raise ValidationError(
                    "Datum službenog markiranja ne može biti unesen bez službene markice."
                )

            if not self.marking_date:
                raise ValidationError(
                    "Ako je unesena službena markica, mora biti unesen i datum službenog markiranja."
                )

    def save(self, *args, **kwargs):
        if self.official_tag:
            official = self.official_tag.upper().replace("HR", "").replace(" ", "").strip()
            self.official_tag = f"HR {official}"

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        if self.official_tag:
            return self.official_tag

        return f"Inicijalno {self.initial_tag}"