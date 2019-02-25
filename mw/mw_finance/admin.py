from django.contrib import admin
from .models import User, Currency, Currency_info, Blacklist

admin.site.unregister(User)
# admin.site.register(User, User)


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username']

@admin.register(Blacklist)
class BlacklistAdmin(admin.ModelAdmin):
    list_display = ['id', 'short_token', 'created_at']

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Currency_info)
class CurrencyInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'symbol', 'current_price', 'comparing_yesterday', 'change',  'created_at']


