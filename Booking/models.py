from django.db import models
from django.db.models.deletion import CASCADE

class Rooms(models.Model):
    name = models.fields.CharField(max_length=255, unique=True)
    capacity = models.fields.IntegerField()
    projector = models.fields.BooleanField()

    def __str__(self) -> str:
        return f'{self.name}'

class Reservations(models.Model):
    date = models.fields.DateField()
    room = models.ForeignKey(Rooms, on_delete=CASCADE)
    comment = models.fields.TextField()

    class Meta:
        unique_together = [['date', 'room_id']]
