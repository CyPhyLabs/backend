from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from ..models import Device
from ..serializers import DeviceSerializer
from ..services import handle_device_token

class DeviceTokenView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user_id = request.user.id
        user_type = request.user.user_type
        serializer = DeviceSerializer(data=request.data)
        if serializer.is_valid():
            device, created = handle_device_token(user_id, serializer.validated_data['device_token'], user_type)
            return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user_id = request.user.id
        try:
            device = Device.objects.get(user_id=user_id)
            device.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Device.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)