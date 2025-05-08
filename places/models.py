from django.db import models


class Place(models.Model):
    address = models.CharField('адрес', max_length=255, unique=True)
    lat = models.FloatField('широта', null=True)
    lon = models.FloatField('долгота', null=True)
    updated_at = models.DateTimeField('дата обновления', auto_now=True)

    def __str__(self):
        return self.address

