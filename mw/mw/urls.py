from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('mw_finance/', include('mw_finance.urls')),
]
