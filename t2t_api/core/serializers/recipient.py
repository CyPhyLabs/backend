from rest_framework import serializers
from core.models import Recipient
from rest_framework.exceptions import ValidationError
import uuid


class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipient
        fields = ['user_id','message_id', 'status', 'acknowledged', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            'status': {'required': False},  # Make status optional
            'acknowledged': {'required': False},  # Make acknowledged optional
            'user_id': {'required': False}
        }

    def create(self, validated_data):
        # Create the Recipient object
        recipient = super().create(validated_data)
        return recipient