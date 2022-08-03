from django.db import models

from users.models import User


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
        return f'{self.name}, измеряется в {self.measurement_unit}'


class Recipes(models.Model):
    """Модель рецептов."""
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='author',
        verbose_name='Автор',
        help_text='Выберите автора',
        blank=False,
        null=True,
    )
    name = models.CharField(
        verbose_name='Название',
        help_text='Введите название блюда',
        max_length=200,
        blank=False,
    )
    image = models.ImageField(
        verbose_name='Изображение',
    )
    text = models.TextField(
        verbose_name='Описание',
        help_text='Введите описание рецепта',
        blank=False,
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        related_name='ingredients',
        help_text='Выберите ингридиенты',
        blank=False,
    )
    tags = models.ManyToManyField(
        Tags,
        related_name='tags',
        help_text='Введите тег',
        blank=False,
        through='Ingredients_in_recipe',
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        help_text='Введите время приготовления в минутах',
        blank=False,
        null=True,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Ingredients_in_recipe(models.Model):
    """Модель ингредиентов в рецепте."""
    ingredients = models.ForeignKey(
        Ingredients,
        on_delete=models.SET_NULL,
        related_name='ingredients',
        verbose_name='Ингредиенты',
    )
    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Рецепты',
    )
    amount = models.IntegerField(
        verbose_name='Количество',
        blank=False,
        null=True,
        help_text='Введите количество ингридиента'
    )
