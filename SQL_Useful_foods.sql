-- Первый запрос: Вывести уникальные названия продуктов
SELECT DISTINCT p.product_name 
FROM public.products p;

-- Второй запрос: Вывести ID, название и цену продуктов с содержанием клетчатки более 5 граммов
SELECT 
    p.product_id, p.product_name, p.price 
FROM 
    public.products p
JOIN 
    public.nutritional_information ni USING(product_id)
WHERE
    ni.fiber > 5;

-- Третий запрос: Найти продукт с наибольшим содержанием белка
SELECT 
    p.product_name 
FROM 
    public.products p
JOIN 
    public.nutritional_information ni USING(product_id)
ORDER BY ni.protein DESC
LIMIT 1;

-- Четвёртый запрос: Посчитать сумму калорий по каждой категории, исключая продукты с нулевым содержанием жиров
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

-- Пятый запрос: Рассчитать среднюю цену товаров по каждой категории
SELECT 
    c.category_name, ROUND(AVG(p.price), 2) AS средняя_цена
FROM 
    public.categories c
JOIN 
    public.products p USING(category_id)
GROUP BY 
    c.category_name;