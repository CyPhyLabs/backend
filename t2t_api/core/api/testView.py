# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class TestUserIDView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id  # Access the user ID from the request
        return Response({"user_id": user_id})