from rest_framework import serializers
from django.contrib.auth.models import User

from fitApp.models import *


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = "__all__"
        extra_kwargs = {
            'exercises': {'required': False},  # Make exercises optional
        }