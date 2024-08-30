import logging
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from ..models import Message, Recipient
from ..serializers import RecipientSerializer

logger = logging.getLogger(__name__)

class ListNotificationsView(generics.ListAPIView):
    serializer_class = RecipientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        return Recipient.objects.filter(user_id=user_id)
    
# list all the entries in recipient model regardless of the user
class ListAllNotificationsView(generics.ListAPIView):
    serializer_class = RecipientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Recipient.objects.all()

class UpdateNotificationStatusView(generics.UpdateAPIView):
    serializer_class = RecipientSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user_id = self.request.user.id
        notification_id = self.kwargs['notification_id']
        print(f"Fetching recipient with user_id: {user_id} and notification_id: {notification_id}")
        logger.debug(f"Fetching recipient with user_id: {user_id} and notification_id: {notification_id}")
        return get_object_or_404(Recipient, user_id=user_id, message_id=notification_id)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        action = self.kwargs.get('action')

        if action == 'delivered':
            instance.status = 'delivered'
        elif action == 'acknowledge':
            instance.acknowledged = True

        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)