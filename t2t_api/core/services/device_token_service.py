import logging
from firebase_admin import messaging
from django.utils import timezone
from ..models import Device

logger = logging.getLogger('__main__')

def handle_device_token(user_id, device_token, user_type):
    # Update or create the device token
    device, created = Device.objects.update_or_create(
        user_id=user_id,
        defaults={
            'device_token': device_token,
            'last_used': timezone.now()
        }
    )
    
    # Subscribe to FCM topic based on user type
    if user_type == 'user':
        # Subsribe to veterans and everyone topic
        try:
            response = messaging.subscribe_to_topic([device_token], topic='everyone')
            logger.info(f'Subscribed to topic "everyone": {response}')
        except Exception as e:
            logger.error(f'Error subscribing to topic "everyone": {e}')
        try:
            response = messaging.subscribe_to_topic([device_token], topic='veterans')
            logger.info(f'Subscribed to topic "veterans": {response}')
        except Exception as e:
            logger.error(f'Error subscribing to topic "veterans": {e}')
    elif user_type == 'staff':
        # Subscribe to staff and everyone topic
        try:
            response = messaging.subscribe_to_topic([device_token], topic='everyone')
            logger.info(f'Subscribed to topic "everyone": {response}')
        except Exception as e:
            logger.error(f'Error subscribing to topic "everyone": {e}')
        try:
            response = messaging.subscribe_to_topic([device_token], topic='staff')
            logger.info(f'Subscribed to topic "staff": {response}')
        except Exception as e:
            logger.error(f'Error subscribing to topic "staff": {e}')
    return device, created