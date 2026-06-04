from datetime import date, timedelta
import re

from django.core.exceptions import ValidationError
from django.db import models

from farms.models import Farm


class Sheep(models.Model):

    BREED_CHOICES = [
        ('CIGAJA', 'Cigaja'),
        ('CRESKA', 'Creska ovca'),
        ('DALMATINSKA_PRAMENKA', 'Dalmatinska pramenka'),
        ('DUBROVACKA_RUDA', 'Dubrovačka ovca – ruda'),
        ('ISTARSKA', 'Istarska ovca'),
        ('KRCKA', 'Krčka ovca'),
        ('LICKA_PRAMENKA', 'Lička pramenka'),
        ('PASKA', 'Paška ovca'),
        ('RAPSKA', 'Rapska ovca'),
        ('ISTOCNOFRIZIJSKA', 'Istočnofrizijska ovca'),
        ('MERINOLANDSCHAF', 'Merinolnadschaf / merinolandšaf'),
        ('ROMANOVSKA', 'Romanovska ovca'),
        ('SOLCAVSKO_JEZERSKA', 'Solčavsko-jezerska ovca'),
        ('SUFFOLK', 'Suffolk / safolk'),
        ('TRAVNICKA_PRAMENKA', 'Travnička / vlašićka / dubska pramenka'),
        ('DORPER', 'Dorper'),
        ('TEXEL', 'Texel / teksel'),
        ('KERRY_HILL', 'Kerry Hill'),
        ('CLUN_FOREST', 'Clun forest'),
        ('KAMERUNSKA', 'Kamerunska ovca'),
        ('BERRICHON_DU_CHER', 'Berrichon du Cher'),
        ('LACAUNE', 'Lacaune / lakon'),
        ('OSTALO', 'Ostalo'),
    ]

    SEX_CHOICES = [
        ('Z', 'Žensko'),
        ('M', 'Muško'),
    ]

    CATEGORY_CHOICES = [
        ('JANJE', 'Janje'),
        ('SILJEZICA', 'Šilježica'),
        ('OVNIC', 'Ovnić'),
        ('OVCA', 'Ovca'),
        ('OVAN', 'Ovan'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Aktivno'),
        ('SOLD', 'Prodano'),
        ('DEAD', 'Uginulo'),
        ('SLAUGHTERED', 'Zaklano'),
    ]

    farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
        related_name='sheep'
    )

    eid_number = models.CharField(
        max_length=12,
        unique=True,
        verbose_name="Životni broj"
    )

    breed = models.CharField(
        max_length=50,
        choices=BREED_CHOICES,
        default='SOLCAVSKO_JEZERSKA',
        verbose_name="Pasmina"
    )

    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        default='Z',
        verbose_name="Spol"
    )

    birth_date = models.DateField(
        verbose_name="Datum rođenja"
    )

    is_breeding_ram = models.BooleanField(
        default=False,
        verbose_name="Rasplodni ovan"
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='JANJE',
        verbose_name="Kategorija"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ACTIVE',
        verbose_name="Status"
    )

    exit_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Datum izlaska"
    )

    exit_reason = models.TextField(
        blank=True,
        verbose_name="Razlog / napomena izlaska"
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Napomena"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def calculate_category(self):
        six_months_ago = date.today() - timedelta(days=183)

        if self.birth_date > six_months_ago:
            return 'JANJE'

        if self.sex == 'M':
            if self.is_breeding_ram:
                return 'OVAN'
            return 'OVNIC'

        if self.pk and self.lambings.exists():
            return 'OVCA'

        return 'SILJEZICA'

    def clean(self):
        pattern = r"^HR\s\d{9}$"

        if not re.match(pattern, self.eid_number):
            raise ValidationError({
                "eid_number": "Životni broj mora biti u formatu HR 123456789."
            })

        if self.status != 'ACTIVE' and not self.exit_date:
            raise ValidationError({
                "exit_date": "Za prodano, uginulo ili zaklano grlo moraš unijeti datum izlaska."
            })

    def save(self, *args, **kwargs):
        number = self.eid_number.upper().replace("HR", "").replace(" ", "").strip()

        if number.isdigit() and len(number) == 9:
            self.eid_number = f"HR {number}"

        self.category = self.calculate_category()

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.eid_number