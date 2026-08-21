CREATE TABLE sales (
    order_id      INTEGER PRIMARY KEY,
    customer_name TEXT,
    order_date    TEXT,
    category      TEXT,
    sub_category  TEXT,
    product_name  TEXT,
    quantity      INTEGER,
    unit_price    REAL,
    total_price   REAL,
    region        TEXT
);

CREATE TABLE region_managers (
    region       TEXT PRIMARY KEY,
    manager_name TEXT
);

INSERT INTO region_managers VALUES
    ('East',  'Elena Park'),
    ('West',  'Marcus Cole'),
    ('South', 'Priya Nair'),
    ('North', 'Tom Becker');

SELECT order_id, customer_name, product_name, total_price
FROM sales
WHERE category = 'Clothing' AND region = 'West'
ORDER BY total_price DESC;

SELECT customer_name, SUM(total_price) AS total_spent
FROM sales
GROUP BY customer_name
ORDER BY total_spent DESC
LIMIT 5;

SELECT AVG(total_price) AS avg_order_value
FROM sales;

SELECT region, AVG(total_price) AS avg_order_value, COUNT(*) AS num_orders
FROM sales
GROUP BY region
ORDER BY avg_order_value DESC;

SELECT s.region, rm.manager_name, COUNT(*) AS orders, SUM(s.total_price) AS revenue
FROM sales s
JOIN region_managers rm ON s.region = rm.region
GROUP BY s.region, rm.manager_name
ORDER BY revenue DESC;

SELECT customer_name, total_price
FROM sales
WHERE total_price > (SELECT AVG(total_price) FROM sales)
ORDER BY total_price DESC
LIMIT 10;

SELECT order_id, customer_name, total_price,
    CASE
        WHEN total_price >= 5000 THEN 'High Value'
        WHEN total_price >= 2000 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS order_size
FROM sales
ORDER BY total_price DESC
LIMIT 10;
