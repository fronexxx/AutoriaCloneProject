from django.http import Http404

from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.constants.choices import StatusChoices
from core.services.currency_service import CurrencyService
from core.services.listings_service import ListingsService

from apps.listings.models import ListingModel, ListingStatsModel
from apps.listings.serializer import ListingCreateUpdateDeleteSerializer, ListingDetailSerializer, ListingSerializer
from apps.users.permissions import IsSeller


class PublicListingListView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ListingSerializer
    queryset = ListingModel.objects.filter(
        status=StatusChoices.ACTIVE
    )


class PrivateListingListView(ListAPIView):
    permission_classes = (IsSeller,)
    serializer_class = ListingDetailSerializer

    def get_queryset(self):
        return ListingModel.objects.filter(
            owner=self.request.user
        )


class PublicListingRetrieveView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ListingSerializer
    queryset = ListingModel.objects.filter(
        status=StatusChoices.ACTIVE
    )

    def get(self, *args, **kwargs):
        listing = self.get_object()
        ListingsService.stats_handler(listing, user=self.request.user)

        serializer = self.get_serializer(listing)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PrivateListingRetrieveView(RetrieveAPIView):
    permission_classes = (IsSeller,)
    serializer_class = ListingDetailSerializer
    queryset = ListingModel.objects.all()


class ListingCreateView(GenericAPIView):
    permission_classes = (IsSeller,)
    serializer_class = ListingCreateUpdateDeleteSerializer

    def post(self, *args, **kwargs):
        data = self.request.data
        rates = CurrencyService.get_exchange_rates()
        serializer = ListingCreateUpdateDeleteSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        converted_price = CurrencyService.convert_price(
            price=serializer.validated_data['price'],
            currency=serializer.validated_data['currency'],
            exchange_rate=rates
        )

        listing = serializer.save(owner=self.request.user, exchange_rate=rates, price_converted=converted_price)
        ListingStatsModel.objects.create(listing=listing)

        ListingsService.profanity_validation(listing)

        response_serializer = ListingSerializer(listing)

        attempts_left = 3 - listing.edit_attempts

        if listing.status == StatusChoices.ACTIVE:
            return Response(
                {
                    'message':
                        'Listing created successfully.',
                    'listing': response_serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        elif listing.status == StatusChoices.PENDING:
            return Response(
                {
                    'message': (
                        'Profanity detected.'
                        f'You have {attempts_left} attempts to correct'
                    ),
                    'listing': response_serializer.data
                },
                status=status.HTTP_201_CREATED
            )


class ListingUpdateView(GenericAPIView):
    permission_classes = (IsSeller,)
    queryset = ListingModel.objects.all()
    http_method_names = ['patch']

    def patch(self, *args, **kwargs):
        try:
            listing = self.get_object()
        except Http404:
            raise NotFound('Listing does not exist')
        data = self.request.data
        rates = CurrencyService.get_exchange_rates()

        if listing.status == StatusChoices.INACTIVE:
            return Response(
                {
                    'message': (
                        'Listing blocked due to profanity. '
                        'Manager has been notified.')
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ListingCreateUpdateDeleteSerializer(listing, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        converted_price = CurrencyService.convert_price(
            price=serializer.validated_data['price'],
            currency=serializer.validated_data['currency'],
            exchange_rate=rates
        )

        listing = serializer.save(exchange_rate=rates, price_converted=converted_price)

        ListingsService.profanity_validation(listing)

        response_serializer = ListingSerializer(listing)

        attempts_left = 3 - listing.edit_attempts

        if listing.status == StatusChoices.ACTIVE:
            return Response(
                {
                    'message':
                        'Listing updated successfully.',
                    'listing': response_serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        elif listing.status == StatusChoices.PENDING:
            return Response(
                {
                    'message': (
                        'Profanity detected.'
                        f'You have {attempts_left} attempts to correct'
                    ),
                    'listing': response_serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'message': (
                    'Listing blocked due to profanity. '
                    'Manager has been notified.'),
                'listing': response_serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class ListingDestroyView(GenericAPIView):
    permission_classes = (IsSeller,)
    queryset = ListingModel.objects.all()

    def delete(self, *args, **kwargs):
        try:
            listing = self.get_object()
        except Http404:
            raise NotFound('Listing does not exist')

        listing.delete()

        return Response({'details': 'Listing has been deleted'}, status=status.HTTP_204_NO_CONTENT)
