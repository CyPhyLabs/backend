from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..models import PersonalCalendar
from ..services import fetch_events, create_event, update_event, delete_event, format_google_event
from ..serializers.event import EventSerializer
from django.utils.dateparse import parse_datetime
from datetime import datetime, timedelta


class PersonalCalendarEventsView(APIView):
    permission_classes = [IsAuthenticated]

    def get_personal_calendar(self, user):
        return PersonalCalendar.objects.filter(user=user).first()

    def get(self, request):
        personal_cal = self.get_personal_calendar(request.user)
        if not personal_cal:
            return Response({"error": "No personal calendar found."}, status=404)

        start_param = request.GET.get("start")
        end_param = request.GET.get("end")

        if not start_param:
            time_min = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            time_min = parse_datetime(start_param)
            if not time_min:
                return Response({"error": "Invalid start date format."}, status=400)

        if not end_param:
            time_max = time_min + timedelta(days=7)
        else:
            time_max = parse_datetime(end_param)
            if not time_max:
                return Response({"error": "Invalid end date format."}, status=400)

        try:
            events = fetch_events(personal_cal.calendar_id, time_min, time_max)
            return Response(events)
        except Exception as e:
            return Response({"error": f"Error fetching events: {str(e)}"}, status=500)

    def post(self, request):
        personal_cal = self.get_personal_calendar(request.user)
        if not personal_cal:
            return Response({"error": "No personal calendar found."}, status=404)

        serializer = EventSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        event_data = {
            'summary': serializer.validated_data['title'],
            'description': serializer.validated_data.get('description', ''),
            'start': {'dateTime': serializer.validated_data['start_time'].isoformat(), 'timeZone': 'America/Chicago'},
            'end': {'dateTime': serializer.validated_data['end_time'].isoformat(), 'timeZone': 'America/Chicago'},
            'location': serializer.validated_data.get('location', '')
        }

        try:
            created_event = create_event(personal_cal.calendar_id, event_data)
            return Response(format_google_event(created_event), status=201)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

    def put(self, request):
        personal_cal = self.get_personal_calendar(request.user)
        if not personal_cal:
            return Response({"error": "No personal calendar found."}, status=404)

        serializer = EventSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        try:
            updated_event = update_event(
                calendar_id=personal_cal.calendar_id,
                event_id=serializer.validated_data["event_id"],
                updated_data={
                    'summary': serializer.validated_data['title'],
                    'description': serializer.validated_data.get('description', ''),
                    'start': {'dateTime': serializer.validated_data['start_time'].isoformat(), 'timeZone': 'America/Chicago'},
                    'end': {'dateTime': serializer.validated_data['end_time'].isoformat(), 'timeZone': 'America/Chicago'},
                    'location': serializer.validated_data.get('location', '')
                }
            )
            return Response(format_google_event(updated_event))

        except Exception as e:
            return Response({'error': str(e)}, status=500)

    def delete(self, request):
        personal_cal = self.get_personal_calendar(request.user)
        if not personal_cal:
            return Response({"error": "No personal calendar found."}, status=404)

        event_id = request.data.get("event_id")
        if not event_id:
            return Response({"error": "Missing event_id in request body."}, status=400)

        try:
            delete_event(personal_cal.calendar_id, event_id)
            return Response({"detail": "Event deleted."})
        except Exception as e:
            return Response({'error': str(e)}, status=500)
