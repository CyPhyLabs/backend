from django.db import models
from django.conf import settings
import uuid

class PersonalCalendar(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='personal_calendars')
    calendar_id = models.CharField(max_length=255)  # Google Calendar ID
    calendar_name = models.CharField(max_length=255)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'calendar_id')

    def __str__(self):
        return f"{self.calendar_name} - {self.user.email}"

class CommunityCalendar(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    calendar_id = models.CharField(max_length=255, unique=True)  # Google Calendar ID
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    subscribers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='subscribed_calendars',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class CalendarEvent(models.Model):
    calendar = models.ForeignKey(CommunityCalendar, on_delete=models.CASCADE, related_name='events')
    event_id = models.CharField(max_length=255, unique=True)  # Google Calendar Event ID
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
