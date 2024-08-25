from rest_framework import serializers
from core.models import Message, Recipient
from rest_framework.exceptions import ValidationError
import uuid

class MessageSerializer(serializers.ModelSerializer):
    title = serializers.CharField(write_only=True)
    body = serializers.CharField(write_only=True)
    priority = serializers.CharField(write_only=True, required=False, default='low')
    target_audience = serializers.CharField()
    created_by = serializers.UUIDField(default=uuid.uuid4)

    class Meta:
        model = Message
        fields = [
            'id', 'target_audience', 'message', 'priority', 'created_by', 
            'status', 'scheduled_time', 'created_at', 'updated_at', 
            'attachment_url', 'title', 'body'
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
        # Extract the user from the request context
        user = self.context['request'].user # BHAVIKKKK HELP ME WITH THIS PLEASE

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

        # Assign the user ID to the created_by field
        validated_data['created_by'] = "ca39434a-5d29-471a-a90a-80c90c867f75" # WITH THIS AS WELL, it should have been user.id

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

class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipient
        fields = ['id', 'user_id', 'message_id', 'status', 'acknowledged', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        # Extract the user from the request context
        user = self.context['request'].user

        # Assign the user ID to the user_id field
        validated_data['user_id'] = user.id

        # Create the Recipient object
        recipient = super().create(validated_data)

        return recipient