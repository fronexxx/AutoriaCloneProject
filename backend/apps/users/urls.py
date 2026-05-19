from django.urls import path

from apps.users.views import ManagerToUserView, UserListCreateView, UserToManagerView

urlpatterns = [
    path('', UserListCreateView.as_view(), name='user_list_create'),
    path('/<int:pk>/to_manager', UserToManagerView.as_view(), name='user_to_manager'),
    path('/<int:pk>/to_user', ManagerToUserView.as_view(), name='manager_to_user'),
]
