
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# This code is not the complete code of what I used in this projecct, this is a snippet of what I sourced from the internet.
# And this code will not run comfortable on a VS Code, it will be comfortable on the Jupyter Notebook server.
%matplotlib inline
sns.set(style="whitegrid")

df = pd.read_csv('data/SampleSuperstore.csv')


# Display first 5 rows
df.head()

# Show the shape (rows, columns)
df.shape
# Show the shape (rows, columns)
df.shape
# List all columns
df.columns

# General info (data types, nulls)
df.info()

# Summary stats for numeric columns
df.describe()

# Count missing values per column
df.isnull().sum()


df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])


df['Month'] = df['Order Date'].dt.month
df['Year'] = df['Order Date'].dt.year
df['Weekday'] = df['Order Date'].dt.day_name()



"""   STEP 3: Data Cleaning & Feature Engineering   """


df.dropna(inplace=True)  # Remove rows with missing values

df.fillna(0, inplace=True)


df.duplicated().sum()  # Check number of duplicates
df.drop_duplicates(inplace=True)

df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.month
df['Month_Name'] = df['Order Date'].dt.strftime('%B')
df['Weekday'] = df['Order Date'].dt.day_name()
df['Quarter'] = df['Order Date'].dt.quarter


months_order = ['January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December']
df['Month_Name'] = pd.Categorical(df['Month_Name'], categories=months_order, ordered=True)

# Profit margin = Profit / Sales
df['Profit_Margin'] = df['Profit'] / df['Sales']


plt.figure(figsize=(10, 5))
sns.boxplot(x=df['Sales'])
plt.title("Sales Distribution")
plt.show()



"""   4  This one is all about data display """
sales_over_time = df.groupby(['Order Date'])[['Sales', 'Profit']].sum().reset_index()

plt.figure(figsize=(14, 6))
plt.plot(sales_over_time['Order Date'], sales_over_time['Sales'], label='Sales')
plt.plot(sales_over_time['Order Date'], sales_over_time['Profit'], label='Profit')
plt.title('Sales and Profit Over Time')
plt.xlabel('Date')
plt.ylabel('Amount')
plt.legend()
plt.grid()
plt.show()


# Sales by Category and Sub-Category
plt.figure(figsize=(12, 6))
category_sales = df.groupby('Category')['Sales'].sum().sort_values()
category_sales.plot(kind='barh', color='teal')
plt.title("Total Sales by Category")
plt.xlabel("Sales")
plt.show()
plt.figure(figsize=(14, 6))
subcat_sales = df.groupby('Sub-Category')['Sales'].sum().sort_values()
subcat_sales.plot(kind='barh', color='orange')
plt.title("Total Sales by Sub-Category")
plt.xlabel("Sales")
plt.show()

# Top 10 Products by Sales

top_products = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 5))
top_products.plot(kind='bar', color='purple')
plt.title("Top 10 Products by Sales")
plt.ylabel("Sales")
plt.xticks(rotation=75)
plt.show()




plt.figure(figsize=(8, 5))
region_profit = df.groupby('Region')['Profit'].sum().sort_values()
region_profit.plot(kind='bar', color='green')
plt.title("Profit by Region")
plt.ylabel("Profit")
plt.xticks(rotation=45)
plt.show()



# Heatmap of Profit by Category and Region

pivot = df.pivot_table(index='Category', columns='Region', values='Profit', aggfunc='sum')
plt.figure(figsize=(8, 6))
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu")
plt.title("Profit by Category and Region")
plt.show()