from rest_framework import generics, status
from rest_framework.response import Response
from core.models.message_model import Message, Recipient
from core.serializers.message import MessageSerializer, RecipientSerializer
from firebase_admin import messaging

class CreateMessageView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        # Save the message
        message = serializer.save()

        # Format message for FCM
        fcm_message = messaging.Message(
            data={
                'title': message.message.get('title'),
                'body': message.message.get('body'),
                'message_id': str(message.id),
            },
            topic=message.target_audience,
        )

        # Send message via FCM
        try:
            response = messaging.send(fcm_message)
            message.status = 'sent'
        except Exception as e:
            message.status = 'failed'
        
        # Save the message with updated status
        message.save()


        # NEED TO IMPLEMENT LOGIC FOR THIS
        # Populate Recipient table (you'll need to adapt this to your needs)
        # Example: assuming `users` is a list of user IDs
        users = []  # Fetch the list of users based on the target audience
        for user_id in users:
            Recipient.objects.create(user_id=user_id, message_id=message)

class ListMessagesView(generics.ListAPIView):
    # NEED TO IMPLEMENT LOGIC FOR THIS
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class RetrieveMessageView(generics.RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class UpdateMessageView(generics.UpdateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class DeleteMessageView(generics.DestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class ListNotificationsView(generics.ListAPIView):
    serializer_class = RecipientSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Recipient.objects.filter(user_id=user_id)

class UpdateNotificationStatusView(generics.UpdateAPIView):
    serializer_class = RecipientSerializer

    def get_object(self):
        user_id = self.kwargs['user_id']
        notification_id = self.kwargs['notification_id']
        return Recipient.objects.get(user_id=user_id, id=notification_id)
