🛍️ E-commerce Sales Dashboard
Overview
This project is a fully functional E-commerce Sales Dashboard built using Streamlit and Plotly. The dashboard provides an interactive way to explore and analyze a synthetic dataset of e-commerce sales, offering insights into sales trends, product categories, customer demographics, payment methods, and more.

Key Features
📊 Sales Analysis:

View total sales, total orders, and average order value.
Track sales over time and across categories, subcategories, and countries.
🛍️ Product Insights:

Identify the top-selling products and analyze sales by category and subcategory.
👥 Customer Demographics:

Analyze customer data by gender, age group, and geographic location.
💳 Payment Method Analysis:

Explore the distribution of payment methods used in orders.
📅 Drill-down Filter System:

Hierarchical filters for product categories and subcategories.
Collapsible sections for better user experience.
Multi-select options to allow filtering by multiple categories, subcategories, genders, etc.
Table of Contents
Key Features
Technologies Used
Installation
Usage
How to Run
Screenshots
Data Preprocessing
License
Technologies Used
Python: The main programming language.
Streamlit: For building the interactive web app.
Plotly: For creating interactive visualizations and charts.
Pandas: For data manipulation and analysis.
Faker: For generating synthetic customer and product data.
randomtimestamp: For generating random timestamps in the dataset.
Installation
1. Clone the Repository
bash
Copy code
git clone https://github.com/your-username/ecommerce-sales-dashboard.git
cd ecommerce-sales-dashboard
2. Install the Required Dependencies
Make sure you have Python installed on your system, then install the dependencies listed in the requirements.txt file:

bash
Copy code
pip install -r requirements.txt
This will install the following packages:

pandas
numpy
matplotlib
seaborn
plotly
streamlit
Faker
randomtimestamp
Usage
Running the App Locally
To run the app locally, simply use Streamlit to launch it:

bash
Copy code
streamlit run app.py
Once the app is running, it will automatically open in your default browser. If it doesn’t, navigate to the URL shown in your terminal (usually http://localhost:8501/).

Exploring the Dashboard
Filters: Use the sidebar to filter data by date range, product categories, subcategories, customer demographics, and payment methods.
Charts: View various interactive charts and graphs that provide insights into e-commerce sales trends, customer demographics, and more.
Download Data: You can download the filtered data as a CSV file.
How to Run on Streamlit Community Cloud
Fork this repository and push your code to GitHub.
Go to Streamlit Community Cloud and sign in.
Deploy your GitHub repository as a Streamlit app by connecting it to Streamlit Cloud.
Once deployed, you will get a shareable link where others can interact with the dashboard.
