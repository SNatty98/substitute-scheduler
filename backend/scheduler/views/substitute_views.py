from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Substitute
from ..serializers import SubstituteSerializer


class SubstituteViewSet(viewsets.ModelViewSet):
    queryset = Substitute.objects.select_related('user').all()
    serializer_class = SubstituteSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        subjects = self.request.query_params.get('subjects')
        if subjects:
            queryset = queryset.filter(subjects__contains=subjects)
        return queryset
