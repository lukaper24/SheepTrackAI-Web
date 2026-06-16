from django.core.exceptions import ValidationError
from django.db import models

from sheep.models import Sheep


class VeterinaryRecord(models.Model):

    RECORD_TYPES = [
        ("VACCINATION", "Cijepljenje"),
        ("TREATMENT", "Liječenje"),
        ("DISEASE", "Bolest"),
        ("OTHER", "Ostalo"),
    ]

    PERFORMED_BY_CHOICES = [
        ("SELF", "Samostalno"),
        ("VET", "Veterinar"),
    ]

    animal = models.ForeignKey(
        Sheep,
        on_delete=models.CASCADE,
        related_name="veterinary_records",
        verbose_name="Grlo"
    )

    record_type = models.CharField(
        max_length=20,
        choices=RECORD_TYPES,
        verbose_name="Vrsta zapisa"
    )

    date = models.DateField(verbose_name="Datum")

    title = models.CharField(
        max_length=150,
        verbose_name="Naziv"
    )

    medicine = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Lijek / cjepivo"
    )

    performed_by = models.CharField(
        max_length=10,
        choices=PERFORMED_BY_CHOICES,
        default="SELF",
        verbose_name="Tko je izvršio"
    )

    vet_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Ime veterinara"
    )

    withdrawal_period = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Karenca u danima"
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Napomena"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.performed_by == "VET" and not self.vet_name:
            raise ValidationError({
                "vet_name": "Ako je zahvat obavio veterinar, moraš upisati ime veterinara."
            })

        if self.performed_by == "SELF":
            self.vet_name = ""

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.animal.eid_number} - {self.get_record_type_display()}"