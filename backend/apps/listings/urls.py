from django.urls import path

from apps.listings.views import ListingCreateView, ListingListView

urlpatterns = [
    path('', ListingListView.as_view(), name='listings_list'),
    path('/create', ListingCreateView.as_view(), name='listings_create'),
]