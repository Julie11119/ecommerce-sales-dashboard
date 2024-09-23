# app.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="E-commerce Sales Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load the data with preprocessing
@st.cache_data
def load_data():
    # Load the dataset
    df = pd.read_csv('synthetic_ecommerce_orders.csv')
    
    # Data Cleaning and Preprocessing
    
    # 1. Handle Missing Values
    # Replace missing values with appropriate values or drop rows
    df.replace('?', np.nan, inplace=True)
    df.dropna(inplace=True)  # Alternatively, you can fill missing values
    
    # 2. Data Type Conversions
    df['order_date'] = pd.to_datetime(df['order_date'])
    numeric_columns = ['quantity', 'order_price', 'total_amount', 'age']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # 3. Remove Duplicates
    df.drop_duplicates(inplace=True)
    
    # 4. Feature Engineering
    # Extract date-related features
    df['month'] = df['order_date'].dt.month
    df['year'] = df['order_date'].dt.year
    df['day_of_week'] = df['order_date'].dt.day_name()
    df['hour'] = df['order_date'].dt.hour
    
    # Create age groups
    df['age_group'] = pd.cut(df['age'], bins=[17, 24, 34, 44, 54, 64, np.inf],
                             labels=['18-24', '25-34', '35-44', '45-54', '55-64', '65+'])
    
    # 5. Standardize Categorical Variables
    categorical_columns = ['gender', 'payment_method', 'category', 'subcategory', 'product_name', 'country']
    for col in categorical_columns:
        df[col] = df[col].str.strip().str.title()
    
    return df

df = load_data()

# Dashboard title
st.title('🛍️ E-commerce Sales Dashboard')

# Sidebar filters
st.sidebar.header('Filter Options')

# Organize filters into expanders
with st.sidebar.expander("Date Range", expanded=True):
    # Date range filter
    min_date = df['order_date'].min()
    max_date = df['order_date'].max()
    start_date = st.date_input('Start date', min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.date_input('End date', min_value=min_date, max_value=max_date, value=max_date)

with st.sidebar.expander("Category Filters", expanded=True):
    # Category filter
    categories = df['category'].unique()
    selected_categories = st.multiselect('Select Categories', categories, default=categories)
    
    # Update subcategories based on selected categories
    if selected_categories:
        filtered_subcategories = df[df['category'].isin(selected_categories)]['subcategory'].unique()
    else:
        filtered_subcategories = df['subcategory'].unique()
    
    # Subcategory filter
    selected_subcategories = st.multiselect('Select Subcategories', filtered_subcategories, default=filtered_subcategories)

with st.sidebar.expander("Customer Demographics", expanded=False):
    # Gender filter
    genders = df['gender'].unique()
    selected_genders = st.multiselect('Select Genders', genders, default=genders)
    
    # Age group filter
    age_groups = df['age_group'].unique()
    selected_age_groups = st.multiselect('Select Age Groups', age_groups, default=age_groups)

with st.sidebar.expander("Payment Methods", expanded=False):
    # Payment method filter
    payment_methods = df['payment_method'].unique()
    selected_payment_methods = st.multiselect('Select Payment Methods', payment_methods, default=payment_methods)


# Apply filters
mask = (
    (df['order_date'] >= pd.to_datetime(start_date)) &
    (df['order_date'] <= pd.to_datetime(end_date)) &
    (df['category'].isin(selected_categories)) &
    (df['subcategory'].isin(selected_subcategories)) &
    (df['gender'].isin(selected_genders)) &
    (df['age_group'].isin(selected_age_groups)) &
    (df['payment_method'].isin(selected_payment_methods))
)
filtered_data = df.loc[mask]

# Check if filtered data is empty
if filtered_data.empty:
    st.warning('No data matches the selected filters. Please adjust your filter selections.')
else:
    # Display key metrics
    st.markdown("## 📊 Key Metrics")
    total_revenue = filtered_data['total_amount'].sum()
    total_orders = filtered_data['order_id'].nunique()
    aov = total_revenue / total_orders if total_orders > 0 else 0
    total_customers = filtered_data['customer_id'].nunique()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric('Total Revenue', f'${total_revenue:,.2f}')
    col2.metric('Total Orders', f'{total_orders}')
    col3.metric('Average Order Value', f'${aov:,.2f}')
    col4.metric('Total Customers', f'{total_customers}')

    # Sales Over Time
    st.markdown("## 📈 Sales Over Time")
    sales_over_time = filtered_data.groupby(filtered_data['order_date'].dt.to_period('D')).agg({'total_amount': 'sum'}).reset_index()
    sales_over_time['order_date'] = sales_over_time['order_date'].dt.to_timestamp()
    fig_sales_time = px.line(sales_over_time, x='order_date', y='total_amount', title='Total Sales Over Time',
                             labels={'order_date': 'Order Date', 'total_amount': 'Total Sales ($)'})
    st.plotly_chart(fig_sales_time, use_container_width=True)

    # Sales by Category and Subcategory
    st.markdown("## 🛍️ Sales by Category and Subcategory")
    sales_by_category = filtered_data.groupby('category').agg({'total_amount': 'sum'}).reset_index()
    fig_sales_category = px.bar(sales_by_category, x='category', y='total_amount', title='Sales by Category',
                                labels={'category': 'Category', 'total_amount': 'Total Sales ($)'})
    st.plotly_chart(fig_sales_category, use_container_width=True)

    sales_by_subcategory = filtered_data.groupby('subcategory').agg({'total_amount': 'sum'}).reset_index()
    fig_sales_subcategory = px.bar(sales_by_subcategory, x='subcategory', y='total_amount', title='Sales by Subcategory',
                                   labels={'subcategory': 'Subcategory', 'total_amount': 'Total Sales ($)'})
    fig_sales_subcategory.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_sales_subcategory, use_container_width=True)

    # Top 10 Products
    st.markdown("## 🏆 Top 10 Products")
    top_products = filtered_data.groupby('product_name').agg({'quantity': 'sum', 'total_amount': 'sum'}).reset_index()
    top_products = top_products.sort_values(by='total_amount', ascending=False).head(10)
    fig_top_products = px.bar(top_products, x='product_name', y='total_amount', title='Top 10 Products by Sales',
                              labels={'product_name': 'Product Name', 'total_amount': 'Total Sales ($)'})
    fig_top_products.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_top_products, use_container_width=True)

    # Sales by Day of Week
    st.markdown("## 📅 Sales by Day of Week")
    sales_by_day = filtered_data.groupby('day_of_week').agg({'total_amount': 'sum'}).reset_index()
    # Reorder days of the week
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    sales_by_day['day_of_week'] = pd.Categorical(sales_by_day['day_of_week'], categories=days_order, ordered=True)
    sales_by_day = sales_by_day.sort_values('day_of_week')
    fig_sales_day = px.bar(sales_by_day, x='day_of_week', y='total_amount', title='Sales by Day of Week',
                           labels={'day_of_week': 'Day of Week', 'total_amount': 'Total Sales ($)'})
    st.plotly_chart(fig_sales_day, use_container_width=True)

    # Customer Demographics
    st.markdown("## 👥 Customer Demographics")

    # Age Group Distribution
    st.markdown("### Age Group Distribution")
    age_group_counts = filtered_data['age_group'].value_counts().sort_index().reset_index()
    age_group_counts.columns = ['age_group', 'count']
    fig_age_group = px.bar(age_group_counts, x='age_group', y='count', title='Age Group Distribution',
                           labels={'age_group': 'Age Group', 'count': 'Number of Customers'})
    st.plotly_chart(fig_age_group, use_container_width=True)

    # Gender Distribution
    st.markdown("### Gender Distribution")
    gender_counts = filtered_data['gender'].value_counts().reset_index()
    gender_counts.columns = ['gender', 'count']
    fig_gender = px.pie(gender_counts, names='gender', values='count', title='Gender Distribution')
    st.plotly_chart(fig_gender, use_container_width=True)

    # Payment Methods Used
    st.markdown("## 💳 Payment Methods Used")
    payment_counts = filtered_data['payment_method'].value_counts().reset_index()
    payment_counts.columns = ['payment_method', 'count']
    fig_payment = px.pie(payment_counts, names='payment_method', values='count', title='Payment Methods')
    st.plotly_chart(fig_payment, use_container_width=True)

    # Geographic Distribution (if location data is available)
    st.markdown("## 🌍 Sales by Country")
    sales_by_country = filtered_data.groupby('country').agg({'total_amount': 'sum'}).reset_index()
    fig_sales_country = px.choropleth(
        sales_by_country,
        locations='country',
        locationmode='country names',
        color='total_amount',
        title='Sales by Country',
        color_continuous_scale='Blues',
        labels={'total_amount': 'Total Sales ($)'}
    )
    st.plotly_chart(fig_sales_country, use_container_width=True)

    # Download Filtered Data
    st.markdown("## 📥 Download Filtered Data")
    csv = filtered_data.to_csv(index=False)
    st.download_button(label='Download CSV', data=csv, file_name='filtered_data.csv', mime='text/csv')
