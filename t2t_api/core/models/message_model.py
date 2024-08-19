from django.db import models
import uuid

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.JSONField()  # Store the contents of the message as JSON
    target_audience = models.CharField(max_length=255)  # FCM Topic
    created_by = models.UUIDField()  # Unique identifier of the user that created the message
    status = models.CharField(max_length=50, choices=[
        ('queued', 'Queued'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ], default='queued')  # Status of the message
    scheduled_time = models.DateTimeField(null=True, blank=True)  # Nullable scheduled time
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of creation
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp of last update
    attachment_url = models.URLField(null=True, blank=True)  # Link to object storage for attachment

    def __str__(self):
        return f"Message {self.id} - Status: {self.status}"


class Recipient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField()  # Unique identifier for the user
    message_id = models.ForeignKey(Message, on_delete=models.CASCADE)  # Reference to the message
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
    ], default='pending')  # Delivery status
    acknowledged = models.BooleanField(default=False)  # Acknowledgment status
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of creation
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp of last update

    def __str__(self):
        return f"Recipient {self.id} - User {self.user_id} - Status: {self.status}"