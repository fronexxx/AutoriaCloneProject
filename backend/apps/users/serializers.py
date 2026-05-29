from django.contrib.auth import get_user_model
from django.db.transaction import atomic

from rest_framework import serializers

from core.services.email_service import EmailService

from apps.users.models import CustomUserModel, PaymentModel, ProfileModel

from .models import Role

UserModel = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = (
            'id',
            'name',
            'surname',
            'phone_number',
            'created_at',
            'updated_at',
        )

    def validate_phone_number(self, value: str):

        if value.startswith('0'):
            value = '+38' + value

        return value

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = UserModel
        fields = (
            'id',
            'email',
            'password',
            'role',
            'account_type',
            'is_active',
            'is_staff',
            'is_superuser',
            'created_at',
            'updated_at',
            'profile',
        )
        read_only_fields = ('id', 'account_type', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'created_at', 'updated_at')
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'role': {
                'error_messages': {
                        'required': 'This field is required and you can choose either `buyer` or `seller` role'
                    }
            }
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.role in (Role.ADMIN, Role.MANAGER):
            data.pop('account_type', None)
        return data

    @staticmethod
    def validate_role(value):
        allowed = [Role.BUYER, Role.SELLER]

        if value not in allowed:
            raise serializers.ValidationError('You can choose either buyer or seller role')

        return value

    @atomic
    def create(self, validated_data: dict):
        profile = validated_data.pop('profile')
        user = UserModel.objects.create_user(**validated_data)
        ProfileModel.objects.create(**profile, user=user)
        EmailService.register(user)
        return user

class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = (
            'id',
            'email',
            'role',
            'is_staff',
        )

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentModel
        fields = (
            'id',
            'amount',
            'status'
        )
        read_only_fields = (
            'id',
            'amount',
            'status'
        )