from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from typing import Any, Dict
from v1.user.models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        res = super().validate(attrs)
        res['user'] = {
            'id': self.user.id,
            'phone': self.user.phone,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
        }
        return res


class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'password', 'password1')

    def validate(self, attrs):
        password1 = attrs.pop('password1')
        password = attrs.get('password')
        if password1 != password:
            raise serializers.ValidationError('Parol birxil emas')
        User.objects.create_user(**attrs)
        return attrs
