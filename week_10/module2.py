"""
Author: Pooja Kamble
Date: June 3, 2023
Description: This program analyzes stock data and generates visualizations. It also includes classes for managing investors and their portfolios.

Dependencies:
- module1
- pandas
- numpy
- sqlite3
- plotly.graph_objects
- plotly.express

"""

import datetime

# Investor class to generate details of the Investor who owns stocks/bonds
class Investor:
    def __init__(self, investor_id, name, phone_number):
        self.name = name
        self.investor_id = investor_id
        self.phone_number = phone_number
        self.stocks = []  # List to store the investor's stocks
        self.bonds = []  # List to store the investor's bonds


# Stock Class to define stocks and calculate the loss or gain in the portfolio  
class Stock():
    def __init__(self, stock_name, numofshares, currentprice, purchaseprice, purchasedate, purchaseid):
        self.stock_name = stock_name
        self.numofshares = numofshares
        self.purchaseprice = purchaseprice
        self.currentprice = currentprice
        self.purchasedate = purchasedate
        self.purchaseID = purchaseid

    # Function to calculate the loss/gain
    def Calculate_lossorgain(self):
        earnings_loss = (self.currentprice - self.purchaseprice) * self.numofshares
        earnings_loss = round(earnings_loss, 2)
        return earnings_loss

    # Function to calculate the percentage yield/loss
    def Percentage_yield_loss_func(self):
        Percentage_yield_loss = (self.currentprice - self.purchaseprice) / self.purchaseprice * 100
        Percentage_yield_loss = round(Percentage_yield_loss, 2)
        return Percentage_yield_loss
    
    # Function to calculate the yearly earnings/loss
    def Yearlyearnings_loss(self):    
        percentagechange = (self.currentprice - self.purchaseprice) / self.purchaseprice
        numberofdays = (datetime.date.today() - self.purchasedate).days
        returnrate = percentagechange / numberofdays
        annualizedreturn = returnrate * 365
        yearlyearnings_loss = annualizedreturn * 100
        yearlyearnings_loss = round(yearlyearnings_loss, 2)
        return yearlyearnings_loss

    
# InvestorPortfolio to print the performance of stocks for the Investor
class InvestorPortfolio:
    def print_portfolio(self, investor, df, investment_type):
        print(f"\t\t\t {investment_type} ownership for {investor.name}")
        print(f"\t\t\tInvestor Address: {investor.address}")
        print('-' * 80)
        if investment_type == 'Stock':
            df = df[['INVESTOR_ID', 'SYMBOL', 'NO_SHARES', 'Earnings_Loss', 'Yearly_Earning_Loss']]
        elif investment_type == 'Bond':
            df = df[['INVESTOR_ID', 'SYMBOL', 'NO_SHARES', 'Earnings_Loss', 'Yearly_Earning_Loss', 'Coupon', 'Yield']]
        print(df)
        print('\n')
