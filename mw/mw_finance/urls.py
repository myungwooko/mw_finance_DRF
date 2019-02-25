from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import UserView, CurrencyView, CurrencyInfoView




user_signup = UserView.as_view({
    'post': 'create',
})

menu_list = CurrencyView.as_view({
    'get': 'list'
})

currency_all = CurrencyInfoView.as_view({
    'get': 'list',
})

currency_item = CurrencyInfoView.as_view({
    'get': 'retrieve'
})




urlpatterns = format_suffix_patterns([
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('signup/', user_signup, name='user_signup'),
    path('menu/', menu_list, name='menu_list'),
    path('', currency_all, name='currency_all'),
    path('<int:currency_id>/', currency_item, name='currency_item'),
])

