from django.db import models


class Tags(models.Model):
    """Модель тегов"""
    name = models.CharField(
        verbose_name='Название',
        help_text='Введите название тега',
        max_length=200,
        blank=False,
        unique=True,
        db_index=True,
    )
    color = models.CharField(
        verbose_name='Цвет(HEX-код)',
        help_text='Введите цветовой HEX-код(например, #49B64E)',
        max_length=16,
        blank=False,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        help_text='Введите слаг',
        blank=False,
        unique=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    """Модель ингредиентов."""
    name = models.CharField(
        verbose_name='Название',
        help_text='Введите название ингредиента',
        max_length=200,
        blank=False,
        unique=True,
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        help_text='Введите единицу измерения',
        max_length=200,
        blank=False,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipes(models.Model):
    """Модель рецептов."""
    ingredients = models.ManyToManyField(
        Ingredients,
        related_name='ingredients',
    )
    tags = models.ManyToManyField(
        Tags,
        related_name='tags',
    )
    image = models.ImageField(
        verbose_name='Изображение',
    )
    name = models.CharField(
        verbose_name='Название',
        help_text='Введите название рецепта',
        max_length=200)
    text = models.TextField(
        verbose_name='Описание',
        
    )
    cooking_time = models.IntegerField