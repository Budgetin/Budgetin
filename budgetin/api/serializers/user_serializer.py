from rest_framework import serializers

from api.models import User

class UserSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField()
    updated_by = serializers.CharField()
    is_active = serializers.IntegerField()
    class Meta:
        model = User
        fields = '__all__'
