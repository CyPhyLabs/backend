# services/fcm_service.py

from firebase_admin import messaging

def send_fcm_message(message):
    fcm_message = messaging.Message(
        data={
            'title': message.message.get('title'),
            'body': message.message.get('body'),
            'message_id': str(message.id),
        },
        topic=message.target_audience,
    )

    try:
        response = messaging.send(fcm_message)
        message.status = 'sent'
    except Exception as e:
        message.status = 'failed'
    
    message.save()