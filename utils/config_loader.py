from dataclasses import dataclass
from typing import List
import yaml


@dataclass
class BacktestConfig:
    tickers: List[str]
    benchmark: str
    start_date: str
    end_date: str
    initial_capital: float
    rebalance_freq: str
    transaction_cost: float
    min_history: int
    data_path: str
    strategy_name: str


@dataclass
class CrossSectionalMomentumConfig:
    lookback: int
    top_n: int
    positive_momentum_only: bool = True

@dataclass
class MovingAverageCrossoverConfig:
    short_window: int
    long_window: int
    top_n: int
    price_above_long_only: bool = True

## You can add more configs for your strategies.

def load_yaml(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_backtest_config(path: str) -> BacktestConfig:
    data = load_yaml(path)
    return BacktestConfig(**data)


def load_cross_sectional_momentum_config(path: str) -> CrossSectionalMomentumConfig:
    data = load_yaml(path)
    return CrossSectionalMomentumConfig(**data)

def load_moving_average_crossover_config(path: str) -> MovingAverageCrossoverConfig:
    data = load_yaml(path)
    return MovingAverageCrossoverConfig(**data)

## You should add a loading function for each of your strategies.