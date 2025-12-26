import pandas as pd
import matplotlib.pyplot as plt


# Load & Explore Data
def load_data(file_path):
    
    df = pd.read_csv(file_path)
    print("Data loaded. Shape:",df.shape)
    print(df.head())
    return df

# Clean Data
def clean_data(df):

    df.columns = df.columns.str.strip().str.lower()
    column_map = {
    'qty': 'quantity',
    'product name': 'product',
    'cat': 'category',
    'unit price': 'price',
    'region_name': 'region',
    'sale date': 'date'
    }
    df = df.rename(columns=column_map)
    
    # validate required columns
    required_columns = ['product', 'category', 'quantity', 'price', 'date', 'region']
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.dropna(subset=['quantity'])
    df['price'] = df.groupby('product')['price'].transform(lambda x: x.fillna(x.mean()))
    df['price'] = df['price'].fillna(df['price'].median())
    df['region'] = df['region'].fillna('Unknown')
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])
    df['quantity'] = df['quantity'].astype(int)
    df['total'] = df['quantity'] * df['price']
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year

    return df

# Calculate KPIs
def calculate_kpis(df):
    revenue = df['total'].sum()
    orders = len(df)
    best_product = df.groupby("product")["total"].sum().idxmax()
    best_category = df.groupby("category")["total"].sum().idxmax()
    best_region = df.groupby("region")["total"].sum().idxmax()
    avg_order_value = revenue / orders

    kpis = {
        "Total Revenue" : revenue,
        "Total Orders" : orders,
        "Average Order Value": round(avg_order_value, 2),
        "Best Product" : best_product,
        "Best Category" : best_category,
        "Best Region" : best_region
    }

    return kpis

# Plot Graphs

def sales_trends(df):
    sales = df.groupby("date")['total'].sum()
    x = sales.index
    y = sales.values
    plt.figure()
    plt.plot(x,y, marker='o')
    plt.title("Sales Trend Over Time")
    plt.xlabel("Date")
    plt.ylabel("Total Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def product_sales(df):
    product_sales = df.groupby("product")['total'].sum()
    plt.figure()
    product_sales.plot(kind='bar')
    plt.title("Sales by Product")
    plt.xlabel("Product")
    plt.ylabel("Total Sales")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

def category_sales(df):
    category_sales = df.groupby("category")['total'].sum()
    plt.figure()
    plt.pie(category_sales, labels=category_sales.index, autopct='%1.1f%%')
    plt.title('Category Contribution to Sales')
    plt.show()

def region_sales(df):
    region_sales = df.groupby("region")['total'].sum()
    plt.figure()
    region_sales.plot(kind='bar')
    plt.title("Sales by Region")
    plt.xlabel("Region")
    plt.ylabel("Total Sales")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()