from django.contrib import admin
from .models import User, Substitute, Assignment, Application

admin.site.register(User)
admin.site.register(Substitute)
admin.site.register(Assignment)
admin.site.register(Application)
