"""Generate the T08 forecast comparison from read-only course CSV files.

Intended final location:
IS6400_Business_Data_Analytics/notes/figures/time-series/

At that location, the default course root is discovered from the script path.
For scratch verification, pass --course-root and --output-dir explicitly.
"""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.exponential_smoothing.ets import ETSModel


def parse_args():
    script_path = Path(__file__).resolve()
    default_root = script_path.parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument("--course-root", type=Path, default=default_root)
    parser.add_argument("--output-dir", type=Path, default=script_path.parent)
    return parser.parse_args()


def forecast(series, steps, **kwargs):
    fitted = ETSModel(series, **kwargs).fit(disp=False)
    return np.asarray(fitted.forecast(steps), dtype=float)


def main():
    args = parse_args()
    course_root = args.course_root.resolve()
    source_dir = course_root / "course_files_export"
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    shampoo_path = source_dir / "shampoo_sales.csv"
    cvd_path = source_dir / "CVD.csv"
    if not shampoo_path.is_file() or not cvd_path.is_file():
        raise FileNotFoundError(
            f"Expected read-only source files under {source_dir}: "
            "shampoo_sales.csv and CVD.csv"
        )

    shampoo = pd.read_csv(shampoo_path)
    shampoo_train = shampoo.iloc[:-5].copy()
    shampoo_test = shampoo.iloc[-5:].copy()
    shampoo_ses = forecast(shampoo_train["Sales"], len(shampoo_test))
    shampoo_holt = forecast(shampoo_train["Sales"], len(shampoo_test), trend="add")
    shampoo_hw = forecast(
        shampoo_train["Sales"], len(shampoo_test),
        trend="add", seasonal="add", seasonal_periods=4,
    )

    cvd = pd.read_csv(cvd_path)
    n_train = int(0.9 * len(cvd))
    cvd_train = cvd.iloc[:n_train].copy()
    cvd_test = cvd.iloc[n_train:].copy()
    cvd_ses = forecast(cvd_train["cvd"], len(cvd_test))
    cvd_holt = forecast(cvd_train["cvd"], len(cvd_test), trend="add")
    cvd_hw = forecast(
        cvd_train["cvd"], len(cvd_test),
        trend="add", seasonal="add", seasonal_periods=4,
    )

    fig, axes = plt.subplots(2, 1, figsize=(11, 8), constrained_layout=True)

    train_x = np.arange(len(shampoo_train))
    test_x = np.arange(len(shampoo_train), len(shampoo))
    axes[0].plot(train_x, shampoo_train["Sales"], marker="o", label="Train actual")
    axes[0].plot(test_x, shampoo_test["Sales"], marker="o", label="Test actual")
    axes[0].plot(test_x, shampoo_ses, marker="o", label="SES")
    axes[0].plot(test_x, shampoo_holt, marker="o", label="Holt")
    axes[0].plot(test_x, shampoo_hw, marker="o", label="Holt-Winters p=4")
    axes[0].axvline(len(shampoo_train) - 0.5, color="black", linestyle="--", linewidth=1)
    axes[0].set(title="Shampoo: source split and forecasts",
                xlabel="Observation index", ylabel="Sales")
    axes[0].legend(ncol=3, fontsize=8)

    train_x = np.arange(len(cvd_train))
    test_x = np.arange(len(cvd_train), len(cvd))
    axes[1].plot(train_x, cvd_train["cvd"], marker="o", label="Train actual")
    axes[1].plot(test_x, cvd_test["cvd"], marker="o", label="Test actual")
    axes[1].plot(test_x, cvd_ses, marker="o", label="SES")
    axes[1].plot(test_x, cvd_holt, marker="o", label="Holt")
    axes[1].plot(test_x, cvd_hw, marker="o", label="Holt-Winters p=4")
    axes[1].axvline(len(cvd_train) - 0.5, color="black", linestyle="--", linewidth=1)
    axes[1].set(title="CVD: source split and forecasts",
                xlabel="Quarter index", ylabel="CVD deaths")
    axes[1].legend(ncol=3, fontsize=8)

    svg_path = output_dir / "T08-forecast-comparison.svg"
    png_path = output_dir / "T08-forecast-comparison.png"
    fig.savefig(svg_path, format="svg")
    fig.savefig(png_path, dpi=160)
    plt.close(fig)
    print(svg_path)
    print(png_path)


if __name__ == "__main__":
    main()
