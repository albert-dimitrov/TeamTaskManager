from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()

class Room(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    leaders = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leaders')
    members = models.ManyToManyField(User, related_name='members', blank=True)

    def __str__(self):
        return self.name