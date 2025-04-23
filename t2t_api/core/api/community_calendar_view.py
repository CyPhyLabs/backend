from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..services import fetch_events, create_event, update_event, delete_event
from ..serializers import EventSerializer
from ..models import CommunityCalendar
from django.utils.dateparse import parse_datetime
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta

class CommunityCalendarEventsView(APIView):
    permission_classes = [IsAuthenticated]

    def get_calendar(self, request):
        calendar_id = request.GET.get("calendar_id")
        if not calendar_id:
            raise ValueError("Missing 'calendar_id' query parameter.")
        return get_object_or_404(CommunityCalendar, calendar_id=calendar_id)

    def get(self, request):
        try:
            calendar = self.get_calendar(request)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        start_param = request.GET.get("start")
        end_param = request.GET.get("end")

        if not start_param:
            time_min = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            time_min = parse_datetime(start_param)
            if not time_min:
                return Response({"error": "Invalid start date format."}, status=status.HTTP_400_BAD_REQUEST)

        if not end_param:
            time_max = time_min + timedelta(days=7)
        else:
            time_max = parse_datetime(end_param)
            if not time_max:
                return Response({"error": "Invalid end date format."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            events = fetch_events(calendar.calendar_id, time_min, time_max)
            return Response(events)
        except Exception as e:
            return Response({"error": f"Error fetching events: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        calendar_id = request.GET.get("calendar_id")
        if not calendar_id:
            return Response({"error": "Missing calendar_id in query params."}, status=status.HTTP_400_BAD_REQUEST)
        calendar = get_object_or_404(CommunityCalendar, calendar_id=calendar_id)

        serializer = EventSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        event_data = {
            'summary': serializer.validated_data['title'],
            'description': serializer.validated_data.get('description', ''),
            'start': {'dateTime': serializer.validated_data['start_time'].isoformat(), 'timeZone': 'America/Chicago'},
            'end': {'dateTime': serializer.validated_data['end_time'].isoformat(), 'timeZone': 'America/Chicago'},
            'location': serializer.validated_data.get('location', '')
        }

        try:
            created_event = create_event(calendar_id, event_data)
            return Response(created_event, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        calendar_id = request.GET.get("calendar_id")
        if not calendar_id:
            return Response({"error": "Missing calendar_id in query params."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = EventSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            updated_event = update_event(
                calendar_id=calendar_id,
                event_id=serializer.validated_data["event_id"],
                updated_data={
                    'summary': serializer.validated_data['title'],
                    'description': serializer.validated_data.get('description', ''),
                    'start': {'dateTime': serializer.validated_data['start_time'].isoformat(), 'timeZone': 'America/Chicago'},
                    'end': {'dateTime': serializer.validated_data['end_time'].isoformat(), 'timeZone': 'America/Chicago'},
                    'location': serializer.validated_data.get('location', '')
                }
            )
            return Response(updated_event)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        calendar_id = request.GET.get("calendar_id")
        if not calendar_id:
            return Response({"error": "Missing calendar_id in query params."}, status=status.HTTP_400_BAD_REQUEST)
        event_id = request.data.get("event_id")
        if not event_id:
            return Response({"error": "Missing event_id in body."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            delete_event(calendar_id, event_id)
            return Response({"detail": "Event deleted."})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
