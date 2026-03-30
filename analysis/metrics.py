import math
import numpy as np
import pandas as pd


def annualized_return(nav: pd.Series, periods_per_year: int = 252) -> float:
    nav = nav.dropna()
    if len(nav) < 2:
        return np.nan
    total_return = nav.iloc[-1] / nav.iloc[0]
    years = len(nav) / periods_per_year
    if years <= 0:
        return np.nan
    return total_return ** (1 / years) - 1


def annualized_volatility(returns: pd.Series, periods_per_year: int = 252) -> float:
    returns = returns.dropna()
    if len(returns) < 2:
        return np.nan
    return returns.std() * math.sqrt(periods_per_year)


def sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.0, periods_per_year: int = 252) -> float:
    returns = returns.dropna()
    if len(returns) < 2:
        return np.nan
    excess_daily = returns - risk_free_rate / periods_per_year
    vol = excess_daily.std()
    if vol == 0:
        return np.nan
    return excess_daily.mean() / vol * math.sqrt(periods_per_year)


def max_drawdown(drawdown: pd.Series) -> float:
    drawdown = drawdown.dropna()
    if drawdown.empty:
        return np.nan
    return drawdown.min()


def win_rate(returns: pd.Series) -> float:
    returns = returns.dropna()
    if len(returns) == 0:
        return np.nan
    return (returns > 0).mean()


def calmar_ratio(annual_ret: float, max_dd: float) -> float:
    if pd.isna(annual_ret) or pd.isna(max_dd) or max_dd == 0:
        return np.nan
    return annual_ret / abs(max_dd)


def summarize_performance(result: pd.DataFrame) -> pd.DataFrame:
    port_ret = result["portfolio_return"]
    bench_ret = result["benchmark_return"]

    port_nav = result["portfolio_nav"]
    bench_nav = result["benchmark_nav"]

    port_ann_ret = annualized_return(port_nav)
    bench_ann_ret = annualized_return(bench_nav)

    port_ann_vol = annualized_volatility(port_ret)
    bench_ann_vol = annualized_volatility(bench_ret)

    port_sharpe = sharpe_ratio(port_ret)
    bench_sharpe = sharpe_ratio(bench_ret)

    port_mdd = max_drawdown(result["portfolio_drawdown"])
    bench_mdd = max_drawdown(result["benchmark_drawdown"])

    port_calmar = calmar_ratio(port_ann_ret, port_mdd)
    bench_calmar = calmar_ratio(bench_ann_ret, bench_mdd)

    total_turnover = result["turnover"].sum()
    total_cost = result["cost"].sum()

    summary = pd.DataFrame({
        "Strategy": {
            "Total Return": port_nav.iloc[-1] / port_nav.iloc[0] - 1,
            "Annualized Return": port_ann_ret,
            "Annualized Volatility": port_ann_vol,
            "Sharpe Ratio": port_sharpe,
            "Max Drawdown": port_mdd,
            "Calmar Ratio": port_calmar,
            "Win Rate (Daily)": win_rate(port_ret),
            "Total Turnover": total_turnover,
            "Total Cost": total_cost,
            "Final NAV": port_nav.iloc[-1]
        },
        "Benchmark": {
            "Total Return": bench_nav.iloc[-1] / bench_nav.iloc[0] - 1,
            "Annualized Return": bench_ann_ret,
            "Annualized Volatility": bench_ann_vol,
            "Sharpe Ratio": bench_sharpe,
            "Max Drawdown": bench_mdd,
            "Calmar Ratio": bench_calmar,
            "Win Rate (Daily)": win_rate(bench_ret),
            "Total Turnover": np.nan,
            "Total Cost": np.nan,
            "Final NAV": bench_nav.iloc[-1]
        }
    })

    return summary
