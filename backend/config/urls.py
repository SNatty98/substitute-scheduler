from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from scheduler.views.auth_views import register, current_user, register_substitute

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/register/', register, name='register'),
    path('api/auth/register/substitute/',
         register_substitute, name='register_substitute'),
    path('api/auth/me/', current_user, name='current_user'),
    path('api/', include('scheduler.urls')),
]
