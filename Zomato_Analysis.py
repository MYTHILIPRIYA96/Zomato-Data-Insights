import streamlit as st
import mysql.connector
import pandas as pd

def db_config():
    return {  
            'user': '3obbBvALArqQPqW.root',
            'password': 'MtV1PAc27naJolYM',
            'host': 'gateway01.ap-southeast-1.prod.aws.tidbcloud.com',
            'database': 'zomato'
        }
conn = mysql.connector.connect(**db_config())


queries = {"Peak Ordering Locations":

           """SELECT location, COUNT(*) AS order_count
           FROM orders o
           JOIN restaurants r ON o.restaurant_id = r.restaurant_id
           GROUP BY location
           ORDER BY order_count DESC;""",

           "Peak Ordering Times":

            """SELECT HOUR(order_date) AS order_hour, COUNT(*) AS order_count
           FROM orders
           GROUP BY order_hour
           ORDER BY order_count DESC;""",

           "Orders with Delivery Delays":

           """SELECT order_id, order_date, delivery_time
           FROM orders
           WHERE TIMESTAMPDIFF(MINUTE, order_date, delivery_time) > 30;""",

           "Cancelled Deliveries":

           """SELECT order_id, order_date, status
           FROM orders
           WHERE status = 'Cancelled';""",

           "Top Customers by Order Frequency":

           """SELECT c.customer_id, c.name, COUNT(o.order_id) AS total_orders
           FROM customers c JOIN orders o ON c.customer_id = o.customer_id
           GROUP BY c.customer_id, c.name
           ORDER BY total_orders DESC
           LIMIT 10;""",

           "Top Customers by Total Order Value":

           """SELECT c.customer_id, c.name, round(SUM(o.total_amount)) AS total_order_value
           FROM customers c JOIN orders o ON c.customer_id = o.customer_id
           GROUP BY c.customer_id, c.name
           ORDER BY total_order_value DESC
           LIMIT 10;""",

           "Average Delivery Time":

           """SELECT round(AVG(TIMESTAMPDIFF(MINUTE, order_date, delivery_time))) AS average_delivery_time
           FROM orders;""",

           "Preferred Cuisines":

           """SELECT preferred_cuisine, COUNT(*) AS cuisine_count
           FROM customers
           GROUP BY preferred_cuisine
           ORDER BY cuisine_count DESC;""",
          
          "Deliveries per Delivery Person":

           """SELECT dp.delivery_person_id, dp.name, COUNT(d.delivery_id) AS total_deliveries
           FROM delivery_persons dp
           JOIN deliveries d ON dp.delivery_person_id = d.delivery_person_id
           GROUP BY dp.delivery_person_id, dp.name
           ORDER BY total_deliveries DESC;""",

           "Average Delivery Time by Delivery Person":

           """SELECT dp.delivery_person_id, dp.name, round(AVG(TIMESTAMPDIFF(MINUTE, o.order_date, o.delivery_time))) AS average_delivery_time
           FROM delivery_persons dp
           JOIN deliveries d ON dp.delivery_person_id = d.delivery_person_id
           JOIN orders o ON d.order_id = o.order_id
           GROUP BY dp.delivery_person_id, dp.name
           ORDER BY average_delivery_time;""",

           "Most Popular Cuisines":

            """SELECT r.cuisine_type, COUNT(o.order_id) AS cuisine_frequency
            FROM restaurants r
            JOIN orders o ON r.restaurant_id = o.restaurant_id
            GROUP BY r.cuisine_type
            ORDER BY cuisine_frequency DESC""",

            " Most Popular Restaurants by Order Frequency":

            """SELECT r.restaurant_id, r.name, COUNT(o.order_id) AS order_frequency
            FROM restaurants r
            JOIN orders o ON r.restaurant_id = o.restaurant_id
            GROUP BY r.restaurant_id, r.name
            ORDER BY order_frequency DESC;""",

           "Average Order Value by Restaurant":

           """SELECT r.restaurant_id, r.name, 
           ROUND(AVG(o.total_amount), 2) AS average_order_value
           FROM restaurants r
           JOIN orders o ON r.restaurant_id = o.restaurant_id
           GROUP BY r.restaurant_id, r.name
           ORDER BY average_order_value DESC""", 
           
           "Identify the days with the most orders":

           """SELECT DAYOFWEEK(order_date) AS day_of_week, COUNT(*) AS order_count
           FROM orders
           GROUP BY day_of_week
           ORDER BY order_count DESC;""",

           "Restaurants with Highest Total Order Value":

           """SELECT r.restaurant_id, r.name, round(SUM(o.total_amount)) AS total_order_value
           FROM restaurants r
           JOIN orders o ON r.restaurant_id = o.restaurant_id
           GROUP BY r.restaurant_id, r.name
           ORDER BY total_order_value DESC
           LIMIT 10;""",

           "Peak Ordering Times for Each Restaurant":
           
           """SELECT r.restaurant_id, r.name, HOUR(o.order_date) AS order_hour, COUNT(o.order_id) AS hourly_order_frequency
           FROM restaurants r
           JOIN orders o ON r.restaurant_id = o.restaurant_id
           GROUP BY r.restaurant_id, r.name, order_hour
           ORDER BY r.restaurant_id, hourly_order_frequency DESC;""",

           "restaurants with a high number of cancelled orders":

           """SELECT r.restaurant_id, r.name, COUNT(o.order_id) AS cancelled_orders
           FROM restaurants r
           JOIN orders o ON r.restaurant_id = o.restaurant_id
           WHERE o.status = 'Cancelled'
           GROUP BY r.restaurant_id, r.name
           ORDER BY cancelled_orders DESC
           LIMIT 10;""",

           "most popular cuisines among customers":

           """SELECT c.preferred_cuisine, COUNT(*) AS cuisine_count, round(AVG(o.total_amount)) AS average_order_value
           FROM customers c
           JOIN orders o ON c.customer_id = o.customer_id
           GROUP BY c.preferred_cuisine;""",

            "top 10 customers who have the highest total order value and  high average rating (above 4)":

            """SELECT c.customer_id, c.name, SUM(o.total_amount) AS total_order_value, round(AVG(o.feedback_rating)) AS Average_rating
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            GROUP BY c.customer_id, c.name
            HAVING average_rating > 4
            ORDER BY total_order_value DESC
            LIMIT 10;""",

            "identify orders that experienced significant delivery delays":

            """SELECT o.order_id, o.order_date, o.delivery_time, d.estimated_time,
            TIMESTAMPDIFF(MINUTE, o.order_date, o.delivery_time) AS actual_delivery_time,
            (TIMESTAMPDIFF(MINUTE, o.order_date, o.delivery_time) - d.estimated_time) AS delivery_delay
            FROM orders o
            JOIN deliveries d ON o.order_id = d.order_id
            WHERE (TIMESTAMPDIFF(MINUTE, o.order_date, o.delivery_time) - d.estimated_time) > 15
            ORDER BY delivery_delay DESC;"""}

st.title("Zomato Food Delivery Data Analysis")
st.write("Select a query to analyze")
st.subheader("20 Queries")

selected_query_name = st.selectbox("Choose a query:",list(queries.keys()))
if st.button("Run Query"):
    conn = mysql.connector.connect(**db_config())
    df = pd.read_sql(queries[selected_query_name],conn)
    st.write(df)