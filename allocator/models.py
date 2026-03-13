from django.db import models


class Session(models.Model):
    total_points = models.IntegerField(default=10)


class Card(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.name
