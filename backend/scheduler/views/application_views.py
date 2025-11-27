from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..models import Application
from ..serializers import ApplicationSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.select_related(
        'substitute__user', 'assignment').all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter applications based on user role"""
        queryset = super().get_queryset()

        # Substitutes see only their own applications
        if self.request.user.role == 'substitute':
            queryset = queryset.filter(substitute__user=self.request.user)

        # Optional filter by assignment
        assignment_id = self.request.query_params.get('assignment_id')
        if assignment_id:
            queryset = queryset.filter(assignment_id=assignment_id)

        return queryset

    def perform_create(self, serializer):
        """Auto-set substitute when creating application"""
        substitute = self.request.user.substitute_profile
        serializer.save(substitute=substitute)
