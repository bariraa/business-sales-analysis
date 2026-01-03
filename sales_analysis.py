import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Load & Explore Data
def load_data(file_path):
    df = pd.read_csv(file_path)
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
    df = df[df['quantity'] > 0]
    df = df.dropna(subset=['product'])
    df['price'] = df.groupby('product')['price'].transform(lambda x: x.fillna(x.mean()))
    df['price'] = df['price'].fillna(df['price'].median())
    df['region'] = df['region'].fillna('Unknown')
    df['category'] = df['category'].fillna('Unknown')
    df['date'] = pd.to_datetime(df['date'], errors='coerce')               
    df['quantity'] = df['quantity'].astype(int)
    df['total'] = df['quantity'] * df['price']
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year

    return df

# Calculate KPIs
def calculate_kpis(df):
    revenue = df['total'].sum()
    orders = len(df)
    best_product_revenue = df.groupby("product")["total"].sum().idxmax()
    best_product_quantity = df.groupby("product")["quantity"].sum().idxmax()
    least_demanded = df.groupby("product")["quantity"].sum().idxmin()
    least_revenue = df.groupby("product")["total"].sum().idxmin()
    best_category = df.groupby("category")["total"].sum().idxmax()
    best_region = df.groupby("region")["total"].sum().idxmax()
    avg_order_value = revenue / orders

    kpis = {
        "💰 Total Revenue" :f"Rs {revenue:,.0f}",
        "🛒 Total Orders" : orders,
        "📊 Average Order Value": f"Rs {round(avg_order_value, 2)}",
        "🏆 Highest Revenue Product" : best_product_revenue,
        "📉 Lowest Revenue Product" : least_revenue,
        "🔥 Most Demanded Product" : best_product_quantity,
        "❄️ Least Demanded Product" : least_demanded,
        "🏅 Best Category" : best_category,
        "🌍 Best Region" : best_region
    }

    return kpis

# Plot Graphs

def sales_trends(df):
    df_graph = df.dropna(subset=['date']) 
    sales = df_graph.groupby("date")['total'].sum()
    fig = Figure(figsize=(6,4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(sales.index, sales.values)
    ax.set_title("Sales Trend Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Total Sales")
    fig.autofmt_xdate() 
    return fig


def monthly_sales_trend(df):
    df_graph = df.dropna(subset=['date']) 
    latest_year = df_graph['year'].max()
    monthly_sales = (df_graph[df_graph['year'] == latest_year].groupby('month')['total'].sum().reset_index())
    fig = Figure(figsize=(6,4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(monthly_sales['month'], monthly_sales['total'], marker='o')
    ax.set_title(f"Monthly Sales Trend ({latest_year})")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Sales")
    ax.set_xticks(range(1, 13))
    return fig


def yearly_sales_trend(df):
    df_graph = df.dropna(subset=['date']) 
    yearly_sales = (df_graph.groupby('year')['total'].sum().reset_index())
    fig = Figure(figsize=(6,4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(yearly_sales['year'], yearly_sales['total'], marker='o')
    ax.set_title("Yearly Sales Trend")
    ax.set_xlabel("Year")
    ax.set_ylabel("Total Sales")
    ax.set_xticks(yearly_sales['year'])
    return fig


def product_sales(df):
    prod_sales = df.groupby("product")['total'].sum()
    fig = Figure(figsize=(6,4), dpi=100)
    ax = fig.add_subplot(111)
    ax.bar(prod_sales.index, prod_sales.values)
    ax.set_title("Sales by Product")
    ax.set_xlabel("Product")
    ax.set_ylabel("Total Sales")
    ax.tick_params(axis='x', rotation=45)
    fig.tight_layout()
    return fig

def category_sales(df):
    cat_sales = df.groupby("category")['total'].sum()
    fig = Figure(figsize=(6,4), dpi=100)
    ax = fig.add_subplot(111)
    ax.pie(cat_sales, labels=cat_sales.index, autopct='%1.1f%%')
    ax.set_title('Category Contribution to Sales')
    return fig

def region_sales(df):
    reg_sales = df.groupby("region")['total'].sum()
    fig = Figure(figsize=(6,4), dpi=100)
    ax = fig.add_subplot(111)
    ax.bar(reg_sales.index, reg_sales.values)
    ax.set_title("Sales by Region")
    ax.set_xlabel("Region")
    ax.set_ylabel("Total Sales")
    return fig

