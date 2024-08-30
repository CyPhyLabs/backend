from django.urls import path
from .api import RegisterView, LogoutView
from .api.message_view import (
    # CreateMessageView, 
    ListMessagesView, RetrieveMessageView,
    UpdateMessageView, DeleteMessageView, ListNotificationsView,
    UpdateNotificationStatusView
)

from .api.test_message_view import(
    CreateMessageView
)




from .api import RegisterView, LogoutView, CustomTokenObtainPairView, CustomTokenRefreshView, TestUserIDView, DeviceTokenView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),



    # Message APIs
    # path('messages/', CreateMessageView.as_view(), name='create-message'),
    path('messages/', ListMessagesView.as_view(), name='list-messages'),
    path('messages/<uuid:id>/', RetrieveMessageView.as_view(), name='retrieve-message'),
    path('messages/<uuid:id>/', UpdateMessageView.as_view(), name='update-message'),
    path('messages/<uuid:id>/', DeleteMessageView.as_view(), name='delete-message'),

    # Recipient APIs
    path('user/<uuid:user_id>/notifications/', ListNotificationsView.as_view(), name='list-notifications'),
    path('user/<uuid:user_id>/notifications/<uuid:notification_id>/delivered/', UpdateNotificationStatusView.as_view(), name='delivered-notification'),
    path('user/<uuid:user_id>/notifications/<uuid:notification_id>/acknowledge/', UpdateNotificationStatusView.as_view(), name='acknowledge-notification'),

    # Device Token APIs
    path('device-token/', DeviceTokenView.as_view(), name='device-token'),

    # test fcm sending apis
    path('create-message/', CreateMessageView.as_view(), name='create-message'),

    # test user id
    path('test/', TestUserIDView.as_view(), name='test'),
]