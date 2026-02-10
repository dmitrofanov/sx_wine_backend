from rest_framework import serializers
from .models import (
    Producer, WineCategory, WineSugar, Country, Region,
    Wine, City, Event, GrapeVariety, WineGrapeComposition,
    PersonGrade, Person, WineColor
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
    
class WineColorSerializer(serializers.ModelSerializer):
    """Сериализатор для WineColor (используется во вложенных объектах)"""
    class Meta:
        model = WineColor
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


class GrapeVarietySerializer(serializers.ModelSerializer):
    class Meta:
        model = GrapeVariety
        fields = ['id', 'name']


class WineGrapeCompositionSerializer(serializers.ModelSerializer):
    # Option A: Include full grape variety object
    # grape_variety = GrapeVarietySerializer(read_only=True)
    
    # Option B: Just include the name (matches your frontend structure)
    name = serializers.CharField(source='grape_variety.name', read_only=True)
    
    class Meta:
        model = WineGrapeComposition
        fields = ['name', 'percentage']  # For Option B
        # OR fields = ['grape_variety', 'percentage']  # For Option A

    
class WineSerializer(serializers.ModelSerializer):
    """Сериализатор для Wine с вложенными объектами"""
    producer = ProducerSerializer(read_only=True)
    category = WineCategorySerializer(read_only=True)
    sugar = WineSugarSerializer(read_only=True)
    color = WineColorSerializer(read_only=True)
    country = CountrySerializer(read_only=True)
    region = RegionSerializer(read_only=True)
    grape_variety = WineGrapeCompositionSerializer(
        source='winegrapecomposition_set',  # Default related_name
        many=True,
        read_only=True
    )

    class Meta:
        model = Wine
        fields = [
            'id', 'name', 'full_name', 'image', 'category', 'sugar', 'color',
            'country', 'region', 'volume', 'producer', 'price',
            'aging', 'aging_caption', 'description', 'grape_variety', 'sur_lie_years', 'sur_lie_months'   
        ]


class EventSerializer(serializers.ModelSerializer):
    """Сериализатор для Event с вложенными объектами"""
    city = CitySerializer(read_only=True)
    producer = ProducerSerializer(read_only=True)
    wine_list = WineSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'name', 'date', 'time', 'city', 'place', 'address',
            'price', 'available', 'producer', 'image', 'wine_list', 'participants'
        ]


class PersonGradeSerializer(serializers.ModelSerializer):
    """Сериализатор для PersonGrade (используется во вложенных объектах)"""
    class Meta:
        model = PersonGrade
        fields = ['id', 'name']


class PersonSerializer(serializers.ModelSerializer):
    """Сериализатор для Person"""
    grade = PersonGradeSerializer(read_only=True)
    grade_id = serializers.PrimaryKeyRelatedField(
        queryset=PersonGrade.objects.all(),
        source='grade',
        write_only=True
    )

    class Meta:
        model = Person
        fields = [
            'id',
            'nickname',
            'phone',
            'firstname',
            'lastname',
            'grade',
            'grade_id',
            'telegram_id',
            # 'key',
        ]
        # extra_kwargs = {
        #     'key': {'read_only': True},
        # }

