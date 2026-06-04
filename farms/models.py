from django.db import models
from django.contrib.auth.models import User


class Farm(models.Model):
    owner = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
    related_name='farm'
)

    name = models.CharField(
        max_length=200,
        verbose_name="Naziv OPG-a"
    )

    address = models.CharField(
        max_length=255,
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    phone = models.CharField(
        max_length=50,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name