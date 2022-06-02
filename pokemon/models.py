from django.db import models


class Pokedex(models.Model):
    name = models.CharField(max_length=200)
    abilities = models.CharField(max_length=200)
    stats = models.CharField(max_length=200)
    sprite = models.CharField(max_length=300)

    def __str__(self):
        return self.name
