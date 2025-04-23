from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class EventSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField(required=False)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    location = serializers.CharField(required=False)
    calendar_id = serializers.CharField(required=False)
    event_id = serializers.CharField(required=False)  # For updates