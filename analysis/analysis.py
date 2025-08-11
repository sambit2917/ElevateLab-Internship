import pandas as pd
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv('sales.csv')

# See first few rows
print(df.head())

# Group by product and sum sales
sales_by_product = df.groupby('Product')['Sales'].sum()
print('\n Total sales by Product:\n', sales_by_product)

# Plot sales by product 
sales_by_product.plot(kind='bar', title='Total sales by product')
plt.ylabel('Sales')
plt.show()

# Group by date and sum sales 
sales_by_date = df.groupby('Date')['Sales'].sum()
print('\n Total sales by Date:\n', sales_by_date)

# Plot sales by date
sales_by_date.plot(kind='line', marker='o', title='Total sales over time')
plt.ylabel('Sales')
plt.show()