from api.altavita_cart import Cart

def test_add_item_to_cart():
    response = Cart.add_item_to_cart(6930, 2)
    print(response.json(), end='\n')
    assert response.status_code == 200
    assert response.json()['new_quantity'] == 2

def test_delete_item_from_cart():
    # Сначала добавляем продукт в корзину
    added_response = Cart.add_item_to_cart(6930, 2)
    product_id = 6930  # ID продукта, который добавили
    session_id = "93310ce3af2dd4c3f1b62542918eb431"  # Идентификатор сессии

    # Удаление продукта из корзины
    deleted_response = Cart.delete_product_from_cart(product_id, session_id)
    print(deleted_response.json(), end='\n')  # Выведем JSON-ответ сервера

    # Проверка успеха операции
    assert deleted_response.status_code == 200
    # Здесь ожидаемое поведение зависит от того, какой ответ сервер даёт после удаления товара
    # Обычно ожидается, что в ответе появится какое-то подтверждение об успехе операции
    # Подставьте нужные условия согласно документации вашего API
    assert deleted_response.json().get('status') == 'ok'