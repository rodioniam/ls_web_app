from django.db import models


class Session(models.Model):
    total_points = models.IntegerField(default=10)


class Card(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Multiplier(models.Model):
    name = models.CharField(max_length=100)
    value = models.FloatField()
    description = models.CharField(max_length=200, blank=True)
    is_positive = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class CardMultiplier(models.Model):
    parent_card = models.ForeignKey(Card, on_delete=models.CASCADE)
    assigned_mults = models.ForeignKey(Multiplier, on_delete=models.CASCADE)
