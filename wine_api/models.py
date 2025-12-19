from django.db import models


class Producer(models.Model):
    """Модель производителя вина"""
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", blank=True)

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"
        ordering = ['name']

    def __str__(self):
        return self.name


class WineCategory(models.Model):
    """Модель категории вина"""
    name = models.CharField(max_length=255, verbose_name="Название")

    class Meta:
        verbose_name = "Категория вина"
        verbose_name_plural = "Категории вин"
        ordering = ['name']

    def __str__(self):
        return self.name


class WineColor(models.Model):
    """Модель цвета вина"""
    name = models.CharField(max_length=255, verbose_name="Название")

    class Meta:
        verbose_name = "Цвет вина"
        verbose_name_plural = "Цвета вин"
        ordering = ['name']

    def __str__(self):
        return self.name


class WineSugar(models.Model):
    """Модель содержания сахара в вине"""
    name = models.CharField(max_length=255, verbose_name="Название")

    class Meta:
        verbose_name = "Содержание сахара"
        verbose_name_plural = "Содержание сахара"
        ordering = ['name']

    def __str__(self):
        return self.name


class Country(models.Model):
    """Модель страны"""
    name = models.CharField(max_length=255, verbose_name="Название")

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"
        ordering = ['name']

    def __str__(self):
        return self.name


class Region(models.Model):
    """Модель региона"""
    name = models.CharField(max_length=255, verbose_name="Название")

    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"
        ordering = ['name']

    def __str__(self):
        return self.name


class GrapeVariety(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название сорта")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Сорт винограда"
        verbose_name_plural = "Сорта винограда"
        ordering = ['name']


class Wine(models.Model):
    """Модель вина"""
    name = models.CharField(max_length=255, verbose_name="Название")
    image = models.ImageField(upload_to='wines/', verbose_name="Изображение", blank=True, null=True)
    saved = models.BooleanField(default=False, verbose_name="Сохранено")
    category = models.ForeignKey(WineCategory, on_delete=models.CASCADE, related_name='wines', verbose_name="Категория")
    sugar = models.ForeignKey(WineSugar, on_delete=models.CASCADE, related_name='wines', verbose_name="Содержание сахара")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='wines', verbose_name="Страна")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='wines', verbose_name="Регион")
    grape_varieties = models.ManyToManyField(
        GrapeVariety,
        through='WineGrapeComposition',
        related_name='wines'
    )
    volume = models.FloatField(verbose_name="Объем (л)")
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE, related_name='wines', verbose_name="Производитель")
    price = models.IntegerField(verbose_name="Цена", null=True, blank=True)
    aging = models.IntegerField(verbose_name="Год производства")
    description = models.TextField(verbose_name="Описание", blank=True)
    

    class Meta:
        verbose_name = "Вино"
        verbose_name_plural = "Вина"
        ordering = ['name']

    def __str__(self):
        return self.name


class WineGrapeComposition(models.Model):
    wine = models.ForeignKey(Wine, on_delete=models.CASCADE)
    grape_variety = models.ForeignKey(GrapeVariety, on_delete=models.CASCADE, verbose_name="Сорт винограда")
    percentage = models.PositiveIntegerField(
        verbose_name="Процент содержания",
        help_text="Процентное содержание сорта в вине"
    )
    
    class Meta:
        verbose_name = "Содержание сорта винограда в вине"
        verbose_name_plural = "Содержание сорта винограда в вине"
        constraints = [
            models.CheckConstraint(
                check=models.Q(percentage__lte=100),
                name='percentage_lte_100'
            ),
            models.UniqueConstraint(
                fields=['wine', 'grape_variety'],
                name='unique_wine_grape'
            )
        ]


class City(models.Model):
    """Модель города"""
    name = models.CharField(max_length=255, verbose_name="Название")

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
        ordering = ['name']

    def __str__(self):
        return self.name


class Event(models.Model):
    """Модель события"""
    name = models.CharField(max_length=255, verbose_name="Название")
    date = models.DateField(verbose_name="Дата")
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='events', verbose_name="Город")
    place = models.CharField(max_length=255, verbose_name="Место проведения")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    price = models.IntegerField(verbose_name="Цена билета")
    available = models.IntegerField(verbose_name="Доступно билетов")
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE, related_name='events', verbose_name="Производитель")
    image = models.ImageField(upload_to='events/', verbose_name="Изображение", blank=True, null=True)
    wine_list = models.ManyToManyField(Wine, related_name='events', verbose_name="Список вин", blank=True)

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "События"
        ordering = ['date', 'name']

    def __str__(self):
        return self.name

