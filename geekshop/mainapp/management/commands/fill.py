import json

from django.core.management import BaseCommand
from django.conf import settings

from mainapp.models import Category, Product
from authapp.models import ShopUser


class Command(BaseCommand):

    @staticmethod
    def _load_data_from_file(file_name):
        with open(f'{settings.BASE_DIR}/mainapp/json/{file_name}.json', 'r', encoding='utf-8') as json_file:
            # a = json.load(json_file)
            # print(a)

            return json.load(json_file)


    def handle(self, *args, **options):
        Category.objects.all().delete()

        categories_list = self._load_data_from_file('categories')
        categories_batch = []
        for cat in categories_list:
            categories_batch.append(
                Category(
                    name=cat.get('name'),
                    description=cat.get('description')
                )
            )

        Category.objects.bulk_create(categories_batch)
        print(Category.objects.all())

        Product.objects.all().delete()
        product_list = self._load_data_from_file('product')
        for prod in product_list:
            print(prod.get('category'))
            _cat = Category.objects.filter(name__icontains=prod.get('category')).first()
            print(_cat)
            prod['category'] = _cat

            Product.objects.create(**prod)

        print('Товары:', Product.objects.all())

        shop_user = ShopUser.objects.create_superuser(username='django', email='django@gb.local', age=26)
        shop_user.set_password('geekbrains')
        shop_user.save()
