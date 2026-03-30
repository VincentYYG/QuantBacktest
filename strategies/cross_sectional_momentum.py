from typing import List, Optional
import pandas as pd

from core.strategy_base import BaseStrategy
from utils.config_loader import CrossSectionalMomentumConfig



class CrossSectionalMomentumStrategy(BaseStrategy):
    def __init__(self, tickers: List[str], config: CrossSectionalMomentumConfig, min_history: int):
        super().__init__(strategy_name="cross_sectional_momentum")
        self.tickers = tickers
        self.config = config
        self.min_history = min_history
        self.momentum: Optional[pd.DataFrame] = None

    def prepare(self, prices: pd.DataFrame) -> None:
        self.momentum = prices / prices.shift(self.config.lookback) - 1.0

    def generate_target_weights(
        self,
        dt: pd.Timestamp,
        prices: pd.DataFrame
    ) -> pd.Series:
#        if self.momentum is None:
#            raise ValueError("Strategy has not been prepared.")

        target_weights = pd.Series(0.0, index=prices.columns)

        sufficient_history = prices.loc[:dt].count() >= self.min_history
        eligible_assets = sufficient_history[sufficient_history].index.tolist()

        if not eligible_assets:
            return target_weights

        momentum_row = self.momentum.loc[dt, eligible_assets].dropna()
        price_row = prices.loc[dt, eligible_assets].dropna()

        if momentum_row.empty or price_row.empty:
            return target_weights

        momentum_row = momentum_row[momentum_row.index.isin(price_row.index)]

        if momentum_row.empty:
            return target_weights

        if self.config.positive_momentum_only:
            momentum_row = momentum_row[momentum_row > 0]

        if momentum_row.empty:
            return target_weights

        selected_assets = (
            momentum_row.sort_values(ascending=False)
            .head(self.config.top_n)
            .index
            .tolist()
        )

        if not selected_assets:
            return target_weights

        equal_weight = 1.0 / len(selected_assets)
        target_weights.loc[selected_assets] = equal_weight

        return target_weights
