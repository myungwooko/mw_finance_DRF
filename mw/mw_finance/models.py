from django.db import models
from django.template.defaultfilters import truncatechars
from django.contrib.auth.models import User




User = User


class Blacklist(models.Model):
    id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=225, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def short_token(self):
        return truncatechars(self.token, 10)


class Currency(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80, unique=True)




class Currency_info(models.Model):
    id                  = models.AutoField(primary_key=True)
    name                = models.CharField(max_length=80,null=False)
    symbol              = models.CharField(max_length=80,null=False)
    current_price       = models.DecimalField(max_digits=10, decimal_places=5, null=False)
    comparing_yesterday = models.DecimalField(max_digits=10, decimal_places=5, null=False)
    change              = models.DecimalField(max_digits=10, decimal_places=5, null=False)
    currency_id = models.ForeignKey(
            'Currency',
            on_delete=models.CASCADE,
        )
    created_at          = models.DateTimeField()



































