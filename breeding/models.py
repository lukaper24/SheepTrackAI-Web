from datetime import timedelta
from django.db import models

from sheep.models import Sheep


class Breeding(models.Model):
    ewe = models.ForeignKey(
        Sheep,
        on_delete=models.CASCADE,
        related_name="breedings_as_ewe",
        verbose_name="Ovca"
    )

    ram = models.ForeignKey(
        Sheep,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="breedings_as_ram",
        verbose_name="Ovan"
    )

    breeding_date = models.DateField(
        verbose_name="Datum pripusta"
    )

    expected_lambing_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Očekivano janjenje"
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Napomena"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.expected_lambing_date = self.breeding_date + timedelta(days=150)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ewe.eid_number} - {self.breeding_date}"