from django.urls import path

from apps.listings.views import ListingCreateView, ListingDestroyView, ListingListView, ListingUpdateView

urlpatterns = [
    path('', ListingListView.as_view(), name='listings_list'),
    path('/create', ListingCreateView.as_view(), name='listings_create'),
    path('/update/<int:pk>/listing', ListingUpdateView.as_view(), name='listing_update'),
    path('/delete/<int:pk>/listing', ListingDestroyView.as_view(), name='listings_delete'),
]