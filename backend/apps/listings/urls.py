from django.urls import path

from apps.listings.views import (
    ListingCreateView,
    ListingDestroyView,
    ListingUpdateView,
    PrivateListingListView,
    PrivateListingRetrieveView,
    PublicListingListView,
    PublicListingRetrieveView,
)

urlpatterns = [
    path('', PublicListingListView.as_view(), name='listings_list'),
    path('/private', PrivateListingListView.as_view(), name='listings_list_private'), 
    path('/create', ListingCreateView.as_view(), name='listings_create'),
    path('/update/<int:pk>/listing', ListingUpdateView.as_view(), name='listing_update'),
    path('/delete/<int:pk>/listing', ListingDestroyView.as_view(), name='listings_delete'),
    path('/get/<int:pk>/private', PrivateListingRetrieveView.as_view(), name='listings_get_by_id_private'),
    path('/get/<int:pk>/public', PublicListingRetrieveView.as_view(), name='listings_get_by_id_public'),
]