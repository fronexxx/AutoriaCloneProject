from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from .roles_and_account_type import AccountType, Role


class IsAdmin(BasePermission):
    def has_permission(self, request: Request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == Role.ADMIN
        )


class IsManager(BasePermission):
    def has_permission(self, request: Request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == Role.MANAGER
        )

class IsBuyer(BasePermission):
    def has_permission(self, request: Request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == Role.BUYER
        )

class IsSeller(BasePermission):
    def has_permission(self, request: Request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == Role.SELLER
        )

    def has_object_permission(self, request: Request, view, obj):
        return obj.owner == request.user

class IsBasicAccountType(BasePermission):
    def has_object_permission(self, request: Request, view, obj):
        return request.user.account_type == AccountType.BASIC

class IsPremiumAccountType(BasePermission):
    def has_object_permission(self, request: Request, view, obj):
        return request.user.account_type == AccountType.PREMIUM