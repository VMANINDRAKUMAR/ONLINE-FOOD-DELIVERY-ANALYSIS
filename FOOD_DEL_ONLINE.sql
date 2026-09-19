CREATE DATABASE IF NOT EXISTS FOOD_DEL_ONLINE;
USE FOOD_DEL_ONLINE;

DROP TABLE IF EXISTS food_orders;

CREATE TABLE food_orders (
 Order_ID VARCHAR(20) PRIMARY KEY, Customer_ID VARCHAR(20), Customer_Age INT,
 Customer_Gender VARCHAR(20), City VARCHAR(50), Area VARCHAR(50),
 Restaurant_ID VARCHAR(20), Restaurant_Name VARCHAR(100), Cuisine_Type VARCHAR(50),
 Order_Date DATE, Order_Time TIME, Delivery_Time_Min DECIMAL(8,2),
 Distance_km DECIMAL(8,2), Order_Value DECIMAL(10,2), Discount_Applied DECIMAL(10,2),
 Final_Amount DECIMAL(10,2), Payment_Mode VARCHAR(30), Order_Status VARCHAR(30),
 Cancellation_Reason VARCHAR(100), Delivery_Partner_ID VARCHAR(20),
 Delivery_Rating DECIMAL(3,2), Restaurant_Rating DECIMAL(3,2),
 Order_Day VARCHAR(20), Peak_Hour BOOLEAN, Profit_Margin DECIMAL(6,4),
 Order_Hour INT, Order_Day_Type VARCHAR(20), Age_Group VARCHAR(20),
 Profit_Amount DECIMAL(12,2), Delivery_Performance VARCHAR(30),
 Discount_Pct DECIMAL(8,2), Month CHAR(7)
);

-- Import the cleaned CSV with LOAD DATA LOCAL INFILE after adjusting the path.

-- 1 Top-spending customers
SELECT Customer_ID, SUM(Final_Amount) AS total_spend
FROM food_orders GROUP BY Customer_ID ORDER BY total_spend DESC LIMIT 10;

-- 2 Age group vs order value
SELECT Age_Group, COUNT(*) AS orders, AVG(Final_Amount) AS avg_order_value,
SUM(Final_Amount) AS revenue
FROM food_orders GROUP BY Age_Group ORDER BY revenue DESC;

-- 3 Weekend vs weekday
SELECT Order_Day_Type, COUNT(*) AS orders, AVG(Final_Amount) AS avg_order_value
FROM food_orders GROUP BY Order_Day_Type;

-- 4 Monthly revenue
SELECT Month, SUM(Final_Amount) AS revenue
FROM food_orders GROUP BY Month ORDER BY Month;

-- 5 Discount impact on profit
SELECT CASE WHEN Discount_Pct=0 THEN '0%'
 WHEN Discount_Pct<=10 THEN '1-10%' WHEN Discount_Pct<=20 THEN '11-20%'
 WHEN Discount_Pct<=30 THEN '21-30%' ELSE '30%+' END AS discount_band,
 COUNT(*) AS orders, AVG(Profit_Amount) AS avg_profit
FROM food_orders GROUP BY discount_band ORDER BY avg_profit DESC;

-- 6 High-revenue cities and cuisines
SELECT City, Cuisine_Type, COUNT(*) AS orders, SUM(Final_Amount) AS revenue
FROM food_orders GROUP BY City, Cuisine_Type ORDER BY revenue DESC LIMIT 20;

-- 7 Average delivery time by city
SELECT City, AVG(Delivery_Time_Min) AS avg_delivery_minutes
FROM food_orders GROUP BY City ORDER BY avg_delivery_minutes;

-- 8 Distance vs delivery delay
SELECT CASE WHEN Distance_km<=5 THEN '0-5 km' WHEN Distance_km<=10 THEN '5-10 km'
WHEN Distance_km<=20 THEN '10-20 km' WHEN Distance_km<=30 THEN '20-30 km'
ELSE '30-40 km' END AS distance_band,
COUNT(*) AS orders, AVG(Delivery_Time_Min) AS avg_delivery_minutes
FROM food_orders GROUP BY distance_band ORDER BY avg_delivery_minutes;

-- 9 Delivery rating vs delivery time
SELECT Delivery_Rating, COUNT(*) AS orders, AVG(Delivery_Time_Min) AS avg_delivery_minutes
FROM food_orders GROUP BY Delivery_Rating ORDER BY Delivery_Rating;

-- 10 Top-rated restaurants
SELECT Restaurant_Name, COUNT(*) AS orders, AVG(Restaurant_Rating) AS avg_rating
FROM food_orders GROUP BY Restaurant_Name HAVING COUNT(*)>=20
ORDER BY avg_rating DESC, orders DESC LIMIT 10;

-- 11 Cancellation rate by restaurant
SELECT Restaurant_Name, COUNT(*) AS orders,
100*AVG(Order_Status='Cancelled') AS cancellation_rate_pct
FROM food_orders GROUP BY Restaurant_Name
ORDER BY cancellation_rate_pct DESC LIMIT 10;

-- 12 Cuisine-wise performance
SELECT Cuisine_Type, COUNT(*) AS orders, SUM(Final_Amount) AS revenue,
AVG(Restaurant_Rating) AS avg_restaurant_rating,
AVG(Delivery_Time_Min) AS avg_delivery_minutes
FROM food_orders GROUP BY Cuisine_Type ORDER BY revenue DESC;

-- 13 Peak hour demand
SELECT Peak_Hour, COUNT(*) AS orders, AVG(Final_Amount) AS avg_order_value
FROM food_orders GROUP BY Peak_Hour;

-- 14 Payment mode preferences
SELECT Payment_Mode, COUNT(*) AS orders,
100*COUNT(*)/(SELECT COUNT(*) FROM food_orders) AS share_pct
FROM food_orders GROUP BY Payment_Mode ORDER BY orders DESC;

-- 15 Cancellation reason analysis
SELECT Cancellation_Reason, COUNT(*) AS cancellations
FROM food_orders WHERE Order_Status='Cancelled'
GROUP BY Cancellation_Reason ORDER BY cancellations DESC;

-- KPI summary
SELECT COUNT(*) AS total_orders, SUM(Final_Amount) AS total_revenue,
AVG(Final_Amount) AS avg_order_value, AVG(Delivery_Time_Min) AS avg_delivery_time,
100*AVG(Order_Status='Cancelled') AS cancellation_rate_pct,
AVG(Delivery_Rating) AS avg_delivery_rating,
100*AVG(Profit_Margin) AS avg_profit_margin_pct
FROM food_orders;
