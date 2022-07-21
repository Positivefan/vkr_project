from django.shortcuts import render
from django.http import HttpResponse
from mainapp.models import Product, Category
import mainapp.parce_pmx
import csv


def index(request):

    context = {
    }

    return render(request, 'mainapp/index.html', context)


def contact(request):
    return render(request, 'mainapp/contact.html')

def test_parse(request):
    mainapp.parce_pmx.goParse()

    context = {
    }

    return render(request, 'mainapp/index_waiting.html', context)

def export(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(["Наименование", "Артикул", "Цена Pyramex", "Наша цена", "Описание", "Ссылка", "Ссылка на изображение"])
    for product in Product.objects.all().values_list('name', 'product_code', 'price', 'price_our', 'description', 'link_text', 'link_img'):
        writer.writerow(product)

    response['Content-Disposition'] = 'attachment; filename="parse_pmx_17-06-22__10-18-21.csv'

    return response
        # category = Category.objects.filter(name__icontains='Стрелковые очки').first(),
        # name = names[i],
        # product_code = arts[i],  # По-русски: АРТИКУЛ!!!
        # description = img_descs[i],
        # price = prices[i],
        # price_our = lowprices[i],
        # link_text = links[i],
        # link_img = img_hrefs[i],

def test_add(request):

    a = mainapp.parce_pmx.testing_mod_db_conn(request)


    context = {
        'my_name_is': {
            '2': a,
            '3': '22',
        }
    }
    test_add2
    return render(request, 'mainapp/index_waiting.html', context)
def test_add2(request):
    context = {


        }
    return render(request, 'mainapp/index_ready.html', context)


