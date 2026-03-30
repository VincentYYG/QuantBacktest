import pandas as pd


def get_rebalance_dates(prices: pd.DataFrame, freq: str = "M") -> pd.DatetimeIndex:
    if freq in ("M", "ME"):
        rebalance_dates = prices.groupby(prices.index.to_period("M")).apply(lambda x: x.index[-1])
    elif freq == "W":
        rebalance_dates = prices.groupby(prices.index.to_period("W")).apply(lambda x: x.index[-1])
    else:
        raise ValueError("rebalance_freq only supports 'M', 'ME', or 'W'.")

    return pd.DatetimeIndex(rebalance_dates)
