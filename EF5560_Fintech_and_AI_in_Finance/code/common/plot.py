"""
common.plot · 统一绘图风格
===========================
所有脚本用这里的 `setup()` 初始化、用 `save()` 保存。保证：
  - 中文标签不变方块（优先 Microsoft YaHei，退到 SimHei，再退到英文）
  - 同一套配色：四个指数 / 两种口径 各有固定颜色，跨图一致
  - 输出统一到 code/output/，文件名由调用方给（见 README §2 命名约定）
  - 无 GUI（Agg 后端），能在命令行和 CI 里跑
"""
from pathlib import Path
from typing import Optional
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

from .load import OUTPUT_DIR

# ---------- 配色（跨图一致） ----------
COLORS = {
    "US_S&P500": "#1f77b4", # 蓝
    "US_SPY": "#17becf",     # 青
    "HK_HangSeng": "#d62728", # 红
    "CN_CSI300": "#ff7f0e",  # 橙
    "simple": "#2ca02c",     # 绿：简单收益
    "log": "#9467bd",        # 紫：对数收益
    "PDD": "#e377c2",
    "JD": "#8c564b",
    "pair": "#111111",
    "actual": "#333333",
    "fitted": "#d62728",
    "baseline": "#7f7f7f",
}

_CJK_CANDIDATES = ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "Source Han Sans SC", "PingFang SC"]


def _pick_cjk_font() -> Optional[str]:
    installed = {f.name for f in fm.fontManager.ttflist}
    for name in _CJK_CANDIDATES:
        if name in installed:
            return name
    return None


def setup(figsize=(10, 5.5), dpi=150):
    """初始化一张图。返回 (fig, ax)。"""
    font = _pick_cjk_font()
    if font:
        plt.rcParams["font.family"] = [font, "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False   # 负号不用 Unicode 减号，避免方块
    plt.rcParams["figure.dpi"] = dpi
    plt.rcParams["axes.grid"] = True
    plt.rcParams["grid.alpha"] = 0.3
    plt.rcParams["axes.spines.top"] = False
    plt.rcParams["axes.spines.right"] = False
    fig, ax = plt.subplots(figsize=figsize)
    return fig, ax


def save(fig, name: str, note: Optional[str] = None) -> Path:
    """保存到 code/output/<name>.png。name 不带扩展名，如 'L01_03_drawdown'。
    note：可选的图底注（数据来源、口径），会以小字加在图下方。
    """
    if note:
        fig.text(0.01, 0.005, note, fontsize=7, color="#666", ha="left", va="bottom")
    fig.tight_layout(rect=(0, 0.03 if note else 0, 1, 1))
    out = OUTPUT_DIR / f"{name}.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"[saved] {out}")
    return out


def pct(x, digits=2) -> str:
    """0.2062 → '20.62%'"""
    return f"{x * 100:.{digits}f}%"
