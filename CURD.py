import streamlit as st
import mysql.connector

# Database Configuration
def db_config():
    return {
         'user': '3obbBvALArqQPqW.root',
         'password': 'MtV1PAc27naJolYM',
         'host': 'gateway01.ap-southeast-1.prod.aws.tidbcloud.com',
         'database': 'zomato'
    }

# Connect to the database
conn = mysql.connector.connect(**db_config())
cursor = conn.cursor()

# Streamlit app title
st.title("Zomato Data Entry Tool")

# Sidebar for navigation
options = ["Add Record", "Update Record", "Delete Record", "Create Table"]
selected_option = st.sidebar.selectbox("Select an operation:", options)

# Add Record
if selected_option == "Add Record":
    st.subheader("Add New Record")
    table_name = st.text_input("Enter table name:")
    if table_name:
        columns = st.text_input("Enter column names (comma-separated):")
        values = st.text_input("Enter values (comma-separated):")
        if columns and values:
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
            cursor.execute(sql)
            conn.commit()
            st.success("Record added successfully!")
            

# Update Record
elif selected_option == "Update Record":
    st.subheader("Update Existing Record")
    table_name = st.text_input("Enter table name:")
    if table_name:
        update_data = st.text_input("Enter update data (column=value, comma-separated):")
        where_clause = st.text_input("Enter where clause:")
        if update_data and where_clause:
            sql = f"UPDATE {table_name} SET {update_data} WHERE {where_clause}"
            cursor.execute(sql)
            conn.commit()
            st.success("Record updated successfully!")
            

# Delete Record
elif selected_option == "Delete Record":
    st.subheader("Delete Existing Record")
    table_name = st.text_input("Enter table name:")
    if table_name:
        where_clause = st.text_input("Enter where clause:")
        if where_clause:
            sql = f"DELETE FROM {table_name} WHERE {where_clause}"
            cursor.execute(sql)
            conn.commit()
            st.success("Record deleted successfully!")
           

# Create Table
elif selected_option == "Create Table":
    st.subheader("Create New Table")
    table_name = st.text_input("Enter table name:")
    if table_name:
        columns_schema = st.text_area("Enter column schema (e.g., id INT PRIMARY KEY, name VARCHAR(255)):")
        if columns_schema:
            sql = f"CREATE TABLE {table_name} ({columns_schema})"
            cursor.execute(sql)
            conn.commit()
            st.success("Table created successfully!")
            
# Close the database connection
conn.close()

