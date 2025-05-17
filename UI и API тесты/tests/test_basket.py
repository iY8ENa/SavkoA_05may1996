import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import allure
from webdriver_manager.chrome import ChromeDriverManager  # Импортируем веб-драйвер-менеджер
from selenium.webdriver.chrome.service import Service


@pytest.fixture(scope="module")
def driver():
    service = Service(ChromeDriverManager().install())  # Менеджер выберет подходящую версию драйвера
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1920, 1080)  # Зафиксируем размер окна
    yield driver
    driver.quit()


class TestBasketUI:
    def set_zoom_level(self, driver):
        # Установка уровня масштабирования 75%
        driver.execute_script("document.body.style.zoom='75%'")

    def scroll_into_view(self, driver, element):
        # Прокрутка элемента в видимость
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", element)

    def click_with_js(self, driver, element):
        # Использование JS-клика для надежности
        driver.execute_script("arguments[0].click();", element)

    def retry_click(self, driver, element, retries=3):
        # Метод для повторных попыток кликов
        for attempt in range(retries):
            try:
                self.scroll_into_view(driver, element)
                self.click_with_js(driver, element)
                break
            except Exception as ex:
                print(f"Attempt {attempt + 1} failed: {ex}")

    @allure.title("Тест на добавление и удаление товара из корзины")
    @allure.description("Автоматическое добавление товара в корзину и последующее удаление.")
    def test_add_and_remove_one_item(self, driver):
        with allure.step("Открываем главную страницу"):
            driver.get("https://altaivita.ru/")
            self.set_zoom_level(driver)  # Масштабирование после открытия главной страницы

        with allure.step("Открываем каталог продуктов"):
            catalog_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            'body > header > div.container > div.header__nav-box > nav > ul.header__nav-list.left.not-list > li:nth-child(1) > a'))
            )
            self.click_with_js(driver, catalog_button)  # Клик по кнопке каталога через JS

        with allure.step("Переходим в категорию подарков"):
            gifts_category = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, '#bg-bg_mountains > div.row > div.col-12.col-md-2 > ul > li:nth-child(7) > a'))
            )
            self.click_with_js(driver, gifts_category)  # Перейти в категорию подарков через JS
            self.set_zoom_level(driver)  # Масштабируем на странице подарков

        with allure.step("Добавляем один товар в корзину"):
            first_item_selector = (
                'body > div:nth-child(11) > main > div > div.category__list > div > div.col-12.col-md-12.col-lg-9 > div > div:nth-child(1) > div > div:nth-child(4) > div > div.product__buy > div.product__add_2_0.js-product__add_2_0_cat_preview_3005'
            )
            add_to_cart_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, first_item_selector))  # Ожидание появления кнопки добавления
            )
            self.scroll_into_view(driver, add_to_cart_button)  # Прокручиваем элемент в видимую область
            self.click_with_js(driver, add_to_cart_button)  # Добавляем товар в корзину через JS

        with allure.step("Проверяем количество товаров в корзине"):
            basket_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            'body > header > div.container > div.header__top > div.header__right > div.header__basket.js-basket-wrapper > a'))
            )
            self.click_with_js(driver, basket_button)  # Открытие корзины через JS

            cart_count_span = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                  'body > header > div.container > div.header__top > div.header__right > div.header__basket.js-basket-wrapper > div > div.dropdown-top.dropdown-padding > div > span.sum.js-count-long'))
            )
            assert cart_count_span.text.strip() == '1 шт.', f'Количество товаров в корзине неверно: {cart_count_span.text}'

        with allure.step("Переходим в корзину"):
            go_to_cart_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            'body > header > div.container > div.header__top > div.header__right > div.header__basket.js-basket-wrapper > div > div.dropdown-top.dropdown-padding > a'))
            )
            self.click_with_js(driver, go_to_cart_button)  # Переход в корзину через JS
            self.set_zoom_level(driver)  # Масштабируем на странице корзины

        with allure.step("Удаляем товар из корзины"):
            delete_button_selector = ".basket__delete.js-item-delete button"
            delete_button = WebDriverWait(driver, 20).until(  # Увеличенное время ожидания
                EC.element_to_be_clickable((By.CSS_SELECTOR, delete_button_selector))
            )
            self.retry_click(driver, delete_button)  # Используется метод повторных попыток

            # ЯВНОЕ ожидание очистки корзины
            WebDriverWait(driver, 10).until(
                lambda d: d.find_element(By.CSS_SELECTOR, 'body > div:nth-child(12) > main > div > div.row.basket__row > div.col-xl-3.basket__col.right > div > div > div > div > span > span.js-cart_page_total_amount').text.strip() == '0 ₽'
            )

        with allure.step("Проверяем общую стоимость корзины"):
            total_price_span = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                  'body > div:nth-child(12) > main > div > div.row.basket__row > div.col-xl-3.basket__col.right > div > div > div > div > span > span.js-cart_page_total_amount'))
            )
            assert total_price_span.text.strip() == '0 ₽', f'Общая стоимость некорректна: {total_price_span.text}'

        with allure.step("Возвращаемся на главную страницу"):
            logo_image = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'body > header > div.container > div.header__top > div.header__logo > a > img'))
            )
            self.click_with_js(driver, logo_image)  # Возвращение на главную через JS
            self.set_zoom_level(driver)  # Восстанавливаем масштаб на главной странице

if __name__ == "__main__":
    pytest.main(['--alluredir', './reports'])