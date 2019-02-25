from rest_framework import viewsets, permissions
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, CurrencySerializer, CurrencyInfoSerializer
from .models import User, Currency
from rest_framework import status
from rest_framework.response import Response
from .models import Currency_info
from .methods import Methods
from django.views.decorators.csrf import csrf_exempt
from datetime import date


today = date.today()


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


    # def destroy(self, request):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_destroy(instance)
    #     return Response(status=status.HTTP_204_NO_CONTENT)






class CurrencyView(viewsets.ModelViewSet):
    queryset = Currency.objects.all().order_by('id')
    serializer_class = CurrencySerializer
    permission_classes = [AllowAny]




class CurrencyInfoView(viewsets.ModelViewSet):
    queryset = Currency_info.objects.all()
    serializer_class = CurrencyInfoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request):
        return self.service(request)

    def retrieve(self, request, currency_id):
        return self.service(request, currency_id)

    @staticmethod
    @csrf_exempt
    def service(request, currency_id=None):
        page_url = 'https://finance.naver.com/marketindex/worldExchangeList.nhn?key=exchange&page='
        pages = Methods.page(page_url)
        if currency_id == None:
            currency_infos = Currency_info.objects.filter(created_at__gte=today)
            if currency_infos.exists():
                result = Methods.currency_id_none_and_len_num(currency_infos, pages)
            else:
                result = Methods.currency_id_none_and_len_zero(pages)
        else:
            result = Methods.currency_id_not_1(currency_id, pages)
        return Response(result, status=status.HTTP_200_OK)