from django.db import models

from django.contrib.auth.models import User as AuthUser
from rest_framework import status
# Create your models here.

    
class Wallet (models.Model):

    ENABLED = "enabled"
    DISABLED = "disabled"

    STATUS_ENABLED = (
        (ENABLED, "Enabled"),
        (DISABLED, "Disabled")
    )

    owned_by =  models.OneToOneField(AuthUser, on_delete = models.CASCADE)
    status = models.CharField(max_length= 10,choices=STATUS_ENABLED, blank=None, null=True)
    balance = models.DecimalField(max_digits=25, decimal_places=3)


class Deposit (models.Model):

    wallet_id = models.ForeignKey(Wallet, on_delete = models.CASCADE)
    deposited_by = models.ForeignKey(AuthUser, on_delete = models.CASCADE)
    deposited_at = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=25, decimal_places=3)
    reference_id = models.CharField(max_length=300, null= True, blank=None)

class Withdrawn (models.Model):
    wallet_id = models.ForeignKey(Wallet, on_delete = models.CASCADE)
    withdrawn_by = models.ForeignKey(AuthUser, on_delete = models.CASCADE)
    withdrawn_at = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=25, decimal_places=3)
    reference_id = models.CharField(max_length=300, null= True, blank=None)