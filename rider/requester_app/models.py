from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from rider_app.models import Rider

class Request(models.Model):

    class AssetType(models.TextChoices):
        LAPTOP = 'LP', _('LAPTOP')
        TRAVEL_BAG = 'TB', _('TRAVEL_BAG')
        PACKAGE = 'PK', _('PACKAGE')

    class Sensitivity(models.TextChoices):
        HIGHLY_SENSITIVE = 'HS', _('HIGHLY_SENSITIVE')
        SENSITIVE = 'S', _('SENSITIVE')
        NORMAL = 'N', _('NORMAL')

    class Status(models.TextChoices):
        PENDING = 'PD', _('PENDING')
        EXPIRED = 'EX', _('EXPIRED')

    request_id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True)
    source = models.CharField(max_length=30,null=False, blank=False)
    destination = models.CharField(max_length=30, null=False, blank=False)
    datetime = models.DateTimeField(null=False, blank=False)
    timestamp = models.BigIntegerField(null=False,default=0)
    quantity = models.IntegerField(null=False, blank=False, default=1)
    asset_type = models.CharField(max_length=2, choices=AssetType.choices)
    sensitivity = models.CharField(max_length=2, choices=Sensitivity.choices)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.PENDING)


class Requester(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    requester_id = models.IntegerField(null=False)
    request_id = models.ForeignKey(Request, null=False, on_delete=models.CASCADE)


class AppliedRequest(models.Model):
    requester_id = models.ForeignKey(Requester, null=False, on_delete=models.CASCADE)
    rider_id = models.ForeignKey(Rider, null=False, on_delete=models.CASCADE)


