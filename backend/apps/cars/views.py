from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cars.models import BrandModel, CarModel
from apps.cars.serializer import BrandSerializer, CarSerializer
from apps.users.permissions import IsAdmin, IsManager


class ListCarsView(ListAPIView):
    permission_classes = (AllowAny, )
    queryset = BrandModel.objects.all()
    serializer_class = BrandSerializer

class CreateCarView(CreateAPIView):
    permission_classes = [IsAdmin | IsManager]
    serializer_class = CarSerializer

class ListModelByBrandView(APIView):
    def get(self, *args, **kwargs):
        pk = kwargs['pk']

        try:
            brand = BrandModel.objects.get(pk=pk)
        except CarModel.DoesNotExist:
            return Response({'details': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BrandSerializer(brand)
        return Response(serializer.data, status.HTTP_200_OK)






    

