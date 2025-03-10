from django.urls import path
from .api import RegisterView, LogoutView
from .api import (
    CreateMessageView, 
    ListMessagesView, RetrieveMessageView,
    UpdateMessageView, DeleteMessageView, ListNotificationsView,
    UpdateNotificationStatusView, 
    ListAllNotificationsView
)


from .api import RegisterView, LogoutView, CustomTokenObtainPairView, CustomTokenRefreshView, TestUserIDView, DeviceTokenView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),



    # Message APIs
    path('messages/create/', CreateMessageView.as_view(), name='create-message'),
    path('messages/', ListMessagesView.as_view(), name='list-messages'),
    path('messages/<uuid:id>/', RetrieveMessageView.as_view(), name='retrieve-message'),
    path('messages/<uuid:id>/update/', UpdateMessageView.as_view(), name='update-message'),
    path('messages/<uuid:id>/delete/', DeleteMessageView.as_view(), name='delete-message'),

    # Recipient APIs
    path('notifications/', ListNotificationsView.as_view(), name='list-notifications'),
    path('notifications/<uuid:notification_id>/<str:action>/', UpdateNotificationStatusView.as_view(), name='update-notification-status'),
    path('notifications/all/', ListAllNotificationsView.as_view(), name='list-all-notifications'),

    # Device Token APIs
    path('device-token/', DeviceTokenView.as_view(), name='device-token'),

    # test fcm sending apis
    # path('create-message/', CreateMessageView.as_view(), name='create-message'),

    # test user id
    path('test/', TestUserIDView.as_view(), name='test'),
]