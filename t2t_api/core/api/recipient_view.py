from rest_framework import generics, status
from rest_framework.response import Response
from core.models.message_model import Message, Recipient
from core.serializers.recipient import RecipientSerializer
from rest_framework.permissions import IsAuthenticated

   
class ListNotificationsView(generics.ListAPIView):
    serializer_class = RecipientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        return Recipient.objects.filter(user_id=user_id)

class UpdateNotificationStatusView(generics.UpdateAPIView):
    serializer_class = RecipientSerializer

    def get_object(self):
        user_id = self.request.user.id
        notification_id = self.kwargs['notification_id']
        return Recipient.objects.get(user_id=user_id, id=notification_id)