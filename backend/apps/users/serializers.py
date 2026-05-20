from django.contrib.auth import get_user_model

from rest_framework import serializers

from apps.users.models import CustomUserModel, ProfileModel

from .models import Role

UserModel = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = (
            'id',
            'name',
            'surname',
            'created_at',
            'updated_at'
        )


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

    def create(self, validated_data: dict):
        profile = validated_data.pop('profile')
        user = UserModel.objects.create_user(**validated_data)
        ProfileModel.objects.create(**profile, user=user)
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