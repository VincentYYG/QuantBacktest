from typing import List, Optional
import pandas as pd

from core.strategy_base import BaseStrategy
from utils.config_loader import MovingAverageCrossoverConfig


class MovingAverageCrossoverStrategy(BaseStrategy):
    def __init__(self, tickers: List[str], config: MovingAverageCrossoverConfig, min_history: int):
        super().__init__(strategy_name="moving_average_crossover")
        self.tickers = tickers
        self.config = config
        self.min_history = min_history
        self.short_ma: Optional[pd.DataFrame] = None
        self.long_ma: Optional[pd.DataFrame] = None

    def prepare(self, prices: pd.DataFrame) -> None:
        self.short_ma = prices.rolling(window=self.config.short_window, min_periods=1).mean()
        self.long_ma = prices.rolling(window=self.config.long_window, min_periods=1).mean()

    def generate_target_weights(
        self,
        dt: pd.Timestamp,
        prices: pd.DataFrame
    ) -> pd.Series:
        if self.short_ma is None or self.long_ma is None:
            raise ValueError("Strategy has not been prepared. Please call prepare(prices) first.")

        target_weights = pd.Series(0.0, index=prices.columns)

        sufficient_history = prices.loc[:dt].count() >= self.min_history
        eligible_assets = sufficient_history[sufficient_history].index.tolist()

        if not eligible_assets:
            return target_weights

        price_row = prices.loc[dt, eligible_assets].dropna()
        short_ma_row = self.short_ma.loc[dt, eligible_assets].dropna()
        long_ma_row = self.long_ma.loc[dt, eligible_assets].dropna()

        valid_assets = list(
            set(price_row.index).intersection(short_ma_row.index).intersection(long_ma_row.index)
        )

        if not valid_assets:
            return target_weights

        signal_assets = []

        for asset in valid_assets:
            short_value = short_ma_row[asset]
            long_value = long_ma_row[asset]
            price_value = price_row[asset]

            # Core crossover condition
            if short_value <= long_value:
                continue

            # Optional trend filter
            if self.config.price_above_long_only and price_value <= long_value:
                continue

            signal_assets.append(asset)

        if not signal_assets:
            return target_weights

        # Rank by crossover strength
        strength = (
            (short_ma_row[signal_assets] / long_ma_row[signal_assets]) - 1.0
        ).sort_values(ascending=False)

        selected_assets = strength.head(self.config.top_n).index.tolist()

        if not selected_assets:
            return target_weights

        equal_weight = 1.0 / len(selected_assets)
        target_weights.loc[selected_assets] = equal_weight

        return target_weights
