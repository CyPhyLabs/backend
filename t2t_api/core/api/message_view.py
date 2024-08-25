from rest_framework import generics, status
from rest_framework.response import Response
from core.models.message_model import Message, Recipient
from core.serializers.message import MessageSerializer
from core.permissions import IsUser, IsStaff
from rest_framework.permissions import IsAuthenticated
from core.services.fcm_service import send_fcm_message


class CreateMessageView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsStaff]

    def perform_create(self, serializer):
        # Save the message
        message = serializer.save(created_by=self.request.user.id)
        # set created field of the message model by to request.user_id
        message.message["created_by"] = str(self.request.user.id)  # Convert UUID to string
        message.save()

        # Update the message JSON field with the message ID
        message.message['message_id'] = str(message.id)
        message.save()

        # Send message via FCM using the service function
        send_fcm_message(message)


        # NEED TO IMPLEMENT LOGIC FOR THIS
        # Populate Recipient table (you'll need to adapt this to your needs)
        # Example: assuming `users` is a list of user IDs
        users = []  # Fetch the list of users based on the target audience
        for user_id in users:
            Recipient.objects.create(user_id=user_id, message_id=message)

class ListMessagesView(generics.ListAPIView): # works
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class RetrieveMessageView(generics.RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_object(self):
        queryset = self.get_queryset()
        message_id = self.kwargs.get('id')
        if message_id:
            obj = generics.get_object_or_404(queryset, id=message_id)
            return obj
        return None

class UpdateMessageView(generics.UpdateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_object(self):
        queryset = self.get_queryset()
        message_id = self.kwargs.get('id')
        if message_id:
            obj = generics.get_object_or_404(queryset, id=message_id)
            return obj
        return None

class DeleteMessageView(generics.DestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_object(self):
        queryset = self.get_queryset()
        message_id = self.kwargs.get('id')
        if message_id:
            obj = generics.get_object_or_404(queryset, id=message_id)
            return obj
        return None

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Message deleted successfully."}, status=status.HTTP_204_NO_CONTENT)