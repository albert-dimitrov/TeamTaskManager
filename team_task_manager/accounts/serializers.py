from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile

UserModel = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'points']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = UserModel
        fields = ['id', 'email', 'is_active', 'is_staff', 'profile']
