from rest_framework import generics, permissions
from django.contrib.auth import get_user_model

from ..serializers import RegisterSerializer
from ..services import create_personal_calendar_for_user

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
    def perform_create(self, serializer):
        user = serializer.save()
        create_personal_calendar_for_user(user)