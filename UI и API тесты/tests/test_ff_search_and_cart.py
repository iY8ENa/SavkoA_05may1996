import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import allure

@pytest.fixture(scope='module')
def driver():
    firefox_options = Options()
    firefox_service = Service(r'C:\API UI\geckodriver.exe')  # Путь к geckodriver
    driver = webdriver.Firefox(service=firefox_service, options=firefox_options)
    driver.maximize_window()
    yield driver
    driver.quit()

class TestFireFoxSearchAndCart:
    def set_zoom_level(self, driver):
        # Постоянно устанавливаем масштаб страницы (если требуется)
        driver.execute_script("document.body.style.zoom='75%'")

    def scroll_into_view(self, driver, element):
        # Прокручиваем элемент в область видимости
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", element)

    def click_with_js(self, driver, element):
        # Использование JavaScript для безопасного клика по элементу
        driver.execute_script("arguments[0].click();", element)

    def retry_click(self, driver, element, retries=3):
        # Повторяем попытку клика несколько раз, если первая неудачная
        for attempt in range(retries):
            try:
                self.scroll_into_view(driver, element)
                self.click_with_js(driver, element)
                break
            except Exception as ex:
                print(f"Attempt {attempt + 1} failed: {ex}")

    @allure.title("Тест поиска и добавления товара в корзину через FireFox")
    @allure.description("Поиск товара, добавление в корзину и последующий возврат на главную страницу.")
    def test_firefox_search_and_cart(self, driver):
        with allure.step("Открываем главную страницу"):
            driver.get("https://altaivita.ru/")
            self.set_zoom_level(driver)  # Устанавливаем масштаб сразу после открытия главной страницы

        with allure.step("Производим поиск товара"):
            # Новый селектор по частичному соответствию класса
            search_input = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[class*="searchpro__field-input"]'))
            )
            search_input.clear()  # Очистим поле поиска, если в нём уже есть текст
            search_input.send_keys("Огнёвка Про")
            search_input.send_keys(Keys.ENTER)

        with allure.step("Добавляем найденный товар в корзину"):
            add_to_cart_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.digi-product__button'))
            )
            self.click_with_js(driver, add_to_cart_button)

        with allure.step("Переходим в корзину"):
            cart_icon = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.header__basket-link.ga_link_to_cart.grid_container_mobile_menu.pdd_cart'))
            )
            self.click_with_js(driver, cart_icon)

            proceed_to_cart_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.dropdown-go-over.link-gray.ga_link_to_cart'))
            )
            self.click_with_js(driver, proceed_to_cart_button)

        with allure.step("Удаляем товар из корзины"):
            delete_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.basket__delete.js-item-delete'))
            )
            self.click_with_js(driver, delete_button)

        with allure.step("Возвращаемся на главную страницу"):
            home_logo = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'img[src="/wa-data/public/site/themes/altaivita/_source/app/img/logo.svg"]'))
            )
            self.click_with_js(driver, home_logo)

if __name__ == "__main__":
    pytest.main(['--alluredir', './reports'])