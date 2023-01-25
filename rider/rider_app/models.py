from django.db import models

from django.utils.translation import gettext_lazy as _
import uuid

class Rider(models.Model):

    class TravelMedium(models.TextChoices):
        BUS = 'BS', _('BUS')
        TRAIN = 'TR', _('TRAIN')
        CAR = 'CR', _('CAR')

    rider_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    source = models.CharField(max_length=30,null=False, blank=False)
    destination = models.CharField(max_length=30, null=False, blank=False)
    datetime = models.DateTimeField(null=False, blank=False)
    timestamp = models.BigIntegerField(null=False, default=0)
    travel_medium = models.CharField(
        max_length=2,
        choices=TravelMedium.choices,
    )
    quantity = models.IntegerField(null=False, blank=False, default=1)

    class Meta:
        db_table = "Rider"

