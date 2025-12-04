from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from ..models import Assignment, Application
from ..serializers import AssignmentForSubstituteSerializer, AssignmentListSerializer, AssignmentDetailSerializer
from ..services import AssignmentService


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.select_related(
        'created_by', 'selected_substitute').all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AssignmentDetailSerializer
        return AssignmentListSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.role == 'substitute':
            serializer = AssignmentForSubstituteSerializer(
                instance,
                context={'request': request}
            )
        else:
            serializer = self.get_serializer(instance)

        return Response(serializer.data)

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.role == 'admin':
            queryset = queryset.filter(
                created_by=self.request.user, date__gte=timezone.now().date())

        if self.action == 'retrieve' and self.request.user.role == 'admin':
            queryset = queryset.prefetch_related(
                'applications__substitute__user')

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
        try:
            assignment = AssignmentService.create_with_postcode_lookup(
                school_name=serializer.validated_data['school_name'],
                school_postcode=serializer.validated_data['school_postcode'],
                date=serializer.validated_data['date'],
                start_time=serializer.validated_data['start_time'],
                end_time=serializer.validated_data['end_time'],
                subject=serializer.validated_data['subject'],
                year_group=serializer.validated_data.get('year_group', ''),
                notes=serializer.validated_data.get('notes', ''),
                created_by=self.request.user
            )
        # Update the serializer instance with the created assignment
            serializer.instance = assignment
        except ValueError as e:
            raise ValidationError({'school_postcode': str(e)})

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
            return Response(
                AssignmentDetailSerializer(assignment).data,
                status=status.HTTP_200_OK
            )
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def available(self, request):

        queryset = Assignment.objects.filter(
            status='open',
            date__gte=timezone.now().date()
        ).select_related('created_by').order_by('date', 'start_time')

        serializer = AssignmentListSerializer(queryset, many=True)
        return Response(serializer.data)
