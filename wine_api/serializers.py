from rest_framework import serializers
from .models import (
    Producer, WineCategory, WineSugar, Country, Region,
    Wine, City, Event
)


class ProducerSerializer(serializers.ModelSerializer):
    """Сериализатор для Producer (используется во вложенных объектах)"""
    class Meta:
        model = Producer
        fields = ['id', 'name', 'description']


class WineCategorySerializer(serializers.ModelSerializer):
    """Сериализатор для WineCategory (используется во вложенных объектах)"""
    class Meta:
        model = WineCategory
        fields = ['id', 'name']


class WineSugarSerializer(serializers.ModelSerializer):
    """Сериализатор для WineSugar (используется во вложенных объектах)"""
    class Meta:
        model = WineSugar
        fields = ['id', 'name']


class CountrySerializer(serializers.ModelSerializer):
    """Сериализатор для Country (используется во вложенных объектах)"""
    class Meta:
        model = Country
        fields = ['id', 'name']


class RegionSerializer(serializers.ModelSerializer):
    """Сериализатор для Region (используется во вложенных объектах)"""
    class Meta:
        model = Region
        fields = ['id', 'name']


class CitySerializer(serializers.ModelSerializer):
    """Сериализатор для City (используется во вложенных объектах)"""
    class Meta:
        model = City
        fields = ['id', 'name']


class WineSerializer(serializers.ModelSerializer):
    """Сериализатор для Wine с вложенными объектами"""
    producer = ProducerSerializer(read_only=True)
    category = WineCategorySerializer(read_only=True)
    sugar = WineSugarSerializer(read_only=True)
    country = CountrySerializer(read_only=True)
    region = RegionSerializer(read_only=True)

    class Meta:
        model = Wine
        fields = [
            'id', 'name', 'image', 'saved', 'category', 'sugar',
            'country', 'region', 'volume', 'producer', 'price',
            'aging', 'description'
        ]


class EventSerializer(serializers.ModelSerializer):
    """Сериализатор для Event с вложенными объектами"""
    city = CitySerializer(read_only=True)
    producer = ProducerSerializer(read_only=True)
    wine_list = WineSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'name', 'date', 'city', 'place', 'address',
            'price', 'available', 'producer', 'image', 'wine_list'
        ]

