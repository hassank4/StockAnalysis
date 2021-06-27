
class Portfolio:

    def __init__(self, stock):
        self.stock = stock
        self.owned_stocks = 0
        self.available_balance = 0

    def set_amount(self, amount):
        self.available_balance = amount

    def buy(self, stock_price):
        stocks_buyable = int(self.available_balance / stock_price)
        self.owned_stocks += stocks_buyable
        self.available_balance -= (stocks_buyable * stock_price)
        print(str(stocks_buyable) + " " + self.stock + " shares bought at $" + str(stock_price))

    def sell(self, stock_price):
        self.available_balance += (self.owned_stocks * stock_price)
        print(str(self.owned_stocks) + " " + self.stock + " shares sold at $" + str(stock_price))
        self.owned_stocks = 0

    def get_portfolio(self):
        string_stocks = ""
        print(self.stock + ": " + str(self.owned_stocks) + " shares and $" + str(
                self.available_balance) + " in account")

'''class Portfolio:

    def __init__(self, stock):
        self.stock = stock
        self.owned_stock = {stock: 0.00}
        self.available_stock_amount = {stock: 0.00}

    def set_amount(self, amount):
        self.available_stock_amount[self.stock] = amount

    def buy(self, stock_price):
        amount_of_stocks = int(self.available_stock_amount[self.stock] / stock_price)
        pre_owned = self.owned_stock.get(self.stock)
        self.owned_stock[self.stock] = pre_owned + amount_of_stocks
        self.available_stock_amount[self.stock] = self.available_stock_amount[self.stock] - (amount_of_stocks * stock_price)
        print(str(amount_of_stocks) + " " + self.stock + " shares bought at $" + str(stock_price))

    def sell(self, stock_price):
        pre_owned = self.owned_stock.get(self.stock)
        stock_amount = self.available_stock_amount[self.stock]
        self.owned_stock[self.stock] = 0
        self.available_stock_amount[self.stock] = stock_amount + (pre_owned * stock_price)
        print(str(pre_owned) + " " + self.stock + " shares sold at $" + str(stock_price))

    def get_portfolio(self):
        string_stocks = ""
        for key, value in self.owned_stock.items():
            print(key + ": " + str(self.owned_stock[key]) + " shares and $" + str(self.available_stock_amount[key]) + " in account")
            string_stocks += key + ": " + str(self.owned_stock[key]) + " and $" + str(
                self.available_stock_amount[key]) + "\n"
        return string_stocks
'''
'''
p = Portfolio("DOW")
p.set_amount()
p.buy(15.4)
p.get_portfolio()
p.sell(20.2)
p.get_portfolio()'''