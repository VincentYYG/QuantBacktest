import os
import shutil
from datetime import datetime
import pandas as pd

from utils.config_loader import load_backtest_config
from strategies.factory import create_strategy
from data_loader.price_loader import load_price_data_from_local
from core.backtester import Backtester
from analysis.metrics import summarize_performance
from analysis.plotting import plot_results, print_latest_selections


def main():
    backtest_config_path = "config/backtest.yaml"
    backtest_config = load_backtest_config(backtest_config_path)

    print("Loading price data...")
    prices, benchmark = load_price_data_from_local(
        tickers=backtest_config.tickers,
        benchmark=backtest_config.benchmark,
        data_path=backtest_config.data_path
    )

    common_index = prices.index.intersection(benchmark.index)
    prices = prices.loc[common_index].copy()
    benchmark = benchmark.loc[common_index].copy()

    print(f"Price data range: {prices.index.min().date()} to {prices.index.max().date()}")
    print(f"Number of assets: {prices.shape[1]}")
    print(f"Number of trading days: {len(prices)}")

    strategy, strategy_config_path = create_strategy(
        strategy_name=backtest_config.strategy_name,
        tickers=backtest_config.tickers,
        min_history=backtest_config.min_history
    )

    backtester = Backtester(
        prices=prices,
        benchmark=benchmark,
        strategy=strategy,
        config=backtest_config
    )

    result = backtester.run()
    summary = summarize_performance(result)

    pd.set_option("display.float_format", lambda x: f"{x:,.4f}")
    print("\n========== Backtest Performance ==========")
    print(summary)

    print_latest_selections(backtester.selection_log, last_n=6) # print the last 6 times of selection.

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    strategy_output_dir = os.path.join("output", backtest_config.strategy_name, timestamp)
    config_output_dir = os.path.join(strategy_output_dir, "configs")

    os.makedirs(strategy_output_dir, exist_ok=True)
    os.makedirs(config_output_dir, exist_ok=True)

    result_path = os.path.join(strategy_output_dir, "backtest_result.csv")
    summary_path = os.path.join(strategy_output_dir, "backtest_summary.csv")

    result.to_csv(result_path, encoding="utf-8-sig")
    summary.to_csv(summary_path, encoding="utf-8-sig")

    shutil.copy2(backtest_config_path, os.path.join(config_output_dir, "backtest.yaml"))
    shutil.copy2(
        strategy_config_path,
        os.path.join(config_output_dir, os.path.basename(strategy_config_path))
    )

    print("\nResults exported:")
    print(f"- {result_path}")
    print(f"- {summary_path}")

    plot_results(
        result=result,
        title=f"{backtest_config.strategy_name} Backtest ({backtest_config.start_date} to {backtest_config.end_date})",
        output_dir=strategy_output_dir,
        show_plots=True
    )


if __name__ == "__main__":
    main()
