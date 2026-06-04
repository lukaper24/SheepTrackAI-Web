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

    STATUS_CHOICES = [
        ('ACTIVE', 'Aktivna'),
        ('SOLD', 'Prodana'),
        ('DEAD', 'Uginula'),
    ]

    farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
        related_name='sheep'
    )

    eid_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Životni broj"
    )

    name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Naziv / nadimak"
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

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ACTIVE',
        verbose_name="Status"
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Napomena"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.eid_number