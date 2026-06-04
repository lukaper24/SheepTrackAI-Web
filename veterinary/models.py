from django.db import models
from sheep.models import Sheep


class VeterinaryRecord(models.Model):

    RECORD_TYPES = [
        ("VACCINATION", "Cijepljenje"),
        ("TREATMENT", "Liječenje"),
        ("DISEASE", "Bolest"),
        ("OTHER", "Ostalo"),
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

    vet_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Veterinar"
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

    def __str__(self):
        return f"{self.animal.eid_number} - {self.get_record_type_display()}"