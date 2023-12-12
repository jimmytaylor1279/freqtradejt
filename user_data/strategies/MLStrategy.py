from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
from freqtrade.persistence import Trade
from freqtrade.wallets import Wallets
from model import predict_market

# Import your custom modules
from model import predict_market
from preprocessing import prepare_data

class MLStrategy(IStrategy):
    """
    Machine Learning based Trading Strategy with dynamic stake amount.
    """

    # Define the stoploss for the strategy
    stoploss = -0.10  # Adjust this value as per your risk preference

    # Define minimal ROI for the strategy
    minimal_roi = {
        "0": 0.05  # Adjust this value as per your strategy
    }

    # Define any other strategy parameters here
    # ...

    def __init__(self, config: dict):
        super().__init__(config)
        self.last_trade_profit = 0
        self.consecutive_losses = 0

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Preprocess the data
        dataframe = prepare_data(dataframe)
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # Call the model prediction function for buy
                predict_market(dataframe, 'buy')
            ),
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # Call the model prediction function for sell
                predict_market(dataframe, 'sell')
            ),
            'sell'] = 1
        return dataframe

    def stake_amount(self, pair: str, **kwargs) -> float:
        balance = self.wallets.get_free_balance(currency=self.config['stake_currency'])
        base_stake = balance * 0.05  # 5% of account balance

        if self.last_trade_profit > 0 or self.consecutive_losses >= 3:
            self.consecutive_losses = 0
            return base_stake
        else:
            loss_stake = base_stake * (2 ** self.consecutive_losses)
            self.consecutive_losses += 1
            return min(loss_stake, balance)

    def check_sell(self, pair: str, trade: Trade, order_type: str, amount: float, rate: float, time_in_force: str, sell_reason: str, **kwargs) -> bool:
        # Update trade outcome
        if trade and trade.close_profit:
            self.last_trade_profit = trade.close_profit
        else:
            self.last_trade_profit = 0
  
    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        buy_signals = predict_market(dataframe, 'buy')
        dataframe.loc[buy_signals, 'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        sell_signals = predict_market(dataframe, 'sell')
        dataframe.loc[sell_signals, 'sell'] = 1
        return dataframe

# Add any additional helper functions or classes here if needed
