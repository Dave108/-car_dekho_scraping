from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import time
from django.utils.crypto import get_random_string
import pandas as pd


# Create your views here.

def homepage(request):
    return render(request, 'home.html')


# print(price.text)
# print(dotlist.text)
# print(cars_image['src'])
# print(cars.a, '---***---***---***---***---***---***---***---***')
def new_car_view(request):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/75.0.3770.80 Safari/537.36'}
    brand = request.GET.get('brand')
    context = None
    if brand:
        # print(brand)
        car_dict = {}
        car_list = []
        car_specs_dict = {}
        car_specs_list = []
        url = 'https://www.cardekho.com{}'.format(brand)
        html_text = requests.get(url, headers=headers)
        time.sleep(10)
        html_text = html_text.text
        soup = BeautifulSoup(html_text, 'lxml')
        # print(soup.prettify())
        cars_summary = soup.find("div", class_="gsc_col-md-8 gsc_col-lg-9 gsc_col-sm-12 gsc_col-xs-12 BrandDesc")
        # print(cars_summary.h1.text)
        time.sleep(5)
        cars_data = soup.find_all('li', class_="gsc_col-xs-12 gsc_col-sm-6 gsc_col-md-12 gsc_col-lg-12")
        # print(cars_data)
        for cars in cars_data:
            cars_image = cars.find('img')
            # time.sleep(6)
            # print("...............vv",cars_image)

            price = cars.find('div', class_="price")
            dotlist = cars.find('div', class_="dotlist")
            if cars_image:
                url = 'https://www.cardekho.com{}'.format(cars.a['href'])
                time.sleep(5)
                html_text = requests.get(url, headers=headers)
                html_text = html_text.text
                soup = BeautifulSoup(html_text, 'html5lib')
                car_specs = soup.find_all('tr', class_="gsc_col-xs-4 gsc_col-sm-2")
                car_specs_dict = {}
                for specs in car_specs:
                    header = specs.find('span', class_="iconname")
                    value = specs.find('td', class_="gsc_col-xs-12 textHold")
                    dict1 = {header.text: value.text}
                    # print(dict)
                    car_specs_dict.update(dict1)
                specs_link_find = soup.find('ul', class_="modelNavUl")
                spec_link = specs_link_find.find_all('a')
                final_spec_dict = {}
                variants_list = []
                for indlist in spec_link[1:]:
                    if indlist.text == "Specs":
                        spec_url = "https://www.cardekho.com" + indlist['href']
                        # print(spec_url)
                        html_text = requests.get(spec_url, headers=headers)
                        time.sleep(0.5)
                        html_text = html_text.text
                        soup = BeautifulSoup(html_text, 'html5lib')
                        specs_details = soup.find('div', id="technicalSpecsTop")
                        details = specs_details.find_all('tr')
                        # print(details, "------")

                        for x in details:
                            # print(x.td.text, ":", x.span.text)
                            dict1 = {x.td.text: x.span.text}
                            # print(dict1)
                            final_spec_dict.update(dict1)
                        # print(final_spec_dict)
                    if indlist.text == "Variants":
                        spec_url = "https://www.cardekho.com" + indlist['href']
                        # print(spec_url)
                        html_text = requests.get(spec_url, headers=headers)
                        time.sleep(0.5)
                        html_text = html_text.text
                        soup = BeautifulSoup(html_text, 'html5lib')
                        specs_details = soup.find('table', class_="allvariant contentHold").tbody
                        # print(specs_details.td.a)
                        for y in specs_details:
                            # print(y.td.a.text)
                            variants_list.append(y.td.a.text)
                print(variants_list)
                print("-----")
                # print(final_spec_dict)
                car_dict = {"image_url": cars_image['src'], "car_name": cars.a.text, "price": price.text,
                            "dotlist": dotlist.text, "car_page": cars.a['href'], "variants_list": variants_list}
                car_dict.update(car_specs_dict)
                car_dict.update(final_spec_dict)
                # print(car_dict)
                car_list.append(car_dict)

        df = pd.DataFrame(car_list)
        # file_name = cars_summary.h1.text
        # file_name = file_name.replace(" ", "_") + get_random_string(3) + ".csv"
        # print(file_name)
        # df.to_csv(file_name, index=False) #UN-COMMENT THIS LATER
        print(df)
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
            # print(brand_action)
            # print(brand_name)
            # print("----------------------------------------------")
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
