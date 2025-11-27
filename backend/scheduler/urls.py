from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubstituteViewSet, AssignmentViewSet, ApplicationViewSet

router = DefaultRouter()
router.register(r'substitutes', SubstituteViewSet)
router.register(r'assignments', AssignmentViewSet)
router.register(r'applications', ApplicationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
