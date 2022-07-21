from bs4 import BeautifulSoup
import requests as req
from datetime import datetime
import csv
from mainapp.models import Product, Category

url = 'https://www.pyramex.net/category/ballisticheskie-takticheskie-ochki/?page='


def testing_mod_db_conn(request):
    # cat_name_text = [
    #     'Стрелковые очки',
    #     'Тактические очки',
    #     'Со сменными линзами',
    #     'Очки с диоптриями',
    #     'Тактические перчатки',
    #     'Беруши и наушники',
    #     'Наборы',
    #     'Аксессуары для очков',
    #     'Балаклава',
    #     'Жилеты светоотражающие',
    #     ]
    return 'response'
    # # Category.objects.all().delete()
    # Product.objects.all().delete()
    #
    # for cat in cat_name_text:
    #     Category.objects.create(
    #         name=cat,
    #         description=f'Описание категории {cat}',
    #     )

    # Category.objects.create(
    #     name='name_text_my_7',
    #     description='description_text_my_7',
    # )
    # # [names[i], arts[i], prices[i], lowprices[i], img_descs[i], links[i], img_hrefs[i]]

    # Product.objects.create(
    #     category=Category.objects.filter(name__icontains='name_text_my_7').first(),
    #     name='Название',
    #     product_code='Название',  # По-русски: АРТИКУЛ!!!
    #     description='Описание',
    #     price='590',
    #     price_our='540',
    #     link_text='https://www.pyramex.net/mini-intruder-s4110snmp/',
    #     link_img='https://www.pyramex.net/wa-data/public/shop/products/45/04/445/images/1281/1281.750.jpg',
    # )


def goParse():
    try:
        t_date = datetime.now().strftime("%d-%m-%y__%H-%M-%S")
    except:
        t_date = 555
    names = []
    prices = []
    lowprices = []
    links = []
    categories_url = [
        'https://www.pyramex.net/category/ballisticheskie-strelkovye-ochki',
        'https://www.pyramex.net/category/ballisticheskie-takticheskie-ochki',
        'https://www.pyramex.net/category/ochki-so-smennymi-linzami-pyramex',
        'https://www.pyramex.net/category/takticheskie-ochki-s-dioptriyami',
        'https://www.pyramex.net/category/takticheskie-perchatki',
        'https://www.pyramex.net/category/berushi-pyramex',
        'https://www.pyramex.net/category/nabory-naushniki--ochki-pyramex',
        'https://www.pyramex.net/category/chekhly-dlya-ochkov-pyramex',
        'https://www.pyramex.net/category/ekipirovka/balaklava',
        'https://www.pyramex.net/category/ekipirovka/zhilety-svetootrazhayushchi'
    ]


    for url in categories_url:  # ВЫБОР КАТЕГОРИИ
        print(f'Current category: {str(url).replace("https://www.pyramex.net/category/", "")}')
        for counter in range(10):
            print('page = ' + str(counter + 1))
            HEADERS = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.267 (Edition Yx GX)'
            }
            res = req.get(url + '/?page=' + str(counter + 1), headers=HEADERS)
            html = BeautifulSoup(res.text, 'lxml')
            try:
                if 'В этой к' in html.find('div', id="product-list").text:
                    print(f'with #{counter+1} no pages left')
                    break
            except:
                pass

            for name in html.find_all('h5'):
                names.append(name.find().get_text(strip=True).replace(',', ''))

            for price in html.find_all('div', class_='price-wrapper'):
                prc1 = price.find().get_text(strip=True)
                prc1 = prc1.replace("₽", "")  # убираю знак рубля
                prc1 = prc1.replace(" ", "")  # убираю пробел между разрядами
                prices.append(int(prc1))
                lowprices.append(int(round(int(prc1) * 0.91, -1)))  # округление+коэфф цен

            for link in html.find_all('div', class_='pl-item-info-expandable'):
                links.append('https://www.pyramex.net' + str(link.a['href']))
            print('done')

        tail = str(int(categories_url.index(url)) + 1)
        print('tail = ' + tail)

        # Вызов обхода за артикулами
    arts, img_hrefs, img_descs = Parse_artikul(links)
    print(len(names))
    print(len(arts))
    print(len(img_hrefs))


    with open(f"media/download_csv/parse_pmx_{t_date}.csv", "a", newline='', encoding='cp1251') as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(
            ["Наименование", "Артикул", "Цена Pyramex", "Наша цена", "Описание", "Ссылка", "Ссылка на изображение"]
        )
        for i, val in enumerate(names, start=0):
            writer.writerow(
                    [names[i], arts[i], prices[i], lowprices[i], img_descs[i], links[i], img_hrefs[i]]
            )
            Product.objects.create(
                    category=Category.objects.filter(name__icontains='Стрелковые очки').first(),
                    name=names[i],
                    product_code=arts[i],  # По-русски: АРТИКУЛ!!!
                    description=img_descs[i],
                    price=prices[i],
                    price_our=lowprices[i],
                    link_text=links[i],
                    link_img=img_hrefs[i],
                )
    print(f'\nfile created "{f.name}"')



def Parse_artikul(links):
    arts = []
    img_hrefs = []
    img_descs = []
    for i, val in enumerate(links):
        url_module = links[i]

        print('item number = \t' + str(i + 1) + '  ||  ' + url_module)
        HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.267 (Edition Yx GX)'
        }
        res = req.get(url_module, headers=HEADERS)
        html_arts = BeautifulSoup(res.text, 'lxml')

        for art in html_arts.find('span', class_='value-article'):
            arts.append(str(art.text))

        for img_href in html_arts.find_all('img', id="product-image"):
            img_hrefs.append('https://www.pyramex.net' + img_href.attrs['src'])
            try:
                img_descs.append(img_href.attrs['title'])
            except:
                pass

    print('module done, href_len =', len(img_hrefs))
    return arts, img_hrefs, img_descs


print('GREATER SUCCESS')
