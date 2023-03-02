import time
from concurrent.futures import ThreadPoolExecutor, wait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

PAGE_COUNT = 2
URL = "https://market.yandex.ru/product--smartfon-apple-iphone-14-pro-max/1768738052/offers?glfilter=14871214%3A16048172_101813096786&glfilter=23476910%3A26684950_101813096786&glfilter=24938610%3A41821219_101813096786&glfilter=25879492%3A25879710_101813096786&cpa=1&grhow=supplier&sku=101813096786&resale_goods=resale_new&local-offers-first=0"
PATH_TO_CHROME_PROFILE = r"user-data-dir=C:\\Users\\Victor\\AppData\\Local\\Google\\Chrome\\User Data\\"
PROFILE_DIR_NAME = '--profile-directory=Default'
SHOP_NAME_XP = "//*[self::span[@class = 'Vu-M2 _3Xnho']|self::img[@class = '_2DwmZ']|self::span[@class = '_3BJUh _3kBZk']|self::img[@class = '_2DwmZ _19HY9']]"
PRICE_VAL_XP = "//div[contains(@class,'_3NaXx _1YKgk')]"
CAPTCHA_XP = "//input[contains(@class, 'CheckboxCaptcha-Button')]"
NEXT_PAGE_XP = "//a[contains(@class, '_2prNU _3OFYT')]"
TIME_OUT = 1


def init_browser():
    options = Options()
    options.binary_location = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
    options.add_argument("--no-sandbox")  # bypass OS security model
    options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    # options.add_argument('--headless=new')
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


def get_page(p_browser, p_url):
    p_browser.get(p_url)
    time.sleep(TIME_OUT)
    if p_browser.find_elements(By.XPATH, CAPTCHA_XP):
        p_browser.find_element(By.XPATH, CAPTCHA_XP).click()
        time.sleep(TIME_OUT)
    return p_browser


def scan():
    b = init_browser()
    shop_names = []
    price_vals = []
    page_num = 1
    last_page = False
    while not last_page:
        b.get(get_url_for_page(page_num))
        time.sleep(TIME_OUT)
        if b.find_elements(By.XPATH, CAPTCHA_XP):
            b.find_element(By.XPATH, CAPTCHA_XP).click()
            time.sleep(TIME_OUT)
        shop_names += norm_shop_names(b.find_elements(By.XPATH, SHOP_NAME_XP))
        price_vals += norm_price_vals(b.find_elements(By.XPATH, PRICE_VAL_XP))
        if not b.find_elements(By.XPATH, NEXT_PAGE_XP):
            last_page = True
        page_num += 1
    b.close()

    print(len(shop_names))
    print(len(price_vals))
    for i in range(len(shop_names)):
        print(shop_names[i] + '---' + str(price_vals[i]))


b = init_browser()
b = get_page(b, get_url_for_page(1))
time.sleep(300)
