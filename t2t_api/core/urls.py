from django.urls import path
from .api import RegisterView, LogoutView, CustomTokenObtainPairView, CustomTokenRefreshView, TestUserIDView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('test/', TestUserIDView.as_view(), name='test'),
]