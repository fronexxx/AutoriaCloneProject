from django.urls import path

from apps.users.views import (
    BlockUserView,
    ManagerToUserView,
    UnBlockUserView,
    UserCreateView,
    UserListView,
    UserToManagerView,
)

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('/create', UserCreateView.as_view(), name='user_create'),
    path('/<int:pk>/to_manager', UserToManagerView.as_view(), name='user_to_manager'),
    path('/<int:pk>/to_user', ManagerToUserView.as_view(), name='manager_to_user'),
    path('/<int:pk>/block', BlockUserView.as_view(), name='user_block'),
    path('/<int:pk>/unblock', UnBlockUserView.as_view(), name='user_unblock'),
]
