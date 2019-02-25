from .models import User, Currency, Currency_info
from rest_framework import serializers
from werkzeug.security import generate_password_hash
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')



    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            password=make_password(validated_data['password'])
        )
        return user



class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('id', 'name')



class CurrencyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency_info
        fields = ('currency_id', 'name', 'symbol', 'current_price', 'comparing_yesterday', 'change', 'created_at')



