import requests

class Cart:

    @staticmethod
    def add_item_to_cart(prod_id: int, count: int, session_id=None):
        URL = "https://altaivita.ru/engine/cart/add_products_to_cart_from_preview.php"
        data = {
            "product_id": prod_id,
            "LANG_key": "ru",
            "S_wh": 1,
            "S_CID": session_id or "93310ce3af2dd4c3f1b62542918eb431",
            "S_cur_code": "usd",
            "S_koef": 0.01273,
            "quantity": count,
            "S_hint_code": "eur",
            "S_customerID": "",
        }

        response = requests.post(URL, data=data, headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"})

        if response.status_code == 200:
            return response
        else:
            raise Exception(f"API request failed with status code {response.status_code}")

    @staticmethod
    def delete_product_from_cart(prod_id: int, session_id=None):
        URL = "https://altaivita.ru/engine/cart/delete_products_from_cart_preview.php"
        data = {
            "product_id": prod_id,
            "LANG_key": "ru",
            "S_wh": 1,
            "S_CID": session_id or "93310ce3af2dd4c3f1b62542918eb431",
            "S_cur_code": "usd",
            "S_koef": 0.01273,
            "S_hint_code": "eur",
            "S_customerID": "",
        }

        response = requests.post(URL, data=data, headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"})

        if response.status_code == 200:
            return response
        else:
            raise Exception(f"API request failed with status code {response.status_code}")

    @staticmethod
    def clear_cart(session_id=None):
        URL = "https://altaivita.ru/engine/cart/clear_cart.php"
        data = {
            "LANG_key": "ru",
            "S_wh": 1,
            "S_CID": session_id or "93310ce3af2dd4c3f1b62542918eb431",
            "S_cur_code": "usd",
            "S_koef": 0.01273,
            "S_hint_code": "eur",
            "S_customerID": "",
        }

        response = requests.post(URL, data=data)

        if response.status_code != 200:
            raise Exception(f"Failed to clear cart. Status code: {response.status_code}")