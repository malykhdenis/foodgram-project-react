import sys
from csv import DictReader
from os.path import exists
from django.contrib.staticfiles.finders import find
from django.core.management import BaseCommand
from recipes.models import Ingredient

DATA_MODEL = {
    'ingredients': Ingredient,
}


def delete_objects(model):
    """Удаление существующих элементов в базе."""
    model = model
    try:
        model.objects.all().delete()
        message = f'Существющие объекты {model.__name__} удалены.'
        return message
    except Exception as error:
        raise Exception(f'Ошибка при удалении объектов: {error}')


def check_db(model):
    """Проверка базы данных и удаление по запросу."""
    if model.objects.exists():
        print(f'В базе уже есть объекты {model.__name__}!')
        result = input('Для удаления введите "Y" или что-нибудь '
                       'другое для отмены и выхода: ')
        if result == 'Y' or result == 'y':
            return delete_objects(model)
        else:
            sys.exit(0)


def objects_creator(model, row):
    if model == Ingredient:
        Ingredient.objects.create(
            name=row['name'],
            measurement_unit=row['measurement_unit'],
        )


class Command(BaseCommand):
    """Command for load csv data to database."""
    def handle(self, *args, **options):
        for filename, model in DATA_MODEL.items():
            check_db(model)
            csv_file = find(f'data/{filename}.csv')
            print(csv_file)
            if exists(csv_file):
                try:
                    for row in DictReader(open(csv_file, encoding='utf-8')):
                        objects_creator(model, row)
                except Exception as error:
                    raise Exception(f'Ошибка добавления объекта: {error}')
            else:
                print(f'Файл {filename}.csv для заполнения '
                      f'{model.__name__} отсутвует.')

            print(f'{model.__name__}: новые объекты добавлены.')
