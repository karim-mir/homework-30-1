from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'avatar', 'phone', 'city', 'is_active')
        read_only_fields = ('is_active',)
