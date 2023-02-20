import csv
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

PAGE_COUNT = 3
URL = "https://market.yandex.ru/product--smartfon-apple-iphone-14-pro-max/1768738052/offers?glfilter=14871214%3A16048172_101813096786&glfilter=23476910%3A26684950_101813096786&glfilter=24938610%3A41821219_101813096786&glfilter=25879492%3A25879710_101813096786&cpa=1&grhow=supplier&sku=101813096786&resale_goods=resale_new&local-offers-first=0"
PATH_TO_CHROME_PROFILE = r"user-data-dir=C:\\Users\\Victor\\AppData\\Local\\Google\\Chrome\\User Data\\"
PROFILE_DIR_NAME = '--profile-directory=Default'
SHOP_NAME_XP = "//*[self::span[@class = 'Vu-M2 _3Xnho']|self::img[@class = '_2DwmZ']|self::span[@class = '_3BJUh _3kBZk']]"
PRICE_VAL_XP = "//div[contains(@class,'_3NaXx _1YKgk')]"


def init_browser(p_profile_path, p_profile_dir_name):
    options = Options()
    options.add_argument(p_profile_path)
    options.add_argument(p_profile_dir_name)
    browser = webdriver.Chrome(options=options)
    return browser


def get_url_for_page(p_page_num):
    if p_page_num > 1:
        index = URL.find('local-offers-first=0')
        out_url = URL[:index] + 'page=' + str(p_page_num) + '&' + URL[index:]
    else:
        out_url = URL
    return out_url


def norm_price(p_price):
    p_price = p_price.text
    p_price = p_price.replace(" ", "")
    p_price = p_price.replace("₽", "")
    return int(p_price)


def norm_price_vals(p_price_vals):
    return list(map(norm_price, p_price_vals))


def norm_shop_names(p_shop_names):
    out_shop_names = []
    for i in range(len(p_shop_names)):
        if p_shop_names[i].text == '':
            tmp = (p_shop_names[i].get_attribute('title'))
            if tmp != '':
                out_shop_names.append(tmp)
        else:
            out_shop_names.append(p_shop_names[i].text)
    return out_shop_names


def save_to_csv(p_dict):
    header_lst = ['Название магазина', 'Цена на iphone']
    with open('out_data.csv', 'w', encoding='utf-8-sig') as path_to_file:
        wr = csv.writer(path_to_file)
        wr.writerow(header_lst)
        for sh_n, pr in p_dict.items():
            wr.writerow([sh_n, pr])


def main():
    m_browser = init_browser(PATH_TO_CHROME_PROFILE, PROFILE_DIR_NAME)
    shop_names = []
    price_vals = []
    for page_num in range(1, PAGE_COUNT + 1):
        m_browser.get(get_url_for_page(page_num))
        tmp_shop_names = m_browser.find_elements(By.XPATH, SHOP_NAME_XP)
        shop_names += norm_shop_names(tmp_shop_names)
        tmp_price_vals = m_browser.find_elements(By.XPATH, PRICE_VAL_XP)
        price_vals += norm_price_vals(tmp_price_vals)

    if len(shop_names) != len(price_vals):
        print('Parsing error!')
        sys.exit(1)

    m_data = dict(zip(shop_names, price_vals))
    m_sort_data = {}
    sort_shops = sorted(m_data, key=m_data.get)
    for shop in sort_shops:
        m_sort_data[shop] = m_data[shop]
    save_to_csv(m_sort_data)


if __name__ == '__main__':
    main()
