from typing import Dict, List, Optional
import os
import pandas as pd
import matplotlib.pyplot as plt


def plot_results(
    result: pd.DataFrame,
    title: str = "Backtest Result",
    output_dir: Optional[str] = None,
    show_plots: bool = True
) -> None:
    title_fontsize = 18
    label_fontsize = 14
    tick_fontsize = 12
    legend_fontsize = 12

    # 1. Equity curve
    fig1 = plt.figure(figsize=(14, 7))
    plt.plot(result.index, result["portfolio_nav"], label="Strategy NAV")
    plt.plot(result.index, result["benchmark_nav"], label="Benchmark NAV")
    plt.title(title, fontsize=title_fontsize)
    plt.xlabel("Date", fontsize=label_fontsize)
    plt.ylabel("Portfolio Value", fontsize=label_fontsize)
    plt.xticks(fontsize=tick_fontsize)
    plt.yticks(fontsize=tick_fontsize)
    plt.legend(fontsize=legend_fontsize)
    plt.grid(True)
    plt.tight_layout()

    if output_dir is not None:
        os.makedirs(output_dir, exist_ok=True)
        fig1.savefig(os.path.join(output_dir, "equity_curve.svg"), format="svg")
        fig1.savefig(os.path.join(output_dir, "equity_curve.png"), format="png", dpi=200)

    # 2. Drawdown curve
    fig2 = plt.figure(figsize=(14, 5))
    plt.plot(result.index, result["portfolio_drawdown"], label="Strategy Drawdown")
    plt.plot(result.index, result["benchmark_drawdown"], label="Benchmark Drawdown")
    plt.title("Drawdown", fontsize=title_fontsize)
    plt.xlabel("Date", fontsize=label_fontsize)
    plt.ylabel("Drawdown", fontsize=label_fontsize)
    plt.xticks(fontsize=tick_fontsize)
    plt.yticks(fontsize=tick_fontsize)
    plt.legend(fontsize=legend_fontsize)
    plt.grid(True)
    plt.tight_layout()

    if output_dir is not None:
        fig2.savefig(os.path.join(output_dir, "drawdown_curve.svg"), format="svg")
        fig2.savefig(os.path.join(output_dir, "drawdown_curve.png"), format="png", dpi=200)

    # 3. Turnover bar chart
    fig3 = plt.figure(figsize=(14, 4))
    plt.bar(result.index, result["turnover"], width=5)
    plt.title("Turnover", fontsize=title_fontsize)
    plt.xlabel("Date", fontsize=label_fontsize)
    plt.ylabel("Turnover", fontsize=label_fontsize)
    plt.xticks(fontsize=tick_fontsize)
    plt.yticks(fontsize=tick_fontsize)
    plt.grid(True)
    plt.tight_layout()

    if output_dir is not None:
        fig3.savefig(os.path.join(output_dir, "turnover_bar.svg"), format="svg")
        fig3.savefig(os.path.join(output_dir, "turnover_bar.png"), format="png", dpi=200)

    if show_plots:
        plt.show()
    else:
        plt.close(fig1)
        plt.close(fig2)
        plt.close(fig3)


def print_latest_selections(selection_log: Dict[pd.Timestamp, List[str]], last_n: int = 10) -> None:
    print("\nRecent rebalance selections:")
    items = list(selection_log.items())[-last_n:]
    for dt, assets in items:
        print(f"{dt.date()} -> {assets if assets else 'No positions'}")
