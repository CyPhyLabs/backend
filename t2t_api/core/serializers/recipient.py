from rest_framework import serializers
from rest_framework.exceptions import ValidationError
import uuid

from ..models import Recipient, Message, CustomUser

class RecipientSerializer(serializers.ModelSerializer):
    message = serializers.SerializerMethodField()
    class Meta:
        model = Recipient
        fields = ['user_id','message_id', 'status', 'acknowledged', 'created_at', 'updated_at', 'delivered_at','message']
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
    
    def get_message(self, obj):
        message = Message.objects.get(id=obj.message_id.id)
        created_by = message.created_by
        user = CustomUser.objects.get(id=created_by).username
        return {
            'title': message.message.get('title'),
            'body': message.message.get('body'),
            'priority': message.message.get('priority'),
            'message_id': message.message.get('message_id'),
            'created_by': user
        }