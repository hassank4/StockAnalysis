import json
from alpha_vantage.timeseries import TimeSeries
import datetime
import time
from Portfolio import Portfolio
from StockCandlesAnalysis import StockCandlesAnalysis


class StockAnalyzer:

    def __init__(self, stock):
        self.stock = stock
        self.time_series = TimeSeries('R6XCN2331MT9VVZM')
        self.stock_candles = []
        #self.highest_price = []
        self.account = Portfolio(self.stock)
        #self.minimum_stock_price = 0

    def get_stock_candle_info(self, stock_candle):
        open_price, close_price, high_price, low_price = 0, 0, 0, 0
        stock_info = str(stock_candle).split(", ")
        #print(stock_info)
        for i in range(len(stock_info)):
            stock_info[i] = stock_info[i].replace("'", "")
            if i == 0:
                open_cost = stock_info[i].split(": ")
                open_price = float(open_cost[1])
                #print(open_price)
            elif i == 1:
                high = stock_info[i].split(": ")
                high_price = float(high[1])
            elif i == 2:
                low = stock_info[i].split(": ")
                low_price = float(low[1])
            elif i == 3:
                close = stock_info[i].split(": ")
                close_price = float(close[1])
        return [open_price, close_price, high_price, low_price]

    def stock_json(self, stock_candle, stock_trade, trade_method):
        json_string = {
            "Time": stock_candle[0],
            "Trading": stock_trade,
            "Method": trade_method,
            "Close": stock_candle[1][1],
            "Open": stock_candle[1][0],
            "High": stock_candle[1][2],
            "Low": stock_candle[1][3]
        }
        return json_string

    def write_json(self, data, filename='trading.json'):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def create_json(self,filename='trading.json'):
        with open(filename, 'w') as f:
            data = {
                "Transcript": []
            }
            json.dump(data, f, indent=4)

    def get_latest_date(self, first_stock_call):
        return str(first_stock_call)[2:12]

    def selling_stock(self, candle_trend, transcript):
        self.account.sell(self.final_price())
        json_string = self.stock_json(self.stock_candles[0], candle_trend, "Should Sell")
        transcript.append(json_string)

    def buying_stock(self, candle_trend, transcript):
        self.account.buy(self.final_price())
        json_string = self.stock_json(self.stock_candles[0], candle_trend, "Should Buy")
        transcript.append(json_string)

    def amount_of_stock_intervals(self, stock_intervals):
        stock_interval_amount = 0
        for stock_interval in range(len(stock_intervals)):
            if self.get_latest_date(stock_intervals[0]) in stock_intervals[stock_interval]:
                stock_interval_amount += 1
        return stock_interval_amount

    def start_and_end_of_intervals(self, stock_intervals):
        start_found = False
        end_found = False
        stock_interval_position = 0
        start_interval = 0
        end_interval = 0
        stock_interval_amount = self.amount_of_stock_intervals(stock_intervals)

        while end_found is False and stock_interval_position <= stock_interval_amount:
            if self.get_latest_date(stock_intervals[0]) in stock_intervals[stock_interval_position]:
                if int(stock_intervals[stock_interval_position][12:14]) <= 15:
                    end_found = True
                    end_interval = stock_interval_position
            stock_interval_position += 1

        while start_found is False and stock_interval_position <= stock_interval_amount and end_found is True:
            if self.get_latest_date(stock_intervals[0]) in stock_intervals[stock_interval_position]:
                if int(stock_intervals[stock_interval_position][12:14]) <= 8:
                    start_found = True
                    start_interval = stock_interval_position
            stock_interval_position += 1

        return start_interval, end_interval

    def get_time(self):
        current_dt = datetime.datetime.now()
        date = str(current_dt).split(" ")
        final_time = date[1].rsplit(":", 1)
        return final_time[0]

    def final_price(self):
        return self.stock_candles[0][1][1]

    def check_stock(self):
        try:
            stock_data, stock_meta = TimeSeries('R6XCN2331MT9VVZM').get_intraday(symbol=self.stock, interval='1min',
                                                                                 outputsize='compact')
            return True
        except:
            return False

    def realtime_candle_trends(self):
        stock_analysis = StockCandlesAnalysis()
        self.create_json()
        with open('trading.json') as json_file:
            data = json.load(json_file)
            transcript = data['Transcript']
            current_time = self.get_time().split(":")
            bought_price = 0
            while (9 <= int(current_time[0]) <= 15):

                stock_data, stock_meta = self.time_series.get_intraday(symbol=self.stock, interval='1min', outputsize='compact')
                stock_intervals = str(stock_data).split("}, ")
                stock_intervals[0] = stock_intervals[0][1:]
                #print(stock_intervals)
                #print(stock_interval_amount)

                trading = False

                stock_call = str(stock_intervals[0]).split(': ', 1)
                info = self.get_stock_candle_info(stock_call[1])
                stock_date = stock_call[0].replace("{", "")
                self.stock_candles.insert(0, [stock_date, info])

                if len(self.stock_candles) > 5:
                    if trading:
                        if stock_analysis.bearish_engulfing(self.stock_candles) and bought_price < \
                                self.stock_candles[0][1][1]:
                            self.selling_stock("Bearish Engulfing", transcript)
                            trading = False
                        elif stock_analysis.bearish_evening(self.stock_candles) and bought_price < \
                                self.stock_candles[0][1][1]:
                            self.selling_stock("Bearish Evening", transcript)
                            trading = False
                        elif stock_analysis.bearish_harami(self.stock_candles) and bought_price < \
                                self.stock_candles[0][1][1]:
                            self.selling_stock("Bearish Harami", transcript)
                            trading = False
                        elif stock_analysis.bearish_rising_three(self.stock_candles) and bought_price < \
                                self.stock_candles[0][1][1]:
                            self.selling_stock("Bearish Rising Three", transcript)
                            trading = False
                    else:
                        if stock_analysis.bullish_engulfing(self.stock_candles):
                            self.buying_stock("Bullish Engulfing", transcript)
                            bought_price = self.final_price()
                            trading = True
                        elif stock_analysis.bullish_rising_three(self.stock_candles):
                            self.buying_stock("Bullish Rising Three", transcript)
                            bought_price = self.final_price()
                            trading = True
                        elif stock_analysis.bullish_harami(self.stock_candles):
                            self.buying_stock("Bullish Harami", transcript)
                            bought_price = self.final_price()
                            trading = True
                time.sleep(60)
                current_time = self.get_time().split(":")

            if trading:
                self.account.sell(self.stock_candles[1][1][1])
                json_string = self.stock_json(self.stock_candles[1], "Final Sell", "Should Sell")
                transcript.append(json_string)
            self.account.get_portfolio()
            self.write_json(data)

    def day_candle_trends(self):
        stock_analysis = StockCandlesAnalysis()
        self.create_json()
        with open('trading.json') as json_file:
            data = json.load(json_file)
            transcript = data['Transcript']
            stock_data, stock_meta = self.time_series.get_intraday(symbol=self.stock, interval='1min', outputsize='full')
            stock_intervals = str(stock_data).split("}, ")
            stock_intervals[0] = stock_intervals[0][1:]
            #date = self.get_latest_date(stock_intervals[0])
            #print(date)
            #print(stock_intervals)
            #stock_interval_amount = self.amount_of_stock_intervals(stock_intervals)
            #print(stock_interval_amount)
            bought_price = 0
            trading = False
            start_interval, end_interval = self.start_and_end_of_intervals(stock_intervals)

            while start_interval >= end_interval:

                stock_call = str(stock_intervals[start_interval]).split(': ', 1)
                info = self.get_stock_candle_info(stock_call[1])
                stock_date = stock_call[0].replace("{", "")
                self.stock_candles.insert(0, [stock_date, info])

                if len(self.stock_candles) > 5:
                    if trading:
                        if stock_analysis.bearish_engulfing(self.stock_candles) and bought_price < self.stock_candles[0][1][1]:
                            self.selling_stock("Bearish Engulfing", transcript)
                            trading = False
                        elif stock_analysis.bearish_evening(self.stock_candles) and bought_price < self.stock_candles[0][1][1]:
                            self.selling_stock("Bearish Evening", transcript)
                            trading = False
                        elif stock_analysis.bearish_harami(self.stock_candles) and bought_price < self.stock_candles[0][1][1]:
                            self.selling_stock("Bearish Harami", transcript)
                            trading = False
                        elif stock_analysis.bearish_rising_three(self.stock_candles) and bought_price < self.stock_candles[0][1][1]:
                            self.selling_stock("Bearish Rising Three", transcript)
                            trading = False
                    else:
                        if stock_analysis.bullish_engulfing(self.stock_candles):
                            self.buying_stock("Bullish Engulfing", transcript)
                            bought_price = self.final_price()
                            trading = True
                        elif stock_analysis.bullish_rising_three(self.stock_candles):
                            self.buying_stock("Bullish Rising Three", transcript)
                            bought_price = self.final_price()
                            trading = True
                        elif stock_analysis.bullish_harami(self.stock_candles):
                            self.buying_stock("Bullish Harami", transcript)
                            bought_price = self.final_price()
                            trading = True

                start_interval -= 1

            if trading:
                self.account.sell(self.stock_candles[1][1][1])
                json_string = self.stock_json(self.stock_candles[1], "Final Sell", "Should Sell")
                transcript.append(json_string)
            self.account.get_portfolio()
            self.write_json(data)


chosen_stock = input("Enter a stock:").capitalize()
stock_app = StockAnalyzer(chosen_stock)

while stock_app.check_stock() is False:
    chosen_stock = input("Enter a stock:")
    stock_app = StockAnalyzer(chosen_stock)

current_time = stock_app.get_time().split(":")
#print(current_time[0])

valid_balance = False
balance = ""
while valid_balance is False:
    balance = input("Enter amount you want to use for stocks:")
    try:
        stock_app.account.set_amount(float(balance))
        valid_balance = True
    except:
        print("Invalid balance.")

if 9 <= int(current_time[0]) <= 15:
    print("Real Time Trading")
    stock_app.realtime_candle_trends()

else:
    print("Whole Day Trading")
    stock_app.account.set_amount(float(balance))
    stock_app.day_candle_trends()

print("\nA transcript of when the program locates the best places to buy and sell the stock is located in 'trading.json'")



