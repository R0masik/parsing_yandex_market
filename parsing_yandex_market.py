import csv
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

URL = "https://market.yandex.ru/product--smartfon-apple-iphone-14-pro-max/1768738052/offers?glfilter=14871214%3A16048172_101813096786&glfilter=23476910%3A26684950_101813096786&glfilter=24938610%3A41821219_101813096786&glfilter=25879492%3A25879710_101813096786&cpa=1&grhow=supplier&sku=101813096786&resale_goods=resale_new&local-offers-first=0"
PATH_TO_CHROME_PROFILE = r"user-data-dir=C:\\Users\\Victor\\AppData\\Local\\Google\\Chrome\\User Data\\"
PROFILE_DIR_NAME = '--profile-directory=Default'
SHOP_NAME_XP = "//*[self::span[@class = 'Vu-M2 _3Xnho']|self::img[@class = '_2DwmZ']|self::span[@class = '_3BJUh _3kBZk']|self::img[@class = '_2DwmZ _19HY9']]"
PRICE_VAL_XP = "//div[contains(@class,'_3NaXx _1YKgk')]"


def init_browser(p_profile_path, p_profile_dir_name):
    options = Options()
    options.add_argument(p_profile_path)
    options.add_argument(p_profile_dir_name)
    options.add_argument('--headless=new')
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
    return int(p_price.text.replace(" ", "").replace("₽", ""))


def norm_price_vals(p_price_vals):
    return list(map(norm_price, p_price_vals))


def norm_shop_names(p_shop_names):
    out_shop_names = []
    for i in range(len(p_shop_names)):
        if p_shop_names[i].text == '':
            title = p_shop_names[i].get_attribute('title')
            if title != '':
                out_shop_names.append(title)
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
    page_num = 1
    previus_shop_names = []
    previus_price_vals = []
    stop_parsing = False
    while not stop_parsing:
        m_browser.get(get_url_for_page(page_num))
        tmp_shop_names = norm_shop_names(m_browser.find_elements(By.XPATH, SHOP_NAME_XP))
        tmp_price_vals = norm_price_vals(m_browser.find_elements(By.XPATH, PRICE_VAL_XP))
        if previus_shop_names == tmp_shop_names and previus_price_vals == tmp_price_vals:
            stop_parsing = True
        else:
            previus_shop_names = tmp_shop_names
            previus_price_vals = tmp_price_vals
            shop_names += tmp_shop_names
            price_vals += tmp_price_vals
            page_num += 1

    if len(shop_names) != len(price_vals):
        print('Parsing error!')
        sys.exit(1)

    m_data = dict(zip(shop_names, price_vals))
    sort_shops = sorted(m_data, key=m_data.get)
    m_sort_data = {sh_n: m_data[sh_n] for sh_n in sort_shops}
    print(len(m_sort_data))
    save_to_csv(m_sort_data)


if __name__ == '__main__':
    main()
