# Generated by Django 2.2.19 on 2022-08-15 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_remove_recipe_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания рецепта'),
        ),
    ]
