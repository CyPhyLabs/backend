from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from ..services import create_google_calendar

from ..models.calendar_model import PersonalCalendar, CommunityCalendar
from ..serializers.calendar import (
    PersonalCalendarSerializer,
    CommunityCalendarSerializer,
    CommunityCalendarDetailSerializer
)
from ..permissions import IsUser, IsStaff

# Personal Calendar Views
class CreatePersonalCalendarView(generics.CreateAPIView):
    serializer_class = PersonalCalendarSerializer
    permission_classes = [IsAuthenticated, IsUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ListPersonalCalendarsView(generics.ListAPIView):
    serializer_class = PersonalCalendarSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PersonalCalendar.objects.filter(user=self.request.user)

class UpdatePersonalCalendarView(generics.UpdateAPIView):
    serializer_class = PersonalCalendarSerializer
    permission_classes = [IsAuthenticated, IsUser]

    def get_object(self):
        calendar_id = self.kwargs.get('id')
        return get_object_or_404(
            PersonalCalendar, 
            id=calendar_id,
            user=self.request.user
        )

class DeletePersonalCalendarView(generics.DestroyAPIView):
    serializer_class = PersonalCalendarSerializer
    permission_classes = [IsAuthenticated, IsUser]

    def get_object(self):
        calendar_id = self.kwargs.get('id')
        return get_object_or_404(
            PersonalCalendar, 
            id=calendar_id,
            user=self.request.user
        )

# Community Calendar Views
class CreateCommunityCalendarView(generics.CreateAPIView):
    serializer_class = CommunityCalendarSerializer
    permission_classes = [IsAuthenticated, IsStaff]

class ListCommunityCalendarsView(generics.ListAPIView):
    queryset = CommunityCalendar.objects.all()
    serializer_class = CommunityCalendarSerializer
    permission_classes = [IsAuthenticated]

class RetrieveCommunityCalendarView(generics.RetrieveAPIView):
    queryset = CommunityCalendar.objects.all()
    serializer_class = CommunityCalendarDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        calendar_id = self.kwargs.get('id')
        return get_object_or_404(CommunityCalendar, id=calendar_id)

class SubscribeCalendarView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, calendar_id):
        calendar = get_object_or_404(CommunityCalendar, id=calendar_id)
        user = request.user

        if calendar.subscribers.filter(id=user.id).exists():
            return Response(
                {"detail": "Already subscribed to this calendar."},
                status=status.HTTP_400_BAD_REQUEST
            )

        calendar.subscribers.add(user)
        return Response(
            {"detail": "Successfully subscribed to calendar."},
            status=status.HTTP_200_OK
        )

class UnsubscribeCalendarView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, calendar_id):
        calendar = get_object_or_404(CommunityCalendar, id=calendar_id)
        user = request.user

        if not calendar.subscribers.filter(id=user.id).exists():
            return Response(
                {"detail": "Not subscribed to this calendar."},
                status=status.HTTP_400_BAD_REQUEST
            )

        calendar.subscribers.remove(user)
        return Response(
            {"detail": "Successfully unsubscribed from calendar."},
            status=status.HTTP_200_OK
        )

class ListMySubscriptionsView(generics.ListAPIView):
    serializer_class = CommunityCalendarSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CommunityCalendar.objects.filter(subscribers=self.request.user)
    
class GenerateCommunityCalendarView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsStaff]

    def post(self, request):
        name = request.data.get('name')
        description = request.data.get('description', '')

        if not name:
            return Response({'error': 'Calendar name is required.'}, status=400)

        try:
            calendar_data = create_google_calendar(name, description)

            community_calendar = CommunityCalendar.objects.create(
                calendar_id=calendar_data['calendar_id'],
                name=calendar_data['name'],
                description=calendar_data['description']
            )

            serializer = CommunityCalendarSerializer(community_calendar)
            return Response(serializer.data, status=201)

        except Exception as e:
            return Response({'error': str(e)}, status=500)