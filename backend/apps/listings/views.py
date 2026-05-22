from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.listings.models import ListingModel
from apps.listings.serializer import ListingCreateSerializer, ListingSerializer


class ListingListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ListingSerializer
    queryset = ListingModel.objects.all()

class ListingCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ListingCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
