from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Room


User = get_user_model()


class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']



class RoomSerializer(serializers.ModelSerializer):
    leaders = UserSummarySerializer(read_only=True)
    members = UserSummarySerializer(read_only=True, many=True)

    class Meta:
        model = Room
        fields = ['id', 'name', 'description', 'leaders', 'members']


class RoomMemberActionSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def validate_user_id(self, value):
        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist.")
        return value
