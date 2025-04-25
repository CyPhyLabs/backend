# mirror_token_view.py

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta

class MirrorRefreshTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        # Generate a refresh token with custom long expiry (6 months)
        refresh = RefreshToken.for_user(user)
        refresh.set_exp(lifetime=timedelta(days=180))

        return Response({
            'mirror_refresh_token': str(refresh),
        }, status=status.HTTP_200_OK)
