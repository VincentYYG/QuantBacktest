import pandas as pd


class BaseStrategy:
    def __init__(self, strategy_name: str):
        self.strategy_name = strategy_name

    def prepare(self, prices: pd.DataFrame) -> None:
        pass

    def generate_target_weights(
        self,
        dt: pd.Timestamp,
        prices: pd.DataFrame
    ) -> pd.Series:
        raise NotImplementedError("Strategy must implement the generate_target_weights method.")

