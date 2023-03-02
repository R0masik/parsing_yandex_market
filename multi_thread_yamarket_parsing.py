import time
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv

CHROME_BINARY_LOCATION = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
SRC_URL = "https://market.yandex.ru/product--smartfon-apple-iphone-14-pro-max/1768738052/offers?glfilter=14871214%3A16048172_101813096786&glfilter=23476910%3A26684950_101813096786&glfilter=24938610%3A41821219_101813096786&glfilter=25879492%3A25879710_101813096786&cpa=1&grhow=supplier&sku=101813096786&resale_goods=resale_new&local-offers-first=0"
SHOP_NAME_XP = "//*[self::span[@class = 'Vu-M2 _3Xnho']|self::img[@class = '_2DwmZ']|self::span[@class = '_3BJUh _3kBZk']|self::img[@class = '_2DwmZ _19HY9']]"
PRICE_VAL_XP = "//div[contains(@class,'_3NaXx _1YKgk')]"
CAPTCHA_BUTTON_XP = "//input[contains(@class, 'CheckboxCaptcha-Button')]"
NEXT_PAGE_XP = "//a[contains(@class, '_2prNU _3OFYT')]"
TIMEOUT = 1


def init_browser():
    options = Options()
    options.binary_location = CHROME_BINARY_LOCATION
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--headless=new')
    return webdriver.Chrome(options=options)


def get_url_for_page(p_page_num):
    if p_page_num > 1:
        index = SRC_URL.find('local-offers-first=0')
        out_url = SRC_URL[:index] + 'page=' + str(p_page_num) + '&' + SRC_URL[index:]
    else:
        out_url = SRC_URL
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


def scan_page(p_page_num):
    browser = init_browser()
    browser.get(get_url_for_page(p_page_num))
    time.sleep(TIMEOUT)
    if browser.find_elements(By.XPATH, CAPTCHA_BUTTON_XP):
        browser.find_element(By.XPATH, CAPTCHA_BUTTON_XP).click()
        time.sleep(TIMEOUT)
    shops = norm_shop_names(browser.find_elements(By.XPATH, SHOP_NAME_XP))
    prices = norm_price_vals(browser.find_elements(By.XPATH, PRICE_VAL_XP))
    if browser.find_elements(By.XPATH, NEXT_PAGE_XP):
        is_last_page = False
    else:
        is_last_page = True
    browser.close()
    return shops, prices, is_last_page


def main():
    futures_lst = []
    shop_names = []
    price_vals = []
    page_num = 1
    last_page = False
    with ThreadPoolExecutor() as executor:
        while not last_page:
            futures_lst.append(executor.submit(scan_page, page_num))
        wait(futures_lst)
        for future in futures_lst:
            res = future.result()
            shop_names += res[0]
            price_vals += res[1]
    print(len(shop_names))
    m_data = dict(zip(shop_names, price_vals))
    sort_shops = sorted(m_data, key=m_data.get)
    m_sort_data = {sh_n: m_data[sh_n] for sh_n in sort_shops}
    print(len(m_sort_data))
    save_to_csv(m_sort_data)


if __name__ == '__main__':
    main()
