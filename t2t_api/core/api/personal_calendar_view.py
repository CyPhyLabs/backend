from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..models import PersonalCalendar
from ..services import fetch_events
from django.utils.dateparse import parse_datetime
from datetime import datetime, timedelta

class PersonalCalendarEventsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        personal_cal = PersonalCalendar.objects.filter(user=request.user).first()
        if not personal_cal:
            return Response(
                {"error": "No personal calendar found."}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # Get start and end parameters, default to today if not provided
        start_param = request.GET.get("start")
        end_param = request.GET.get("end")

        if not start_param:
            time_min = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            time_min = parse_datetime(start_param)
            if not time_min:
                return Response(
                    {"error": "Invalid start date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if not end_param:
            time_max = time_min + timedelta(days=7)  # Default to a week from start
        else:
            time_max = parse_datetime(end_param)
            if not time_max:
                return Response(
                    {"error": "Invalid end date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        try:
            events = fetch_events(personal_cal.calendar_id, time_min, time_max)
            return Response(events)
        except Exception as e:
            return Response(
                {"error": f"Error fetching events: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )