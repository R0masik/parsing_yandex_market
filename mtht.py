from concurrent.futures import ThreadPoolExecutor, as_completed, wait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


PAGE_COUNT = 2
URL = "https://market.yandex.ru/product--smartfon-apple-iphone-14-pro-max/1768738052/offers?glfilter=14871214%3A16048172_101813096786&glfilter=23476910%3A26684950_101813096786&glfilter=24938610%3A41821219_101813096786&glfilter=25879492%3A25879710_101813096786&cpa=1&grhow=supplier&sku=101813096786&resale_goods=resale_new&local-offers-first=0"
PATH_TO_CHROME_PROFILE = r"user-data-dir=C:\\Users\\Victor\\AppData\\Local\\Google\\Chrome\\User Data\\"
PROFILE_DIR_NAME = '--profile-directory=Default'
SHOP_NAME_XP = "//*[self::span[@class = 'Vu-M2 _3Xnho']|self::img[@class = '_2DwmZ']|self::span[@class = '_3BJUh _3kBZk']|self::img[@class = '_2DwmZ _19HY9']]"
PRICE_VAL_XP = "//div[contains(@class,'_3NaXx _1YKgk')]"
TIME_OUT = 20


def init_browser(p_profile_path, p_profile_dir_name):
    options = Options()
    options.add_argument(p_profile_path)
    options.add_argument(p_profile_dir_name)
    return webdriver.Chrome(options=options)


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


def scan_page(p_url, p_browser):
    p_browser.get(p_url)
    out_shop_names = norm_shop_names(WebDriverWait(p_browser, TIME_OUT).until(
        EC.visibility_of_all_elements_located((By.XPATH, SHOP_NAME_XP))
    ))
    out_price_vals = norm_price_vals(WebDriverWait(p_browser, TIME_OUT).until(
        EC.visibility_of_all_elements_located((By.XPATH, PRICE_VAL_XP))
    ))
    return out_shop_names, out_price_vals


def main():
    browser = init_browser(PATH_TO_CHROME_PROFILE, PROFILE_DIR_NAME)
    urls = [get_url_for_page(page_num) for page_num in range(1, PAGE_COUNT + 1)]
    thread_lst = []
    with ThreadPoolExecutor() as executor:
        for url in urls:
            thread_lst.append(executor.submit(scan_page, url, browser))

    wait(thread_lst)

    thread1 = thread_lst[0]
    thread2 = thread_lst[1]

    print(thread1.result())
    print(thread2.result())


if __name__ == '__main__':
    main()
