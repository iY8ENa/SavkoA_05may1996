
import pytest
from api.altavita_cart import Cart

# Твоя существующая фикстура
@pytest.fixture(scope="session")
def base_url():
    """Базовый URL сайта."""
    return "https://altaivita.ru"

# Новая фикстура, которая очищает корзину перед каждым тестом
@pytest.fixture(autouse=True)
def clean_cart_before_test():
    """
    Фикстура, очищающая корзину перед каждым тестом.
    Используется автоматически благодаря параметру autouse=True.
    """
    Cart.clear_cart()