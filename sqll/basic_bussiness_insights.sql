--What is the total revenue generated?
SELECT SUM(order_value) AS total_revenue
FROM ecommerce_clean.orders;
-- How many total orders were placed?
SELECT COUNT(order_id) AS total_orders
FROM ecommerce_clean.orders;
--How many unique customers are there?

SELECT table_name, creation_time
FROM `central-element-478605-p7.ecommerce_clean.INFORMATION_SCHEMA.TABLES`
ORDER BY creation_time DESC;



--How many total items (quantity) were sold?,
SELECT SUM(quantity) AS total_items_sold
FROM ecommerce_clean.orders;

--What is the monthly revenue trend?
SELECT month,SUM(order_value) AS monthly_revenue
FROM ecommerce_clean.orders
GROUP BY month
ORDER BY month;
--Which are the top 10 best-selling products?(based on total quantity sold)
SELECT 
  product_id,
  SUM(quantity) AS total_quantity_sold
FROM `central-element-478605-p7.ecommerce_clean.orders`
GROUP BY product_id
ORDER BY total_quantity_sold DESC
LIMIT 10;





