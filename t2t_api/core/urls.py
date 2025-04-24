from django.urls import path
from .api import RegisterView, LogoutView
from .api import (
    CreateMessageView, 
    ListMessagesView, RetrieveMessageView,
    UpdateMessageView, DeleteMessageView, ListNotificationsView,
    UpdateNotificationStatusView, 
    ListAllNotificationsView,
    DeleteNotificationView,
)


from .api import RegisterView, LogoutView, CustomTokenObtainPairView, CustomTokenRefreshView, TestUserIDView, DeviceTokenView


from .api import (
    CreatePersonalCalendarView, 
    ListPersonalCalendarsView,
    UpdatePersonalCalendarView, 
    DeletePersonalCalendarView,
    CreateCommunityCalendarView, 
    ListCommunityCalendarsView,
    RetrieveCommunityCalendarView, 
    SubscribeCalendarView,
    UnsubscribeCalendarView, 
    ListMySubscriptionsView,
    GenerateCommunityCalendarView,

    CommunityCalendarEventsView,
    PersonalCalendarEventsView
)




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
    path('notifications/<uuid:notification_id>/', DeleteNotificationView.as_view(), name='delete-notification'),

    # Device Token APIs
    path('device-token/', DeviceTokenView.as_view(), name='device-token'),


    # Personal Calendar endpoints
    path('calendars/personal/create/', CreatePersonalCalendarView.as_view(), name='create-personal-calendar'),
    path('calendars/personal/', ListPersonalCalendarsView.as_view(), name='list-personal-calendars'),
    path('calendars/personal/<uuid:id>/update/', UpdatePersonalCalendarView.as_view(), name='update-personal-calendar'),
    path('calendars/personal/<uuid:id>/delete/', DeletePersonalCalendarView.as_view(), name='delete-personal-calendar'),
    path('calendars/personal/events/', PersonalCalendarEventsView.as_view(), name='personal-calendar-events'),

    # Community Calendar endpoints
    path('calendars/community/create/', CreateCommunityCalendarView.as_view(), name='create-community-calendar'),
    path('calendars/community/', ListCommunityCalendarsView.as_view(), name='list-community-calendars'),
    path('calendars/community/<uuid:id>/', RetrieveCommunityCalendarView.as_view(), name='retrieve-community-calendar'),
    path('calendars/community/<uuid:calendar_id>/subscribe/', SubscribeCalendarView.as_view(), name='subscribe-calendar'),
    path('calendars/community/<uuid:calendar_id>/unsubscribe/', UnsubscribeCalendarView.as_view(), name='unsubscribe-calendar'),
    path('calendars/subscriptions/', ListMySubscriptionsView.as_view(), name='my-subscriptions'),

    # Generate Community Calendar
    path("calendars/community/generate/", GenerateCommunityCalendarView.as_view(), name="generate_community_calendar"),
    path("calendars/community/events/", CommunityCalendarEventsView.as_view(), name='community-calendar-events'),

    
    

    # test fcm sending apis
    # path('create-message/', CreateMessageView.as_view(), name='create-message'),

    # test user id
    path('test/', TestUserIDView.as_view(), name='test'),
]