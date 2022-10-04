from django.contrib.auth import get_user_model
from django.db import models

PAYMENT_CHOICES = (
    (0, "One Time"),
    (1, "Monthly Frequency")
)

CURRENCY_CHOICES = (
    ("USD", "USA Dollar"),
)


class Products(models.Model):
    stripe_product_id = models.CharField(max_length=63)
    name = models.CharField(max_length=63)
    info = models.TextField(null=True, blank=True)
    full_description = models.TextField(null=True, blank=True)
    stripe_price_id = models.CharField(max_length=63)
    price = models.FloatField()
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="USD")
    payment = models.IntegerField(choices=PAYMENT_CHOICES, default=0)


class Sales(models.Model):
    product = models.ForeignKey(Products, on_delete=models.DO_NOTHING)
    value = models.FloatField()
    fees = models.FloatField()
    quantity = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=True)
    client = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING)
    note = models.TextField()

