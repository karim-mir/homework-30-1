from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "avatar", "phone", "city", "is_active")
        read_only_fields = ("is_active",)


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)  # Добавляем поле подтверждения пароля

    class Meta:
        model = User
        fields = ("id", "email", "password", "password2", "avatar", "phone", "city")

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Пароли не совпадают")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')  # Удаляем password2, он не нужен для создания пользователя
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)  # Устанавливаем пароль через set_password (хеширование)
        user.save()
        return user
