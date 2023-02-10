import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

PAGE_COUNT = 7
URL = "https://market.yandex.ru/product--smartfon-apple-iphone-14-pro-max/1768738052/offers?glfilter=14871214%3A16048172_101813096786&glfilter=23476910%3A26684950_101813096786&glfilter=24938610%3A41821219_101813096786&glfilter=25879492%3A25879710_101813096786&cpa=1&grhow=supplier&sku=101813096786&resale_goods=resale_new&local-offers-first=0"
PATH_TO_CHROME_PROFILE = r"user-data-dir=C:\\Users\\Victor\\AppData\\Local\\Google\\Chrome\\User Data\\"
PROFILE_DIR_NAME = '--profile-directory=Default'
SHOP_NAME_XP = "//*[self::span[@class = 'Vu-M2 _3Xnho']|self::img[@class = '_2DwmZ']|self::span[@class = '_3BJUh _3kBZk']]"
PRICE_VAL_XP = "//div[contains(@class,'_3NaXx _1YKgk')]"


def init_browser(p_url, p_profile_path, p_profile_dir_name):
    options = Options()
    options.add_argument(p_profile_path)
    options.add_argument(p_profile_dir_name)
    browser = webdriver.Chrome(options=options)
    browser.get(p_url)
    return browser


def get_url_for_page(p_page_num):
    index = URL.find('local-offers-first=0')
    out_url = URL[:index] + 'page=' + str(p_page_num) + '&' + URL[index:]
    return out_url


def norm_price(p_price):
    p_price = p_price.replace(" ", "")
    p_price = p_price.replace("₽", "")
    return int(p_price)


def norm_price_vals(p_price_vals):
    out_price_vals = []
    for i in range(len(p_price_vals)):
        out_price_vals.append(norm_price(p_price_vals[i].text))
    return out_price_vals


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


def data_to_dict(p_shop_names, p_price_vals):
    out_data = {}
    if len(p_shop_names) != len(p_price_vals):
        print('Parsing error.')
        return
    for i in range(len(p_shop_names)):
        out_data[p_shop_names[i]] = p_price_vals[i]
    return out_data


def save_to_csv(p_dict):
    path_to_file = open('out_data.csv', 'w')
    wr = csv.writer(path_to_file)
    for sh_n, pr in p_dict.items():
        wr.writerow([sh_n, pr])


m_browser = init_browser(URL, PATH_TO_CHROME_PROFILE, PROFILE_DIR_NAME)

shop_names = []
price_vals = []
for page_num in range(1, PAGE_COUNT + 1):
    if page_num > 1:
        cur_url = get_url_for_page(page_num)
        m_browser.get(cur_url)
    tmp_shop_names = []
    tmp_price_vals = []
    tmp_shop_names += m_browser.find_elements(By.XPATH, SHOP_NAME_XP)
    shop_names += norm_shop_names(tmp_shop_names)
    tmp_price_vals += m_browser.find_elements(By.XPATH, PRICE_VAL_XP)
    price_vals += norm_price_vals(tmp_price_vals)

m_data = data_to_dict(shop_names, price_vals)
m_sort_data = {}
sort_prices = sorted(m_data, key=m_data.get)
for price in sort_prices:
    m_sort_data[price] = m_data[price]
save_to_csv(m_sort_data)
