from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.services.email_service import EmailService

from apps.cars.models import BrandModel, CarModel
from apps.cars.serializer import BrandSerializer, CarRequestSerializer, CarSerializer
from apps.users.permissions import IsAdmin, IsManager


class ListCarsView(ListAPIView):
    permission_classes = (AllowAny, )
    queryset = BrandModel.objects.all()
    serializer_class = BrandSerializer

class CreateCarView(CreateAPIView):
    permission_classes = [IsAdmin | IsManager]
    serializer_class = BrandSerializer

class ListCarByBrandView(APIView):
    permission_classes = (AllowAny, )
    @staticmethod
    def get(*args, **kwargs):
        pk = kwargs['pk']

        try:
            brand = BrandModel.objects.get(pk=pk)
        except CarModel.DoesNotExist:
            return Response({'details': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BrandSerializer(brand)
        return Response(serializer.data, status.HTTP_200_OK)

class CarRequestView(APIView):
    permission_classes = (IsAuthenticated, )

    @staticmethod
    def post(request: Request):
        data = request.data

        serializer = CarRequestSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        EmailService.send_car_request(
            user=request.user,
            data=serializer.validated_data
        )
        return Response({'details': 'Email has been successfully sent'}, status.HTTP_200_OK)









    

