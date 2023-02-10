## Это тестовый файл для экспирементов

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

PAGE_COUNT = 1
URL = "https://market.yandex.ru/product--smartfon-apple-iphone-14-pro-max/1768738052/offers?glfilter=14871214%3A16048172_101813096786&glfilter=23476910%3A26684950_101813096786&glfilter=24938610%3A41821219_101813096786&glfilter=25879492%3A25879710_101813096786&cpa=1&grhow=supplier&sku=101813096786&resale_goods=resale_new&local-offers-first=0"
PATH_TO_CHROME_PROFILE = r"user-data-dir=C:\\Users\\Victor\\AppData\\Local\\Google\\Chrome\\User Data\\"
PROFILE_DIR_NAME = '--profile-directory=Default'
SHOP_NAME_TXT_XP = "//span[contains(@class,'Vu-M2 _3Xnho')]"
TEST_SHOP_NAME_TXT_XP = "//span[@class = 'Vu-M2 _3Xnho']"
TEST_SHOP_NAME_IMG_XP = "//img[@class = '_2DwmZ']"
TEST_TOTAL_XP = "//*[self::span[@class = 'Vu-M2 _3Xnho']|self::img[@class = '_2DwmZ']|self::span[@class = '_3BJUh _3kBZk']]"
PRICE_VAL_XP = "//div[contains(@class,'_3NaXx _1YKgk')]"


def init_browser(p_url, p_profile_path, p_profile_dir_name):
    options = Options()
    options.add_argument(p_profile_path)
    options.add_argument(p_profile_dir_name)
    # options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)
    browser.get(p_url)
    return browser


def get_url_for_page(p_page_num):
    index = URL.find('local-offers-first=0')
    out_url = URL[:index] + 'page=' + str(p_page_num) + '&' + URL[index:]
    return out_url

m_browser = init_browser(URL, PATH_TO_CHROME_PROFILE, PROFILE_DIR_NAME)

page_num = 3
cur_url = get_url_for_page(page_num)
m_browser.get(cur_url)

t = m_browser.find_elements(By.XPATH, TEST_TOTAL_XP)

print(len(t))

delete_items_indeces = []

for i in range(len(t)):
    if t[i].text == '':
        tmp = t[i].get_attribute('title')
        print(tmp)
        if tmp == '':
            delete_items_indeces.append(i)
    else:
        print(t[i].text)

for i in range(len(delete_items_indeces)):
    t.pop(delete_items_indeces[i])

print('AFTER DELETE: ')
print(len(t))

for i in range(len(t)):
    if t[i].text == '':
        tmp = t[i].get_attribute('title')
        print(tmp)
    else:
        print(t[i].text)
