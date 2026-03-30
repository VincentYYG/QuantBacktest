import os
import pandas as pd
import yfinance as yf

TICKERS = [
    # Information Technology
    "AAPL", "MSFT", "NVDA", "AVGO", "AMD",
    "CRM", "ORCL", "ADBE", "CSCO", "INTC",
    # Communication Services
    "GOOG", "META", "NFLX", "DIS", "TMUS",
    # Consumer Discretionary
    "AMZN", "TSLA", "HD", "MCD", "NKE",
    # Consumer Staples
    "PG", "KO", "PEP", "WMT", "COST",
    # Health Care
    "JNJ", "LLY", "PFE", "MRK", "ABBV",
    # Financials
    "JPM", "BAC", "WFC", "GS", "MS",
    # Industrials
    "CAT", "HON", "UPS", "UNP", "GE",
    # Energy
    "XOM", "CVX", "COP", "SLB", "EOG",
    # Utilities
    "NEE", "DUK", "SO",
    # Materials
    "LIN", "APD", "SHW",
    # Real Estate
    "PLD", "AMT",
    # Benchmark
    "SPY"
]

START_DATE = "2016-01-01"
END_DATE = "2025-01-01"

DATA_DIR = "data"
RAW_DIR = os.path.join(DATA_DIR, "raw")

def ensure_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


def download_and_save():
    ensure_dir(DATA_DIR)
    ensure_dir(RAW_DIR)

    print("Downloading data...")
    df = yf.download(
        TICKERS,
        start=START_DATE,
        end=END_DATE,
        auto_adjust=True,
        progress=False
    )

    if df.empty:
        raise ValueError("Downloaded data is empty. Please check network connection or ticker symbols.")

    close = df["Close"].copy()

    # Save individual ticker files
    for ticker in close.columns:
        ticker_df = pd.DataFrame({
            "Date": close.index,
            "Close": close[ticker].values
        })
        file_path = os.path.join(RAW_DIR, f"{ticker}.csv")
        ticker_df.to_csv(file_path, index=False, encoding="utf-8-sig")
        print(f"已保存: {file_path}")

    # Save combined wide-format file
    combined = close.copy()
    combined.to_csv(os.path.join(DATA_DIR, "combined_close.csv"), encoding="utf-8-sig")
    print("已保存合并数据: data/combined_close.csv")


if __name__ == "__main__":
    download_and_save()
