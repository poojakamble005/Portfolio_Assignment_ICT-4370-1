"""
Stock Data Analysis and Visualization
Author: Pooja Kamble
Date: June 3, 2023
Description: This program reads stock data from a SQLite database, performs analysis and visualization, and saves the results as HTML files.

Dependencies:
- module1
- pandas
- numpy
- sqlite3
- plotly.graph_objects
- plotly.express
"""

import module1
import pandas as pd
import numpy as np
import sqlite3
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates

# Function to read tables from the database
def read_tables_from_db(table):
    try:
        conn = sqlite3.connect('Investor.db')
        # Read the specified table from the database into a pandas DataFrame
        df_stocks = pd.read_sql_query(f"SELECT * FROM {table}", conn)
        return df_stocks
    except Exception as e:
        print("An error occurred while connecting or using SQLite3:", e)

# Read the 'stocks' table from the database into a DataFrame
df_stocks = read_tables_from_db('stocks')
df_stocks['NO_SHARES'] = df_stocks['NO_SHARES'].astype('int')

# Read the 'AllStocks' table from the database into a DataFrame
allstocks = read_tables_from_db('AllStocks')
df_allstocks = pd.DataFrame(allstocks)

# Replace 'GOOG' with 'GOOGL' in the 'Symbol' column of df_allstocks
df_allstocks['Symbol'].replace('GOOG', 'GOOGL', inplace=True)

# Function to join df_allstocks and df_stocks based on 'Symbol' and process the joined DataFrame
def get_joint_df(df_allstocks: pd.DataFrame, df_stocks: pd.DataFrame):
    # Inner join df_allstocks and df_stocks on 'Symbol'
    df_join = pd.merge(df_allstocks, df_stocks, left_on='Symbol', right_on='SYMBOL', how='inner')
    # Replace '-' with NaN in the 'Close' column
    df_join['Close'] = df_join['Close'].replace('-', np.nan)
    # Convert 'Close' column to float
    df_join['Close'] = df_join['Close'].astype(float)
    # Convert 'Date' column to datetime format
    df_join['Date'] = pd.to_datetime(df_join['Date'], format="%d-%b-%y")
    # Calculate the stock day value by multiplying 'Close' and 'NO_SHARES' columns
    df_join['stock_day_value'] = df_join['Close'] * df_join['NO_SHARES']
    # Sort the DataFrame by 'Date' in ascending order
    df_join = df_join.sort_values('Date', ascending=True)
    return df_join

# Call the function to get the joined DataFrame
df_join = get_joint_df(df_allstocks, df_stocks)

#Graphing starts here

# Define colors for the line plot
colors = ['rgb(0, 114, 178)', 'rgb(230, 159, 0)', 'rgb(0, 158, 115)', 'rgb(204, 121, 167)', 'rgb(86, 180, 233)']

# Create a line plot using plotly.graph_objects
fig2 = go.Figure()

# Iterate over each symbol and its corresponding data group
for i, (symbol, data) in enumerate(df_join.groupby('Symbol')):
    fig2.add_trace(go.Scatter(
        x=data['Date'],
        y=data['stock_day_value'],
        name=symbol,
        hovertemplate='<b>%{y:$,.2f}</b><br>%{x}<br><b>%{name}</b>',
        line=dict(width=2, color=colors[i % len(colors)])
    ))

# Update the layout of the line plot
fig2.update_layout(
    title='Stock Value Over Time',
    xaxis_title='Date',
    yaxis_title='Stock Value',
    legend_title='Symbol',
    plot_bgcolor='white',
    hovermode='x unified',
    template='plotly_dark'
)

# Create a histogram using plotly.express
fig = px.histogram(df_join, x='Date', y='stock_day_value', color='Symbol', nbins=30,
                   title='Distribution of Stock Values')
fig.update_layout(xaxis_title='Date', yaxis_title='Stock Value')

# Save the histograms as HTML files
fig.write_html("histogram_plot.html")
fig2.write_html("plotly_dark_line_plot.html")

# Convert the DataFrame to the required format for candlestick_ohlc
ohlc = df_join[['Date', 'Open', 'High', 'Low', 'Close']].copy()
ohlc['Date'] = ohlc['Date'].map(mpl_dates.date2num)
ohlc['Close'] = pd.to_numeric(ohlc['Close'], errors='coerce')
ohlc['Open'] = pd.to_numeric(ohlc['Open'], errors='coerce')
ohlc['High'] = pd.to_numeric(ohlc['High'], errors='coerce')
ohlc['Low'] = pd.to_numeric(ohlc['Low'], errors='coerce')

#Create a new figure and axis
fig, ax = plt.subplots()
# Plot the candlestick chart
candlestick_ohlc(ax, ohlc.values, width=0.10, colorup='green', colordown='red')

# Set x-axis labels to date format
ax.xaxis_date()
# Set axis labels and title
ax.set_xlabel('Date')
ax.set_ylabel('Price')
ax.set_title('Candlestick Chart')
ax.grid(False)
ax.set_xticklabels([])
ax.set_yticklabels([])


# Show the plot
plt.savefig('candlestick_chart.png', format='png')


