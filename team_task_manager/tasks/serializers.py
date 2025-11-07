from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Task

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'room', 'assigned_to',
            'status', 'difficulty', 'points', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
