from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Room
from .serializers import RoomSerializer, RoomMemberActionSerializer
from .permissions import IsLeaderOrAdmin
from django.contrib.auth import get_user_model


User = get_user_model()


class RoomListCreateView(generics.ListCreateAPIView):
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Room.objects.all()
        return Room.objects.filter(members=user)

    def perform_create(self, serializer):
        room = serializer.save(leaders=self.request.user)
        room.members.add(self.request.user)


class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated, IsLeaderOrAdmin]
    queryset = Room.objects.all()


class AddMemberView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsLeaderOrAdmin]

    def post(self, request, pk):
        room = get_object_or_404(Room, pk=pk)
        self.check_object_permissions(request, room)

        serializer = RoomMemberActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, pk=serializer.validated_data['user_id'])

        if user in room.members.all():
            return Response({"detail": "User already in room."}, status=status.HTTP_400_BAD_REQUEST)

        room.members.add(user)
        return Response({"detail": f"{user.email} added to {room.name}."}, status=status.HTTP_200_OK)


class RemoveMemberView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsLeaderOrAdmin]

    def post(self, request, pk):
        room = get_object_or_404(Room, pk=pk)
        self.check_object_permissions(request, room)

        serializer = RoomMemberActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, pk=serializer.validated_data['user_id'])

        if user not in room.members.all():
            return Response({"detail": "User is not in this room."}, status=status.HTTP_400_BAD_REQUEST)

        room.members.remove(user)
        return Response({"detail": f"{user.email} removed from {room.name}."}, status=status.HTTP_200_OK)
