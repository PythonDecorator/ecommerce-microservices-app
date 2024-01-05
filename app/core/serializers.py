"""
Serializers for the user API View.
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'password']
        extra_kwargs = {"password": {"write_only": True,
                                     "min_length": 8}
                        }

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        request = self.context.get('request')

        data = request.data

        if data['password'] != data['password1']:
            raise serializers.ValidationError('Passwords do not match!')

        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return a user with encrypted password."""

        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ["id", 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {"password": {"write_only": True, "min_length": 8},
                        "email": {"read_only": True},
                        "id": {"read_only": True}
                        }