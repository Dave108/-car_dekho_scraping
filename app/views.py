from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import time


# Create your views here.

def homepage(request):
    return render(request, 'home.html')


def new_car_view(request):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/75.0.3770.80 Safari/537.36'}
    brand = request.GET.get('brand')
    context = None
    if brand:
        print(brand)
        car_dict = {}
        car_list = []
        url = 'https://www.cardekho.com{}'.format(brand)
        # time.sleep(5)
        html_text = requests.get(url, headers=headers)
        html_text = html_text.text
        soup = BeautifulSoup(html_text, 'lxml')
        # print(soup.prettify())
        cars_summary = soup.find("section", class_="TableINPageCon shadow24 withRating carSummary readMoreLess")
        # print(cars_summary.h1.text)
        cars_data = soup.find_all('li', class_="gsc_col-xs-12 gsc_col-sm-6 gsc_col-md-12 gsc_col-lg-12")
        # print(cars_data)
        for cars in cars_data:
            cars_image = cars.find('img')
            price = cars.find('div', class_="price")
            dotlist = cars.find('div', class_="dotlist")
            if cars_image:
                # print(price.text)
                # print(dotlist.text)
                # print(cars_image['src'])
                print(cars.a, '---***---***---***---***---***---***---***---***')
                car_dict = {"image_url": cars_image['src'], "car_name": cars.a.text, "price": price.text,
                            "dotlist": dotlist.text, "car_page": cars.a['href']}
                car_list.append(car_dict)
        # print(car_list)
        context = {
            "brand_name": cars_summary.h1.text,
            "brand_summary": cars_summary.p.text,
            "car_list": car_list,
        }
    else:
        url = 'https://www.cardekho.com/newcars'
        html_text = requests.get(url, headers=headers)
        html_text = html_text.text
        soup = BeautifulSoup(html_text, 'lxml')
        # print(soup, '------new car soup')
        brand_names = soup.find('ul', class_="listing gsc_row clearfix")
        brand_dict = {}
        brand_list = []
        for cars in brand_names:
            brand_image = cars.img['src']
            brand_name = cars.span.text
            brand_action = cars.a['href']
            print(brand_action)
            print(brand_name)
            print("----------------------------------------------")
            brand_dict = {"brand_image": brand_image, "brand_name": brand_name, "brand_action": brand_action}
            brand_list.append(brand_dict)
        context = {
            "brand_list": brand_list
        }
    return render(request, 'new_car.html', context)


def used_car_view(request):
    location = request.GET.get('location')
    car_list = None
    total_cars = None
    if location:
        print(location)
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/75.0.3770.80 Safari/537.36'}
        url = 'https://www.cardekho.com/used-cars+in+{}'.format(location)
        html_text = requests.get(url, headers=headers)
        print(html_text, 'response')
        html_text = html_text.text
        # print(html_text, '------used car')
        soup = BeautifulSoup(html_text, 'lxml')
        # print(soup, "location")
        car_no = soup.find('section', class_="carSummary").h1
        print(car_no.text)
        total_cars = car_no.text

        dict_data = {}
        all_cars = soup.find_all('div', class_="gsc_col-md-4")
        car_list = []
        for car in all_cars:
            car_image = car.find('img', class_="gsc_col-xs-12")
            car_data = car.find('div', class_="holder hover")
            if car_image or car_data:
                car_img_url = car_image['src']
                car_name = car_data.a.text
                car_url = car_data.a['href']

                total_kms = car_data.find('div', class_="truncate dotlist").span.text

                amount = car_data.find('span', class_="amnt").text

                # print(car_img_url)
                # print(car_name)
                # print(car_url)
                # print(total_kms)
                # print(amount)
                # print("---------END---------------")
                dict_data = {"image_url": car_img_url, "name": car_name, "url": car_url, "total_km": total_kms,
                             "amount": amount}

                car_list.append(dict_data)

    print(car_list)
    context = {
        "car_list": car_list,
        "total_cars": total_cars,
    }
    return render(request, 'used_car.html', context)
