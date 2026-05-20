from django.contrib import admin
from django.urls import path

from apps.cars.views import CarRequestView, CreateCarView, ListCarByBrandView, ListCarsView

urlpatterns = [
    path('', ListCarsView.as_view(), name='cars_list'),
    path('/create', CreateCarView.as_view(), name='cars_create'),
    path('/<int:pk>/brand', ListCarByBrandView.as_view(), name='cars_list_by_pk'),
    path('/request', CarRequestView.as_view(), name='cars_request'),
    path('/admin', admin.site.urls),
]
