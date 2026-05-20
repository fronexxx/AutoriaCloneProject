from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.users.permissions import IsAdmin, IsManager
from apps.users.roles_and_account_type import Role
from apps.users.serializers import UserAdminSerializer, UserSerializer

UserModel = get_user_model()


class UserListView(ListAPIView):
    permission_classes = [IsAdmin | IsManager]
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class UserCreateView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class UserToManagerView(GenericAPIView):
    permission_classes = (IsAdmin,)

    def get_queryset(self):
        return UserModel.objects.exclude(id=self.request.user.id)

    def patch(self, *args, **kwargs):
        user = self.get_object()
        if not user.is_staff:
            if not user.previous_role:
                user.previous_role = user.role
            user.is_staff = True
            user.role = Role.MANAGER
            user.save()

        serializer = UserAdminSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class ManagerToUserView(GenericAPIView):
    permission_classes = (IsAdmin,)

    def get_queryset(self):
        return UserModel.objects.exclude(id=self.request.user.id)

    def patch(self, *args, **kwargs):
        user = self.get_object()
        if user.is_staff:
            user.is_staff = False
            user.role = user.previous_role or Role.BUYER
            user.previous_role = None
            user.save()

        serializer = UserAdminSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class BlockUserView(GenericAPIView):
    permission_classes = [IsAdmin | IsManager]

    def get_queryset(self):
        return UserModel.objects.exclude(id=self.request.user.id)

    def patch(self, *args, **kwargs):
        user = self.get_object()
        if user.is_active:
            user.is_active = False
            user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class UnBlockUserView(GenericAPIView):
    permission_classes = [IsAdmin | IsManager]

    def get_queryset(self):
        return UserModel.objects.exclude(id=self.request.user.id)

    def patch(self, *args, **kwargs):
        user = self.get_object()
        if not user.is_active:
            user.is_active = True
            user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)
