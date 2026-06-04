from datetime import date, timedelta

from django.db import models
from django.core.validators import RegexValidator
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

    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='sheep')

    eid_number = models.CharField(
    max_length=12,
    unique=True,
    verbose_name="Životni broj"
)

    breed = models.CharField(max_length=50, choices=BREED_CHOICES, default='SOLCAVSKO_JEZERSKA', verbose_name="Pasmina")
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='Z', verbose_name="Spol")
    birth_date = models.DateField(verbose_name="Datum rođenja")

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

    notes = models.TextField(blank=True, verbose_name="Napomena")
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_category(self):
        six_months_ago = date.today() - timedelta(days=183)

        if self.birth_date > six_months_ago:
            return 'JANJE'

        if self.sex == 'M':
            if self.is_breeding_ram:
                return 'OVAN'
            return 'OVNIC'

        return 'SILJEZICA'

    def save(self, *args, **kwargs):
        self.eid_number = self.eid_number.upper().strip()
        self.category = self.calculate_category()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.eid_number