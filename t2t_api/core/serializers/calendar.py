from rest_framework import serializers
from ..models.calendar_model import PersonalCalendar, CommunityCalendar
from django.contrib.auth import get_user_model

User = get_user_model()

class PersonalCalendarSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = PersonalCalendar
        fields = ['id', 'calendar_id', 'calendar_name', 'is_primary', 
                 'user_email', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user_email', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Add the current user to the validated data
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)

    def validate(self, data):
        user = self.context['request'].user
        
        if data.get('is_primary'):
            existing_primary = PersonalCalendar.objects.filter(
                user=user, is_primary=True
            ).exists()
            if existing_primary:
                raise serializers.ValidationError(
                    "User already has a primary calendar"
                )
        return data

class CommunityCalendarSerializer(serializers.ModelSerializer):
    subscriber_count = serializers.SerializerMethodField()

    class Meta:
        model = CommunityCalendar
        fields = ['id', 'calendar_id', 'name', 'description', 
                 'subscriber_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_subscriber_count(self, obj):
        return obj.subscribers.count()

class CommunityCalendarDetailSerializer(CommunityCalendarSerializer):
    subscribers = serializers.SerializerMethodField()

    class Meta(CommunityCalendarSerializer.Meta):
        fields = CommunityCalendarSerializer.Meta.fields + ['subscribers']

    def get_subscribers(self, obj):
        return [
            {
                'id': user.id,
                'email': user.email,
                'username': user.username
            }
            for user in obj.subscribers.all()
        ]
    
    