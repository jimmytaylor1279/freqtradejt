from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame

class CustomStrategy(IStrategy):
    """
    Custom Strategy for Freqtrade.
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

    # Consecutive losses and last trade profit
    consecutive_losses = 0
    last_trade_profit = 0

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Add any indicators here. This method will be called once per run.
        """
        # Example: Add Simple Moving Average (SMA) indicator
        dataframe['sma'] = dataframe['close'].rolling(window=7).mean()
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on the indicators, define your buy strategy.
        """
        dataframe.loc[
            (
                # Example condition: Buy when the close is greater than SMA
                (dataframe['close'] > dataframe['sma'])
            ),
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on the indicators, define your sell strategy.
        """
        dataframe.loc[
            (
                # Example condition: Sell when the close is less than SMA
                (dataframe['close'] < dataframe['sma'])
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
