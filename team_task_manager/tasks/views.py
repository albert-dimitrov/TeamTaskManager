from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Task
from .serializers import TaskSerializer
from .permissions import IsLeaderOrAdminOrReadOnly, IsAssignedUserOrReadOnly


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsLeaderOrAdminOrReadOnly]

    def get_queryset(self):
        room_id = self.request.query_params.get('room')
        queryset = Task.objects.all()
        if room_id:
            queryset = queryset.filter(room_id=room_id)

        user = self.request.user
        if not user.is_staff:
            queryset = queryset.filter(room__members=user)
        return queryset

    def perform_create(self, serializer):
        serializer.save()


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAssignedUserOrReadOnly]

    def perform_update(self, serializer):
        instance = serializer.save()

        if instance.status == 'completed' and instance.assigned_to:
            profile = instance.assigned_to.profile
            profile.points += instance.points
            profile.save()
