from rest_framework import serializers
from .models import User, Substitute, Assignment, Application


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']
        read_only_fields = ['id']


class SubstituteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    full_name = serializers.CharField(
        source='user.get_full_name', read_only=True)

    class Meta:
        model = Substitute
        fields = '__all__'


class AssignmentListSerializer(serializers.ModelSerializer):
    application_count = serializers.IntegerField(
        source='applications.count', read_only=True)
    selected_substitute_name = serializers.CharField(
        source='selected_substitute.user.get_full_name',
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = Assignment
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']


class AssignmentDetailSerializer(serializers.ModelSerializer):
    applications = serializers.SerializerMethodField()
    selected_substitute = SubstituteSerializer(read_only=True)

    class Meta:
        model = Assignment
        fields = '__all__'

    def get_applications(self, obj):
        applications = obj.applications.select_related('substitute__user')
        return ApplicationSerializer(applications, many=True).data


class ApplicationSerializer(serializers.ModelSerializer):
    substitute = SubstituteSerializer(read_only=True)
    distance = serializers.DecimalField(
        source='distance_miles',
        max_digits=5,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = Application
        fields = ['id', 'assignment', 'substitute', 'status',
                  'message', 'distance', 'applied_at', 'updated_at']
        read_only_fields = ['applied_at', 'updated_at']
