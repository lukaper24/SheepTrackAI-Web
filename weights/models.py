from django.db import models

from sheep.models import Sheep
from lambing.models import Lamb


class WeightRecord(models.Model):
    sheep = models.ForeignKey(
        Sheep,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="weight_records",
        verbose_name="Grlo"
    )

    lamb = models.ForeignKey(
        Lamb,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="weight_records",
        verbose_name="Janje"
    )

    date = models.DateField(
        verbose_name="Datum vaganja"
    )

    weight = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Težina kg"
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Napomena"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        animal = self.sheep or self.lamb
        return f"{animal} - {self.weight} kg"