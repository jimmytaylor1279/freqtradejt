from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
import talib.abstract as ta

class CustomStrategy(IStrategy):
    """
    Custom Strategy for Freqtrade, integrating RSI and MACD indicators.
    """

    # Minimal ROI designed for the strategy.
    minimal_roi = {
        "0": 0.05  # 5% ROI
    }

    # Optimal stoploss designed for the strategy
    stoploss = -0.10  # 10% stop-loss

    # Trailing stop
    trailing_stop = True
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.02
    trailing_only_offset_is_reached = False

    # RSI and MACD settings
    rsi_buy = 30  # RSI value below which to buy
    rsi_sell = 70  # RSI value above which to sell

    # Consecutive losses and last trade profit
    consecutive_losses = 0
    last_trade_profit = 0

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Add necessary indicators: RSI and MACD
        """
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        macd = ta.MACD(dataframe)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Define the buy signal based on RSI and MACD.
        """
        dataframe.loc[
            (
                (dataframe['rsi'] < self.rsi_buy) &
                (dataframe['macd'] > dataframe['macdsignal'])
            ),
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Define the sell signal based on RSI and MACD.
        """
        dataframe.loc[
            (
                (dataframe['rsi'] > self.rsi_sell) &
                (dataframe['macd'] < dataframe['macdsignal'])
            ),
            'sell'] = 1
        return dataframe

    def custom_stake_amount(self, pair: str, current_time, current_rate, current_balance, trade, **kwargs) -> float:
        """
        Custom stake amount calculation based on the outcome of the last trade.
        """
        if self.consecutive_losses >= 3 or self.last_trade_profit > 0:
            stake_amount = current_balance * 0.05  # 5% of current balance
            self.consecutive_losses = 0  # Reset consecutive losses
        else:
            stake_amount = abs(self.last_trade_profit) * 2  # Double the lost amount

        return stake_amount

    def on_trade_closed(self, pair: str, trade) -> None:
        """
        Executed when a trade is closed. Used to update strategy parameters.
        """
        if trade.profit_percent > 0:
            self.last_trade_profit = trade.stake_amount * trade.profit_percent
            self.consecutive_losses = 0
        else:
            self.last_trade_profit = -trade.stake_amount * abs(trade.profit_percent)
            self.consecutive_losses += 1
