# Generated by Django 2.2.19 on 2022-08-08 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20220806_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carts',
            name='recipes',
            field=models.ManyToManyField(related_name='cart', to='recipes.Recipes', verbose_name='Рецепты'),
        ),
    ]
