from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import re
from faker import Faker


def authentication(driver: webdriver.Chrome, username: str, password: str):
    driver.find_element(By.ID, 'user-name').send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.ID, 'login-button').click()


def add_to_cart(driver: webdriver.Chrome):
    products = driver.find_elements(By.CLASS_NAME, 'inventory_item')
    product = random.choice(products)
    product_button = product.find_element(By.CLASS_NAME, 'btn')
    product_button.click()
    driver.get('https://www.saucedemo.com/cart.html')


def check_cart(driver: webdriver.Chrome):
    cart = driver.find_element(By.CLASS_NAME, 'cart_list')
    products = cart.find_elements(By.CLASS_NAME, 'cart_item')
    assert len(products) > 0, 'Cart is empty'


def fill_form(driver: webdriver.Chrome):
    fake = Faker(locale='ru_RU')
    name = fake.name()
    address = fake.address()
    zip_code = re.search(r'\d{5,6}', address).group()
    driver.find_element(By.CLASS_NAME, 'checkout_button').click()
    driver.find_element(By.ID, 'first-name').send_keys(name)
    driver.find_element(By.ID, 'last-name').send_keys(name)
    driver.find_element(By.ID, 'postal-code').send_keys(zip_code)
    driver.find_element(By.ID, 'continue').click()
    driver.find_element(By.ID, 'finish').click()


def check_order(driver: webdriver.Chrome):
    order = driver.find_element(By.XPATH, '//*[@id="checkout_complete_container"]/h2')
    assert order.text == 'Thank you for your order!', 'Order is not completed'


if __name__ == '__main__':
    service = Service(executable_path='./chromedriver')
    options = Options()
    options.add_experimental_option('detach', True)
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get('https://www.saucedemo.com/')
        authentication(driver, 'standard_user', 'secret_sauce')
        WebDriverWait(driver, 10).until(EC.url_to_be('https://www.saucedemo.com/inventory.html'))
        add_to_cart(driver)
        WebDriverWait(driver, 10).until(EC.url_to_be('https://www.saucedemo.com/cart.html'))
        check_cart(driver)
        fill_form(driver)
        check_order(driver)
    except AssertionError as e:
        print(e)
    finally:
        driver.quit()
