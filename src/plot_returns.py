import pandas as pd
import matplotlib.pyplot as plt
import os

RESULTS_FILE = "data/backtest_results.csv"

def plot_backtest():
    if not os.path.exists(RESULTS_FILE):
        print("❌ Backtest results file not found.")
        return

    df = pd.read_csv(RESULTS_FILE)
    df["cumulative_return"] = (1 + df["return_pct"] / 100).cumprod()

    plt.figure(figsize=(10, 6))
    plt.plot(df["cumulative_return"], marker="o", label="Strategy")
    plt.axhline(y=1.0, color='gray', linestyle="--", label="Flat Benchmark")
    plt.title("Cumulative Strategy Return")
    plt.xlabel("Trade Index")
    plt.ylabel("Cumulative Return (x)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("data/backtest_plot.png")
    plt.show()

if __name__ == "__main__":
    plot_backtest()
