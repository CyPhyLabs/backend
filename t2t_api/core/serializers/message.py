from rest_framework import serializers
from rest_framework.exceptions import ValidationError
import uuid

from ..models import Message

class MessageSerializer(serializers.ModelSerializer):
    title = serializers.CharField(write_only=True)
    body = serializers.CharField(write_only=True)
    priority = serializers.CharField(write_only=True, required=False, default='low')
    target_audience = serializers.CharField()

    class Meta:
        model = Message
        fields = [
            'message', 'target_audience', 'priority', 'title', 'body'
        ]
        extra_kwargs = {
            'priority': {'required': False},  # Make priority optional
            'message': {'required': False},  # Make message not required
        }

    def validate(self, attrs):
        # Ensure the message field is populated
        title = attrs.get('title')
        body = attrs.get('body')
        priority = attrs.get('priority', 'low')

        if not title or not body:
            raise ValidationError("Title and body are required fields.")

        attrs['message'] = {
            'title': title,
            'body': body,
            'priority': priority,
            'message_id': str(uuid.uuid4())  # Assign a new UUID to message_id within the JSON
        }

        return attrs

    def create(self, validated_data):

        # Pop title and body from validated_data
        title = validated_data.pop('title', None)
        body = validated_data.pop('body', None)

        # Ensure the message field is populated
        validated_data['message'] = {
            'title': title,
            'body': body,
            'priority': validated_data.get('priority', 'low'),
            'message_id': str(uuid.uuid4())  # Assign a new UUID to message_id within the JSON
        }

        # Create the Message object
        message = super().create(validated_data)

        return message

    def update(self, instance, validated_data):
        # Update fields
        title = validated_data.pop('title', None)
        body = validated_data.pop('body', None)
        priority = validated_data.get('priority', instance.message.get('priority', 'low'))

        # Update the message field
        message_data = instance.message.copy()
        if title:
            message_data['title'] = title
        if body:
            message_data['body'] = body
        message_data['priority'] = priority

        validated_data['message'] = message_data

        # Update the instance
        return super().update(instance, validated_data)
