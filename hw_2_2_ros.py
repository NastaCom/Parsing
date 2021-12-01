import requests
from bs4 import BeautifulSoup
from pprint import pprint
#import json
import pandas as pd


page = 1
products_list = []

url = 'https://roscontrol.com'#/category/produkti/myasnie_produkti/

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}

search_text = input("Продукт: ")
pages_count = input(f"Количество страниц: ")

while True:
    params = {'keyword': search_text,
          'page': page}

    response = requests.get(url + '/testlab/search', params=params, headers=headers)

    if response.ok:
        dom = BeautifulSoup(response.text, 'html.parser')
        products = dom.find_all('div', {'class', 'wrap-product-catalog__item'})


        for product in products:
            product_data = {}
            name = product.find('div', {'class', 'product__item-link'}).text
            product_rate_text = product.find("div", {"class": "rate"}).text
            product_rate = int(product_rate_text) if product_rate_text != "" else 0

            rating_blocks_tag = product.find("div", {"class": "rating-block"}).find_all("div", {"class": "row"})

            if rating_blocks_tag:
                safety = int(rating_blocks_tag[0].find("div", {"class": "right"}).text)
                naturally = int(rating_blocks_tag[1].find("div", {"class": "right"}).text)
                nutritional_value = int(rating_blocks_tag[2].find("div", {"class": "right"}).text)
                quality = int(rating_blocks_tag[3].find("div", {"class": "right"}).text)
                note = ""
            else:
                safety = naturally = nutritional_value = quality = 0
                note = product.find("div", {"class": "blacklist-desc-full-inner"}).text.replace("\n", "").strip()

            product_data = {"product_name": name,
                            "product_rate": product_rate,
                            "safety": safety,
                            "naturally": naturally,
                            "nutritional_value": nutritional_value,
                            "quality": quality,
                            "note": note}
            products_list.append(product_data)


        if page == int(pages_count) or not products or len(products) == 0:
            break
        else:
            print(f"Got page {page}")
            page += 1
    else:
        break

    if products_list:
        with open("roscontrol_result.json", 'w') as file:
            file.write(str(products_list))

        table = pd.DataFrame(products_list,
                             columns=["product_name", "product_rate", "safety", "naturally", "nutritional_value",
                                      "quality", "note"])
        print(table)
    else:
        print("Ничего не найдено")

pprint(products_list)
