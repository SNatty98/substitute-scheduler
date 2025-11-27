from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from ..models import Assignment, Application
from ..serializers import AssignmentListSerializer, AssignmentDetailSerializer
from ..services import AssignmentService


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.select_related(
        'created_by', 'selected_substitute').all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AssignmentDetailSerializer
        return AssignmentListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtering by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # Filter by date
        date_from = self.request.query_params.get('date')
        if date_from:
            queryset = queryset.filter(date__gte=date_from)

        # Filter by subject
        subject = self.request.query_params.get('subject')
        if subject:
            queryset = queryset.filter(subject__icontains=subject)

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def select_substitute(self, request, pk=None):
        assignment = self.get_object()
        application_id = request.data.get('application_id')

        application = get_object_or_404(
            Application,
            id=application_id,
            assignment=assignment
        )

        try:
            assignment = AssignmentService.select_substitute(
                assignment, application)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
