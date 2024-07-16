#Task no.2  Stock portfolio Tracker

import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import time

API_KEY = 'qsKcv5_HmOK7OeD4_SZPDT3sWAqxsQe9'

class StockPortfolio:

    def __init__(self):                                           #Intership CodeAlpha Task no.2

        self.stocks = {}

        self.history = {}


    def add_stock(self, ticker, quantity):

        if ticker in self.stocks:

            self.stocks[ticker] += quantity

        else:

            self.stocks[ticker] = quantity

        print(f"Added {quantity} of {ticker} to the portfolio.")


    def remove_stock(self, ticker, quantity):

        if ticker in self.stocks and self.stocks[ticker] >= quantity:

            self.stocks[ticker] -= quantity

            if self.stocks[ticker] == 0:

                del self.stocks[ticker]

            print(f"Removed {quantity} of {ticker} from the portfolio.")

        else:

            print(f"Cannot remove {quantity} of {ticker}. Not enough stock in the portfolio.")



    def get_portfolio(self):

        return self.stocks



    def fetch_stock_price(self, ticker):

        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=1min&apikey={API_KEY}'

        response = requests.get(url)

        data = response.json()

        try:

            latest_close = list(data['Time Series (1min)'].values())[0]['4. close']

            return float(latest_close)

        except KeyError:

            print(f"Could not fetch data for {ticker}. Please check the ticker symbol and try again.")

            return None



    def calculate_portfolio_value(self):

        total_value = 0

        for ticker, quantity in self.stocks.items():

            price = self.fetch_stock_price(ticker)

            if price:

                total_value += price * quantity

        return total_value



    def track_performance(self):

        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        for ticker, _ in self.stocks.items():

            if ticker not in self.history:

                self.history[ticker] = []

            price = self.fetch_stock_price(ticker)

            if price:

                self.history[ticker].append((date, price))



    def plot_performance(self):

        if not self.history:

            print("No performance data to plot. Please track performance first.")

            return



        plt.figure(figsize=(10, 6))

        for ticker, data in self.history.items():

            dates = [datetime.strptime(record[0], '%Y-%m-%d %H:%M:%S') for record in data]

            values = [record[1] for record in data]

            plt.plot(dates, values, marker='o', label=ticker)



        plt.xlabel('Date')

        plt.ylabel('Stock Price')

        plt.title('Stock Performance Over Time')

        plt.legend()

        plt.grid(True)

        plt.tight_layout()

        plt.show()



portfolio = StockPortfolio()



def main():

    while True:

        print("\n1. Add Stock")

        print("2. Remove Stock")

        print("3. View Portfolio")

        print("4. View Portfolio Value")

        print("5. Track and Plot Performance")

        print("6. Exit")



        choice = input("Enter your choice: ")



        if choice == '1':

            ticker = input("Enter the stock ticker: ").upper()

            quantity = int(input("Enter the quantity: "))

            portfolio.add_stock(ticker, quantity)

        elif choice == '2':

            ticker = input("Enter the stock ticker: ").upper()

            quantity = int(input("Enter the quantity: "))

            portfolio.remove_stock(ticker, quantity)

        elif choice == '3':

            print("Current Portfolio:", portfolio.get_portfolio())

        elif choice == '4':

            total_value = portfolio.calculate_portfolio_value()

            print(f"Total Portfolio Value: ${total_value:.2f}")

        elif choice == '5':

            portfolio.track_performance()

            portfolio.plot_performance()

        elif choice == '6':

            break

        else:

            print("Invalid choice. Please try again.")



if __name__ == "__main__":

    main()

