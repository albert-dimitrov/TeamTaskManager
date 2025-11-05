from django.contrib.auth import get_user_model
from django.db import models

from team_task_manager.rooms.models import Room
from team_task_manager.tasks.choices import StatusChoices, DifficultyChoices

User = get_user_model()


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default='Pending')
    difficulty = models.CharField(max_length=20, choices=DifficultyChoices.choices, default='Easy')
    points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
