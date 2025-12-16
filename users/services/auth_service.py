from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from users.models import User

class AuthService:
    @staticmethod
    def login(email, password):
        user = authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials")
        return user

    @staticmethod
    def register(validated_data):
        return User.objects.create_user(**validated_data)