
class StockCandlesAnalysis:

    def candle_sizes(self, stock_candles):
        first_candle = stock_candles[0][1][1] - stock_candles[0][1][0]
        second_candle = stock_candles[1][1][1] - stock_candles[1][1][0]
        third_candle = stock_candles[2][1][1] - stock_candles[2][1][0]
        fourth_candle = stock_candles[3][1][1] - stock_candles[3][1][0]
        fifth_candle = stock_candles[4][1][1] - stock_candles[4][1][0]
        return first_candle, second_candle, third_candle, fourth_candle, fifth_candle

    def bearish_engulfing(self, stock_candles):
        first_candle, second_candle, third_candle, forth_candle, fifth_candle = self.candle_sizes(stock_candles)
        if first_candle < 0 and second_candle > 0 and third_candle > 0 and forth_candle > 0 and abs(
                first_candle) > second_candle:
            if stock_candles[1][1][0] > stock_candles[0][1][1] and stock_candles[1][1][1] < stock_candles[0][1][0]:
                print("Bearish Engulfing - Closing Price: $" + str(stock_candles[0][1][1]))
                return True
        return False

    def bullish_engulfing(self, stock_candles):
        first_candle, second_candle, third_candle, forth_candle, fifth_candle = self.candle_sizes(stock_candles)
        if first_candle > 0 and second_candle < 0 and third_candle < 0 and forth_candle < 0 and first_candle > abs(
                second_candle):
            if stock_candles[1][1][0] < stock_candles[0][1][1] and stock_candles[1][1][1] > stock_candles[0][1][0]:
                print("Bullish Engulfing - Closing Price: $" + str(stock_candles[0][1][1]))
                return True
        return False

    def bearish_evening(self, stock_candles):
        first_candle, second_candle, third_candle, forth_candle, fifth_candle = self.candle_sizes(stock_candles)
        if first_candle < 0 and second_candle < 0 and third_candle > 0 and forth_candle > 0 and abs(first_candle) > abs(
                second_candle):
            if stock_candles[0][1][0] < stock_candles[1][1][1] and (
                    stock_candles[2][1][0] <= stock_candles[0][1][1] < stock_candles[2][1][1]):
                return True
        elif first_candle < 0 and second_candle > 0 and third_candle > 0 and forth_candle > 0 and abs(
                first_candle) > second_candle:
            if stock_candles[0][1][0] < stock_candles[1][1][0] and (
                    stock_candles[2][1][0] <= stock_candles[0][1][1] < stock_candles[2][1][1]):
                print("Bearish Evening - Closing Price: $" + str(stock_candles[0][1][1]))
                return True
        return False

    def bearish_harami(self, stock_candles):
        first_candle, second_candle, third_candle, forth_candle, fifth_candle = self.candle_sizes(stock_candles)
        if first_candle > 0 and second_candle > 0 and third_candle > 0 and forth_candle <= 0:
            if stock_candles[0][1][0] < stock_candles[1][1][1]:
                print("Bearish Harami - Closing Price: $" + str(stock_candles[0][1][1]))
                return True
        return False

    def bullish_harami(self, stock_candles):
        first_candle, second_candle, third_candle, forth_candle, fifth_candle = self.candle_sizes(stock_candles)
        if first_candle < 0 and second_candle < 0 and third_candle < 0 and forth_candle >= 0:
            if stock_candles[0][1][0] > stock_candles[1][1][1]:
                print("Bullish Harami - Closing Price: $" + str(stock_candles[0][1][1]))
                return True
        return False

    def bullish_rising_three(self, stock_candles):
        first_candle, second_candle, third_candle, forth_candle, fifth_candle = self.candle_sizes(stock_candles)
        if first_candle > 0 and second_candle < 0 and third_candle < 0 and forth_candle < 0 and fifth_candle > 0:
            if stock_candles[0][1][0] > stock_candles[4][1][0] and stock_candles[0][1][1] > stock_candles[4][1][1]:
                if stock_candles[2][1][0] < stock_candles[4][1][1] and stock_candles[2][1][1] > \
                        stock_candles[4][1][0]:
                    if stock_candles[1][1][0] < stock_candles[4][1][1] and stock_candles[1][1][1] > \
                            stock_candles[4][1][0]:
                        print("Bullish Rising Three - Closing Price: $" + str(stock_candles[0][1][1]))
                        return True
        return False

    def bearish_rising_three(self, stock_candles):
        first_candle, second_candle, third_candle, forth_candle, fifth_candle = self.candle_sizes(stock_candles)
        if first_candle < 0 and second_candle > 0 and third_candle > 0 and forth_candle > 0 and fifth_candle < 0:
            if stock_candles[0][1][0] < stock_candles[4][1][0] and stock_candles[0][1][1] < stock_candles[4][1][1]:
                if stock_candles[2][1][0] > stock_candles[4][1][1] and stock_candles[2][1][1] < \
                        stock_candles[4][1][0]:
                    if stock_candles[1][1][0] > stock_candles[4][1][1] and stock_candles[1][1][1] < \
                            stock_candles[4][1][0]:
                        print("Bearish Rising Three - Closing Price: $" + str(stock_candles[0][1][1]))
                        return True
        return False
