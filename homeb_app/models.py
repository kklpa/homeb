from django.db import models
import datetime
from django.utils.timezone import utc

class Kategoria(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name

class Miesiac(models.Model):
    name = models.CharField(max_length=15)
    
    def __str__(self):
        return self.name

class Zakup(models.Model):
    category = models.ForeignKey(Kategoria, on_delete=models.CASCADE)
    month = models.ForeignKey(Miesiac, on_delete=models.CASCADE, default=datetime.datetime(2015, 12, 26, 17, 1, 28, 128127, tzinfo=utc))
    name = models.CharField(max_length=30)
    price = models.FloatField(default=0.1)
    quantity = models.IntegerField(default=1)
    date = models.DateField(auto_now_add=True, blank=True)

    def total(self):
        amount = (self.price * self.quantity)
        return amount
        
    def __str__(self):
        return self.name
