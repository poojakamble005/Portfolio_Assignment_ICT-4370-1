"""
Author: Pooja Kamble
Date: June 3, 2023
Description: This program analyzes stock data and generates visualizations. It reads stock information from CSV files, calculates earnings/losses, creates an investor object, and stores the data in a SQLite database. It also generates visualizations using the Plotly library.
"""


import module2 as invest
import os
import random
from datetime import datetime
import pandas as pd
import sqlite3
import json


def delete_db():
    """Function to delete existing database"""
    try:
        os.system('rm Investor.db')
    except:
        print("An error occurred while deleting older db")

# Deleting db
delete_db()

# Read both Stocks and Bonds files from the csv with Exception handling

def read_file(file_path):
    try:
        with open(file_path, 'r') as fileobj:
            stock_info_lst = []
            for line in fileobj.readlines():
                stock_info_lst.append(line)

            stock_info = []
            header = stock_info_lst[0].strip().split(',')
            for value in stock_info_lst[1:]:
                values = value.strip().split(',')
                stock_info.append({header[i]: values[i] for i in range(len(header))})
            return stock_info
    except FileNotFoundError:
        raise Exception("The file to read doesn't exist, please check the file path")
    except Exception as e:
        raise Exception(f"An error occurred while reading the file: {str(e)}")


def read_all_stocks(file_path):
    try:
        with open(file_path, 'r') as fileobj:
            allstocks = json.load(fileobj)
            return allstocks
    except FileNotFoundError:
        raise Exception("The file doesn't exist, please check the file path")
    except Exception as e:
        raise Exception(f"An error occurred while reading the file: {str(e)}")


# Change directory per your OS by using the 'cd' command to run in the proper directory
working_directory = os.getcwd()

# Creating/generating a list of file paths to read
file_paths = []
file_path_stocks = working_directory + '/' + 'Lesson6_Data_Stocks.csv'
# file_path_bonds = working_directory + '/' + 'Lesson6_Data_Bonds.csv'

file_paths.append(file_path_stocks)
# file_paths.append(file_path_bonds)


# Call the read function to read the CSV file
for file_path in file_paths:
    data = read_file(file_path)
    if 'Stocks' in file_path.split('/')[-1]:
        stock_info = data
    # elif 'Bonds' in file_path.split('/')[-1]:
    #     bonds_info = data


for i, stock in enumerate(stock_info):
    stock_name = stock['SYMBOL']
    try:
        NO_SHARES = int(stock_info[i]['NO_SHARES'])
        stock_info[i]['NO_SHARES'] = NO_SHARES
        CURRENT_VALUE = float(stock_info[i]['CURRENT_VALUE'])
        stock_info[i]['CURRENT_VALUE'] = CURRENT_VALUE
        PURCHASE_PRICE = float(stock_info[i]['PURCHASE_PRICE'])
        stock_info[i]['PURCHASE_PRICE'] = PURCHASE_PRICE
        PURCHASE_DATE = datetime.strptime(stock_info[i]['PURCHASE_DATE'], '%m/%d/%Y').date()
        stock_info[i]['PURCHASE_DATE'] = PURCHASE_DATE
    except TypeError as e:
        raise Exception("An error occurred while processing the stock information:", e)

    purchaseid = random.randint(1, 100)
    # Initiating stock class
    myStocks = invest.Stock(stock_name, NO_SHARES, CURRENT_VALUE, PURCHASE_PRICE, PURCHASE_DATE, purchaseid)
    loss_or_gain = myStocks.Calculate_lossorgain()
    Percentage_yield_loss = myStocks.Percentage_yield_loss_func()
    yearlyearnings_loss = myStocks.Yearlyearnings_loss()

    stock_info[i]['Earnings_Loss'] = loss_or_gain
    # stock_info[i]['Percentage Yield/Loss'] = Percentage_yield_loss
    stock_info[i]['Yearly_Earning_Loss'] = yearlyearnings_loss


# Investor Class
investor_id = 'ID_' + str(random.randint(500, 1000))
investor = invest.Investor(investor_id, 'Bob Smith', '720-000-0000')
investor.stocks = stock_info
# investor.bonds = bonds_info


# Creating a Database, Tables, and inserting into tables
try:
    conn = sqlite3.connect('Investor.db')
    cursor = conn.cursor()

    # Table for Stocks
    stock_col_headers = list(stock_info[0].keys())
    # Adding investor_id field to col headers
    stock_col_headers.append('INVESTOR_ID')
    # Create a table using the bond keys as column names
    column_names_stocks = ', '.join([f"{key} TEXT" for key in stock_col_headers])
    create_table_query_stocks = f"CREATE TABLE IF NOT EXISTS stocks ({column_names_stocks})"
    conn.execute(create_table_query_stocks)

    insert_query_stocks = "INSERT INTO stocks VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

    for stock in stock_info:
        values = (
            stock['SYMBOL'],
            stock['NO_SHARES'],
            stock['PURCHASE_PRICE'],
            stock['CURRENT_VALUE'],
            stock['PURCHASE_DATE'],
            stock['Earnings_Loss'],
            stock['Yearly_Earning_Loss'],
            investor.investor_id
        )
        conn.execute(insert_query_stocks, values)

except sqlite3.Error as e:
    print("An error connecting or while using sqlite3:", e)


# Table for AllStocks
file_path_allstocks = working_directory + '/' + 'AllStocks.json'
# Read using the function defined
all_stocks = read_all_stocks(file_path_allstocks)
all_stocks_col_headers = list(all_stocks[0].keys())

# Create a table using the bond keys as column names
# column_names_allstocks = ', '.join([f"{key} TEXT" for key in all_stocks_col_headers])
create_table_query_allstocks = f"CREATE TABLE IF NOT EXISTS AllStocks ( Symbol VARCHAR,Date VARCHAR,Open REAL,High REAL,Low REAL,Close REAL,Volume INTEGER)"
conn.execute(create_table_query_allstocks)

try:
    # sql = "INSERT INTO bonds VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    sql = '''
    INSERT INTO AllStocks (Symbol, Date, Open, High, Low, Close, Volume)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    '''

    for item in all_stocks:
        values = (
            item['Symbol'],
            item['Date'],
            item['Open'],
            item['High'],
            item['Low'],
            item['Close'],
            item['Volume']
        )
        conn.execute(sql, values)
except sqlite3.Error as e:
    print("An error connecting or while using sqlite3:", e)

# Read the 'stocks' table into a data frame
df_stocks = pd.read_sql_query("SELECT * FROM stocks", conn)
print("Stocks table:")
print(df_stocks)

# Read the 'AllStocks' table into a data frame
df_allstocks = pd.read_sql_query("SELECT * FROM AllStocks", conn)
print("AllStocks table:")
print(df_allstocks)

# Commit and Close the database cursor and connection
conn.commit()
cursor.close()
conn.close()
