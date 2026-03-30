from typing import Dict, List

import pandas as pd

from core.calendar_utils import get_rebalance_dates
from core.strategy_base import BaseStrategy
from utils.config_loader import BacktestConfig


class Backtester:
    def __init__(
        self,
        prices: pd.DataFrame,
        benchmark: pd.Series,
        strategy: BaseStrategy,
        config: BacktestConfig
    ):
        self.prices = prices.copy()
        self.benchmark = benchmark.copy()
        self.strategy = strategy
        self.config = config

        self.daily_returns = self.prices.pct_change().fillna(0.0)
        self.benchmark_returns = self.benchmark.pct_change().fillna(0.0)
        self.rebalance_dates = get_rebalance_dates(self.prices, self.config.rebalance_freq)

        self.weights = pd.DataFrame(0.0, index=self.prices.index, columns=self.prices.columns)
        self.portfolio_returns = pd.Series(0.0, index=self.prices.index)
        self.turnover = pd.Series(0.0, index=self.prices.index)
        self.costs = pd.Series(0.0, index=self.prices.index)
        self.selection_log: Dict[pd.Timestamp, List[str]] = {}
        self.result = pd.DataFrame(index=self.prices.index)

        self.strategy.prepare(self.prices)

    def run(self) -> pd.DataFrame:
        current_weights = pd.Series(0.0, index=self.prices.columns)

        for dt in self.prices.index:
            if dt in self.rebalance_dates:
                new_weights = self.strategy.generate_target_weights(dt=dt, prices=self.prices)
                new_weights = new_weights.reindex(self.prices.columns).fillna(0.0)

                weight_sum = new_weights.sum()
                if weight_sum > 1.000001:
                    raise ValueError(f"{dt.date()} 目标权重之和超过 1: {weight_sum:.6f}")

                selected_assets = new_weights[new_weights > 0].index.tolist()
                self.selection_log[dt] = selected_assets

                daily_turnover = (new_weights - current_weights).abs().sum()
                trading_cost = daily_turnover * self.config.transaction_cost

                self.turnover.loc[dt] = daily_turnover
                self.costs.loc[dt] = trading_cost

                current_weights = new_weights.copy()

            self.weights.loc[dt] = current_weights

        gross_returns = (self.weights.shift(1).fillna(0.0) * self.daily_returns).sum(axis=1)
        net_returns = gross_returns - self.costs
        self.portfolio_returns = net_returns.fillna(0.0)

        self.result["portfolio_return"] = self.portfolio_returns
        self.result["portfolio_nav"] = (1.0 + self.result["portfolio_return"]).cumprod() * self.config.initial_capital

        self.result["benchmark_return"] = self.benchmark_returns.reindex(self.result.index).fillna(0.0)
        self.result["benchmark_nav"] = (1.0 + self.result["benchmark_return"]).cumprod() * self.config.initial_capital

        self.result["turnover"] = self.turnover
        self.result["cost"] = self.costs

        self.result["portfolio_drawdown"] = self.calculate_drawdown(self.result["portfolio_nav"])
        self.result["benchmark_drawdown"] = self.calculate_drawdown(self.result["benchmark_nav"])

        return self.result

    @staticmethod
    def calculate_drawdown(nav: pd.Series) -> pd.Series:
        rolling_max = nav.cummax()
        drawdown = nav / rolling_max - 1.0
        return drawdown
