from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'profile',
            'first_name',
            'last_name',
        )
        read_only_fields = ('email',)


# class PasswordSetSerializer(serializers.Serializer):
#     password = serializers.CharField()
#     password_confirm = serializers.CharField()

#     def validate(self, attrs):
#         user = self.context['request'].user

#         if attrs['password'] != attrs['password_confirm']:
#             raise serializers.ValidationError({
#                 'password': 'Password not match.',
#                 'password_confirm': 'Password not match.',
#             })

#         try:
#             validate_password(attrs['password'], user)
#         except ValidationError as e:
#             raise serializers.ValidationError({
#                 'password': e.messages,
#             })

#         return attrs


# class PasswordResetSerializer(serializers.Serializer):
#     email = serializers.EmailField()
