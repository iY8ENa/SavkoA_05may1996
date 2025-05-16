SQL-запросы к базе данных «Полезные продукты»
В данном разделе представлены SQL-запросы, разработанные в рамках тестового задания для проекта Altaivita.ru. Запросы предназначены для решения конкретных бизнес-задач, связанных с аналитикой продуктов и категорий.

📋 Постановка задачи
Требуется реализовать следующие SQL-запросы для анализа и агрегирования данных в базе данных "Полезные продукты":

Вывести все уникальные названия продуктов.
Вывести ID, название и стоимость продуктов с содержанием клетчатки более 5 граммов.
Вывести название продукта с самым высоким содержанием белка.
Подсчитать общую сумму калорий для продуктов каждой категории, исключая продукты с нулевым содержанием жира.
Рассчитать среднюю цену товаров каждой категории.
🖇️ Структура базы данных
Таблицы:

Products («Продукты»)Столбцы:  
product_id: int (первичный ключ)  
product_name: varchar  
category_id: int (внешний ключ, ссылающийся на Categories)  
calories: int  
price: decimal
Categories («Категории»)Столбцы:  
category_id: int (первичный ключ)  
category_name: varchar
Nutritional Information («Пищевая ценность»)Столбцы:  
product_id: int (внешний ключ, ссылающийся на Products)  
protein: decimal  
carbohydrates: decimal  
fat: decimal  
fiber: decimal
🧩 Реализованные запросы
1. Выборка уникальных названий продуктов

SELECT DISTINCT p.product_name 
FROM public.products p;
2. Продукты с клетчаткой более 5 граммов

SELECT 
    p.product_id, p.product_name, p.price 
FROM 
    public.products p
JOIN 
    public.nutritional_information ni USING(product_id)
WHERE
    ni.fiber > 5;
3. Продукт с наибольшим содержанием белка

SELECT 
    p.product_name 
FROM 
    public.products p
JOIN 
    public.nutritional_information ni USING(product_id)
ORDER BY ni.protein DESC
LIMIT 1;
4. Суммарные калории по категориям (за исключением продуктов с нулевым жиром)

SELECT 
    c.category_id,
    SUM(ni.calories) AS sum_calories
FROM 
    public.products p
JOIN 
    public.nutritional_information ni USING(product_id)
JOIN 
    public.categories c USING(category_id)
WHERE 
    ni.fat > 0
GROUP BY 
    c.category_id;
5. Средняя цена товаров по категориям

SELECT 
    c.category_name, ROUND(AVG(p.price), 2) AS средняя_цена
FROM 
    public.categories c
JOIN 
    public.products p USING(category_id)
GROUP BY 
    c.category_name;
🛠 Особенности разработки
Агрегированные запросы: Использованы агрегатные функции SUM() и AVG(), позволяющие проводить расчёт общей суммы калорий и средней стоимости товаров соответственно.
Использование JOIN'ов: Применялись операции соединения таблиц для объединения данных из различных источников.
Группировка данных: Во многих запросах используется операция группировки GROUP BY, позволяющая анализировать данные по категориям.
Отсутствие ограничения размеров выбора: Разработчик принял решение вывести полную картину по продуктам и категориям без ограничения выборки по размерам.

# SavkoA_05may1996