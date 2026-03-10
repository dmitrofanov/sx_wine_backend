from django.contrib import admin
from .models import (
    Producer, WineCategory, WineColor, WineSugar,
    Country, Region, Wine, City, Event, GrapeVariety, WineGrapeComposition,
    PersonGrade, Person, Feature, Subscription
)


@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']


@admin.register(WineCategory)
class WineCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(WineColor)
class WineColorAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(WineSugar)
class WineSugarAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class WineGrapeCompositionInline(admin.TabularInline):
    model = WineGrapeComposition
    extra = 1  # Number of empty forms to display
    autocomplete_fields = ['grape_variety']  # If you have many grape varieties


@admin.register(Wine)
class WineAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'producer', 'category', 'country', 'price', 'get_grape_varieties']
    inlines = [WineGrapeCompositionInline]
    list_filter = ['category', 'sugar', 'country', 'region', 'producer']
    search_fields = ['name', 'producer__name', 'aging', 'aging_caption']
    filter_horizontal = []
    readonly_fields = ['full_name']
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'full_name', 'image', 'description')
        }),
        ('Характеристики', {
            'fields': ('category', 'sugar', 'color', 'volume', 'aging', 'aging_caption')
        }),
        ('Происхождение', {
            'fields': ('country', 'region', 'producer')
        }),
        ('Цена', {
            'fields': ('price',)
        }),
        ('Выдержка на осадке', {
            'fields': ('sur_lie_years', 'sur_lie_months')
        }),
    )

    def full_name(self, obj):
        """Отображение составного имени в списке"""
        return obj.full_name
    full_name.short_description = "Полное название"

    def get_grape_varieties(self, obj):
        """Display grape varieties in list view"""
        compositions = obj.winegrapecomposition_set.all()
        return ", ".join([f"{c.grape_variety.name} ({c.percentage}%)" for c in compositions])
    get_grape_varieties.short_description = "Сорта винограда"


@admin.register(GrapeVariety)
class GrapeVarietyAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

# @admin.register(WineGrapeComposition)
# class WineGrapeCompositionAdmin(admin.ModelAdmin):
#     list_display = ['wine', 'grape_variety', 'percentage']
#     list_filter = ['grape_variety']
#     search_fields = ['wine__name', 'grape_variety__name']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'time', 'city', 'place', 'price', 'available']
    list_filter = ['city', 'producer', 'date']
    search_fields = ['name', 'place', 'address', 'date']
    filter_horizontal = ['wine_list', 'participants']
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'date', 'time', 'image')
        }),
        ('Место проведения', {
            'fields': ('city', 'place', 'address')
        }),
        ('Билеты', {
            'fields': ('price', 'available')
        }),
        ('Связанные объекты', {
            'fields': ('producer', 'wine_list', 'participants')
        }),
    )


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    list_filter = ['created_at']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'created_at', 'updated_at', 'get_features_count']
    search_fields = ['name', 'description']
    list_filter = ['created_at', 'price']
    filter_horizontal = ['features']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'price', 'duration')
        }),
        ('Фичи', {
            'fields': ('features',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def get_features_count(self, obj):
        return obj.features.count()
    get_features_count.short_description = "Количество фич"


@admin.register(PersonGrade)
class PersonGradeAdmin(admin.ModelAdmin):
    list_display = ['name', 'required_tastings', 'next_grade']
    search_fields = ['name']


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'firstname', 'lastname', 'phone', 'subscription', 'subscription_starts_at', 'get_grade', 'visited_tastings']
    list_filter = ['subscription']
    search_fields = ['nickname', 'firstname', 'lastname', 'phone']
    fieldsets = (
        ('Основная информация', {
            'fields': ('nickname', 'firstname', 'lastname', 'phone', 'telegram_id', 'key')
        }),
        ('Подписка', {
            'fields': ('is_gold_member', 'subscription', 'subscription_starts_at')
        }),
    )

    def get_grade(self, obj):
        return obj.grade.name if obj.grade else None

    get_grade.short_description = "Грейд"

