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

class Rok(models.Model):
    name = models.IntegerField()
    def __str__(self):
        return self.name

class Zakup(models.Model):
    category = models.ForeignKey(Kategoria, on_delete=models.CASCADE, default=1)
    month = models.ForeignKey(Miesiac, on_delete=models.CASCADE)
    year = models.ForeignKey(Rok, on_delete=models.CASCADE, default=2000)
    name = models.CharField(max_length=30)
    price = models.FloatField(default=0.1)
    quantity = models.IntegerField(default=1)
    total= models.FloatField(default=0.1)
    date = models.DateField(auto_now_add=True, blank=True)

    def amount(self):
        value = (self.price * self.quantity)
        return value
    
    def set_year(self):
        self.year = 2
        return self.year


    def __str__(self):
        return self.name