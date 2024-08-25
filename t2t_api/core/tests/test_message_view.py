# core/api/test_message_view.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.views import APIView
from rest_framework.response import Response
from unittest.mock import patch
from firebase_admin import messaging

# View
class CreateMessageView(APIView):
    def post(self, request, *args, **kwargs):
        title = request.data.get('title')
        body = request.data.get('body')
        topic = request.data.get('topic')  # match 'topic' with the data

        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            topic=topic,
        )

        response = messaging.send(message)
        return Response({'message_id': response}, status=status.HTTP_201_CREATED)

# Test
class CreateMessageViewTests(APITestCase):
    @patch('firebase_admin.messaging.send')
    def test_create_message(self, mock_send):
        url = reverse('create-message')
        data = {
            'title': 'Test Title',
            'body': 'Test Body',
            'topic': 'test_topic'  # match 'topic' with the view
        }
        mock_send.return_value = 'mock_message_id'  # Mock response from FCM
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(mock_send.called)
        mock_send.assert_called_once_with(messaging.Message(
            notification=messaging.Notification(
                title='Test Title',
                body='Test Body',
            ),
            topic='test_topic',
        ))
