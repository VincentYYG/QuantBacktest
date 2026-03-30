import pandas as pd


def load_price_data_from_local(tickers, benchmark, data_path="data/combined_close.csv"):
    close = pd.read_csv(data_path, index_col=0, parse_dates=True)

    missing_tickers = [t for t in tickers + [benchmark] if t not in close.columns]
    if missing_tickers:
        raise ValueError(f"The local dataset is missing the following tickers: {missing_tickers}")


    stock_prices = close[tickers].copy().sort_index()
    benchmark_price = close[benchmark].copy().sort_index()

    stock_prices = stock_prices.ffill().dropna(how="all")
    benchmark_price = benchmark_price.ffill().dropna()

    return stock_prices, benchmark_price
