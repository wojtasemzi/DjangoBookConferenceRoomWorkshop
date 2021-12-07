from django.db import models

class Rooms(models.Model):
    name = models.fields.CharField(max_length=255, unique=True)
    capacity = models.fields.IntegerField()
    projector = models.fields.BooleanField()

    def __str__(self) -> str:
        return f'{self.name}'
