from django.db import models

from users.models import User


class Tags(models.Model):
    """Модель тегов."""
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
        # unique=True,
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
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='recipes',
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
        through='IngredientsInRecipe',
        related_name='recipes',
        help_text='Выберите ингридиенты',
        blank=False,
    )
    tags = models.ManyToManyField(
        Tags,
        related_name='recipes',
        help_text='Введите тег',
        blank=False,
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


class IngredientsInRecipe(models.Model):
    """Модель ингредиентов в рецепте."""
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    amount = models.IntegerField(
        verbose_name='Количество',
        blank=False,
        null=True,
        help_text='Введите количество ингридиента'
    )

    class Meta:
        verbose_name = ("Ингредиент в рецепте")
        verbose_name_plural = ("Ингредиенты в рецепте")

    def __str__(self):
        return f'{self.ingredient} в {self.recipe}'


class Follows(models.Model):
    """Модель подписок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )
    following_date = models.DateTimeField(
        'Дата подписки',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = ("Подписка")
        verbose_name_plural = ("Подписки")

    def __str__(self):
        return f'{self.user} подписан на {self.author}'


class Favorites(models.Model):
    """Модель избранных."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='favorites',
    )

    class Meta:
        verbose_name = ("Избранное")
        verbose_name_plural = ("Избранное")

    def __str__(self):
        return f'Рецепт {self.recipe} в избранном у {self.user}'


class Carts(models.Model):
    """Модель списков покупок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='carts',
    )
    recipes = models.ForeignKey(
        Recipes,
        related_name='cart',
        verbose_name='Рецепты',
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField(
        'Дата создания списка',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = ("Список покупок")
        verbose_name_plural = ("Списки покупок")

    def __str__(self):
        return f'Список покупок пользователя {self.user}'
