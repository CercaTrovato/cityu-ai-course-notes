"""Build a reviewable, text-selectable EF5560 report draft from EF5560-A01-step-by-step.ipynb outputs.

Requires reportlab. The report remains DRAFT until the team checks every claim,
confirms member details, and approves the course-required AI-use statement.
"""

from __future__ import annotations

import csv
import json
import os
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
)


WORK = Path(__file__).resolve().parent
OUTPUT = WORK / "output"
SUBMISSION = (WORK.parent if WORK.name == "work" else WORK) / "submission"
SUBMISSION.mkdir(exist_ok=True)
DATA = json.loads((OUTPUT / "results.json").read_text(encoding="utf-8"))


def load_csv(name: str) -> list[dict[str, str]]:
    with (OUTPUT / name).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


STYLES = getSampleStyleSheet()
STYLES.add(ParagraphStyle(name="TitleCustom", parent=STYLES["Title"], fontName="Helvetica-Bold", fontSize=22, leading=27, textColor=colors.HexColor("#18324A"), spaceAfter=17))
STYLES.add(ParagraphStyle(name="SectionCustom", parent=STYLES["Heading1"], fontName="Helvetica-Bold", fontSize=14, leading=18, textColor=colors.HexColor("#18324A"), spaceBefore=5, spaceAfter=8))
STYLES.add(ParagraphStyle(name="SubCustom", parent=STYLES["Heading2"], fontName="Helvetica-Bold", fontSize=11.5, leading=14, spaceBefore=6, spaceAfter=5))
STYLES.add(ParagraphStyle(name="BodyCustom", parent=STYLES["BodyText"], fontName="Helvetica", fontSize=10.5, leading=15, spaceAfter=8))
STYLES.add(ParagraphStyle(name="SmallCustom", parent=STYLES["BodyText"], fontName="Helvetica", fontSize=9.2, leading=12.5, spaceAfter=6))
STYLES.add(ParagraphStyle(name="CaptionCustom", parent=STYLES["BodyText"], fontName="Helvetica", fontSize=9.2, leading=12, alignment=TA_CENTER, spaceBefore=3, spaceAfter=8))
STYLES.add(ParagraphStyle(name="FormulaCustom", parent=STYLES["BodyText"], fontName="Helvetica", fontSize=11, leading=17, alignment=TA_CENTER, spaceBefore=7, spaceAfter=9))


def p(text: str, style: str = "BodyCustom") -> Paragraph:
    return Paragraph(text, STYLES[style])


def heading(text: str) -> Paragraph:
    return p(text, "SectionCustom")


def formula(text: str) -> Paragraph:
    """A visibly typeset display equation; never expose raw x^2 or LaTeX source."""
    return p(text, "FormulaCustom")


def mse(value: str | float) -> str:
    return f"{float(value):.10f}"


def summary(value: str | float) -> str:
    return f"{float(value):.6f}"


def coefficient(value: str | float) -> str:
    number = float(value)
    return f"{0.0 if abs(number) < 0.5e-8 else number:.8f}"


def image(name: str, width: float, height: float) -> Image:
    return Image(str(OUTPUT / name), width=width * inch, height=height * inch, kind="proportional")


def grid(headers: list[str], rows: list[list[str]], widths: list[float]) -> Table:
    values = [[p(h, "SmallCustom") for h in headers]]
    values.extend([[p(str(v), "SmallCustom") for v in row] for row in rows])
    table = Table(values, colWidths=[w * inch for w in widths], repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E5EDF3")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#18324A")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7F9FB")]),
        ("LINEBELOW", (0, 0), (-1, 0), 0.7, colors.HexColor("#728797")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return table


def page_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#B9C8D3"))
    canvas.line(0.7 * inch, 0.55 * inch, 7.55 * inch, 0.55 * inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#536878"))
    canvas.drawString(0.7 * inch, 0.4 * inch, "EF5560 2026 ML Investment Project | DRAFT - team review required")
    canvas.drawRightString(7.55 * inch, 0.4 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build() -> Path:
    story = []
    add = story.append
    results = {r["model"]: r for r in load_csv("table_1_prediction.csv")}
    portfolios = load_csv("table_3_portfolios.csv")
    coefficients = load_csv("table_2_coefficients.csv")
    forest = load_csv("forest_grid.csv")
    pvals = load_csv("lasso_grid.csv")
    selected = DATA["portfolio_model_selected"]
    rule = DATA["portfolio_rule_selected"]
    sector = DATA["largest_validation_sector_weight"]
    pair = DATA["strongly_correlated_pair"]

    # 1 Cover
    add(Spacer(1, 0.85 * inch))
    add(p("2026 Machine-Learning Investment Assignment", "TitleCustom"))
    add(p("EF5560 | FinTech and AI in Finance", "SectionCustom"))
    add(Spacer(1, 0.28 * inch))
    add(p("<b>Lead student ID:</b> [LEAD_ID - replace before submission]"))
    add(p("<b>Team members:</b> [English names and CityU student numbers - confirm before submission]"))
    add(p("<b>Submission:</b> Report PDF, weekly weight CSV, and source-code ZIP"))
    add(Spacer(1, 0.4 * inch))
    add(p("<b>Decision in this draft.</b> We use pooled OLS forecasts and rank stocks each week. For the final long-only portfolio, we hold 16 stocks equally and allow no more than six from one sector. On the 26 validation weeks this constraint raised annualized Sharpe from 4.453041 to 4.764914 and improved maximum drawdown from -0.047750 to -0.042543; its information ratio was slightly lower (7.707589 versus 7.865440). These are simulated-data results, not expected real-market returns."))
    add(p("<b>Review status.</b> The analysis and official weight-file checker have run. Member details, final wording, and the team's own review of claims and AI-use statement remain to be confirmed before submission.", "SmallCustom"))
    add(PageBreak())

    # 2 Q1
    add(heading("Q1. Data and prediction benchmark"))
    add(p("The handout contains 80 labelled stocks in each of 260 simulated weeks. Weeks 1-78 form 6,240 training stock-weeks, Weeks 79-104 form 2,080 validation stock-weeks, and Weeks 105-260 form 12,480 private stock-weeks. The last block has no visible outcomes. The training target y = ret_next_week - rf_weekly has mean -0.00102268 and sample standard deviation 0.05650977, both in decimal weekly-return units. We did not shift the outcome: the supplied next-week return is already aligned with its forecast row."))
    add(formula("y<sub>i,t</sub> = r<sub>i,t+1</sub> - r<sub>f,t</sub>"))
    add(image("figure_1_correlations.png", 6.4, 4.95))
    add(p("Figure 1. Pearson correlations of all 17 predictors using training rows only.", "CaptionCustom"))
    add(p(f"The strongest absolute pair is <i>{pair['first']}</i> and <i>{pair['second']}</i> (r = {pair['r']:.6f}). Correlation means the two signals overlap; it does not establish that either causes returns. A random stock-week split would mix dates across training and evaluation and let the model exploit a market state it could not have known at the forecast date."))
    add(p("The zero-excess-return forecast sets predicted y to 0, equivalent to forecasting total return as rf_weekly. Its pooled validation MSE is 0.0030908984 squared decimal-return units. All models use the same 2,080 validation rows. In the equations, p<sub>i</sub> is a model's prediction and N is the row count.", "SmallCustom"))
    add(formula("MSE = sum<sub>i</sub>(y<sub>i</sub> - p<sub>i</sub>)<super>2</super> / N&nbsp;&nbsp;&nbsp;&nbsp; R<super>2</super><sub>OOS</sub> = 1 - sum<sub>i</sub>(y<sub>i</sub> - p<sub>i</sub>)<super>2</super> / sum<sub>i</sub>y<sub>i</sub><super>2</super>"))
    add(PageBreak())

    # 3 Q2 first half
    add(heading("Q2. OLS and LASSO"))
    add(p("We estimated each predictor's mean and standard deviation on Weeks 1-78, then applied that fixed scaler to Weeks 79-104. OLS and LASSO both include an intercept and the same 17 predictors. This makes their coefficients comparable and prevents validation data from influencing preprocessing."))
    add(formula("z<sub>i,j</sub> = (x<sub>i,j</sub> - training mean<sub>j</sub>) / training SD<sub>j</sub>"))
    add(p("Table 1. Pooled prediction results (MSE: squared decimal-return units; OOS R<super>2</super>: decimal).", "CaptionCustom"))
    add(grid(["Model", "Training MSE", "Validation MSE", "Validation OOS R<super>2</super>"],
             [[name, mse(results[name]['training_mse']), mse(results[name]['validation_mse']), summary(results[name]['validation_oos_r2'])]
              for name in ["Zero", "OLS", "LASSO", "Random forest"]], [1.6, 1.55, 1.55, 1.65]))
    add(Spacer(1, 0.13 * inch))
    add(p("OLS improves on the zero benchmark in training but has negative validation OOS R<super>2</super> (-0.020575). The selected LASSO reaches 0.006018 and is the best of these models by validation MSE. The forest fits training much better but performs worst in validation. More flexibility did not help here."))
    add(image("figure_2_lasso_penalty.png", 6.0, 3.2))
    add(p("Figure 2. Validation MSE across eight prespecified LASSO penalties.", "CaptionCustom"))
    add(p("The minimum occurs at alpha = 0.00372759. One of 17 slope coefficients remains nonzero. We selected alpha using validation MSE only; the private block was not used.", "SmallCustom"))
    add(PageBreak())

    # 4 Q2 coefficients and Q3
    add(heading("Q2. Which signals survive the penalty?"))
    add(p("Table 2. Coefficients after training-only standardization. The intercept is separate and not counted as a selected predictor.", "CaptionCustom"))
    add(grid(["Predictor", "OLS coefficient", "LASSO coefficient"],
             [[r["predictor"], coefficient(r['ols_standardized_coefficient']), coefficient(r['lasso_standardized_coefficient'])] for r in coefficients],
             [2.55, 1.9, 1.9]))
    add(p("Only quality_signal remains in LASSO (coefficient 0.00274348). Its shrinkage lowers validation MSE from 0.0031544950 for OLS to 0.0030722989. The correlated momentum signals in Q1 both disappear; this does not prove that momentum has no economic effect. The penalty selects a short predictive equation, not a causal ranking.", "SmallCustom"))
    add(heading("Q3. A nonlinear comparison"))
    add(p("We fitted a 200-tree random forest with seed 2026. We compared five settings on the same validation rows. Each pair below is (maximum depth, minimum observations per leaf), followed by validation MSE:"))
    add(p("(5, 10): 0.0038428017;&nbsp;&nbsp; (8, 10): 0.0039446124;&nbsp;&nbsp; (12, 10): 0.0038876442;<br/>(8, 25): 0.0040134832;&nbsp;&nbsp; (unlimited, 25): 0.0039457232.", "SmallCustom"))
    add(p("The first setting wins. A forest can help if returns depend on thresholds or combinations of signals. Here its training MSE is low, but validation MSE is worse than LASSO and even the zero forecast. It appears to have fitted patterns that did not hold in later weeks."))
    add(PageBreak())

    # 5 Q4
    add(heading("Q4. Characteristic importance"))
    add(p("We kept the selected forest fixed. For each predictor in turn, we set its standardized validation value to zero (its training mean), recalculated OOS R<super>2</super>, and subtracted the new R<super>2</super> from the original. No model was refitted. The five largest values are shown in Figure 3, with their signs retained."))
    add(formula("Importance<sub>j</sub> = R<super>2</super><sub>OOS, original</sub> - R<super>2</super><sub>OOS, predictor j replaced by zero</sub>"))
    add(image("figure_3_importance.png", 6.1, 2.65))
    add(p("Figure 3. Fixed-model drop-to-zero importance on validation rows.", "CaptionCustom"))
    add(image("figure_4_response_profile.png", 6.1, 2.65))
    add(p("Figure 4. Mean prediction when sector_trend varies from its training 10th to 90th standardized percentile; other validation inputs stay at their observed values.", "CaptionCustom"))
    add(p("The forest relies most on sector_trend (importance 0.060893) and liquidity_state (0.046827). Its average response to sector_trend declines in steps rather than following one slope. LASSO instead retains only quality_signal. These answer different questions: LASSO asks which linear slopes survive a joint penalty, while drop-to-zero asks how much this fitted forest's validation predictions depend on each input. Correlated predictors can share importance, and neither result is causal.", "SmallCustom"))
    add(PageBreak())

    # 6 Q5
    add(heading("Q5. Forecasts and validation portfolios"))
    add(p("For each validation week we rank 80 stocks by predicted excess return, with asset_id ascending to break ties. The required long-short spread is the mean total return of the top 16 minus that of the bottom 16. The required long-only rule gives 1/16 to each top stock and zero to the others. We rebalance the equal-weight benchmark to 1/80 each week."))
    add(formula("Sharpe = 52<super>1/2</super> mean(r<sub>p</sub> - r<sub>f</sub>) / s(r<sub>p</sub> - r<sub>f</sub>)&nbsp;&nbsp;&nbsp;&nbsp; IR = 52<super>1/2</super> mean(r<sub>p</sub> - r<sub>EW</sub>) / s(r<sub>p</sub> - r<sub>EW</sub>)"))
    add(p("Table 3. Validation portfolios, Weeks 79-104 (returns and drawdown: decimals; ratios: annualized).", "CaptionCustom"))
    add(grid(["Model / rule", "Spread / week", "Sharpe", "IR vs EW", "Max DD"],
             [[r["model_rule"], "N/A" if not r["mean_weekly_long_short_spread"] else summary(r['mean_weekly_long_short_spread']),
               summary(r['long_only_sharpe']), summary(r['long_only_information_ratio']),
               summary(r['long_only_max_drawdown'])] for r in portfolios],
             [2.45, 1.18, .9, .9, 1.1]))
    add(Spacer(1, 0.13 * inch))
    add(p("The best MSE model is LASSO, but OLS has the higher top-16 Sharpe (4.453041 vs 4.292557). Ranking and portfolio payoffs depend on which stocks reach the top 16, not solely on pooled squared error. LASSO has the higher information ratio (10.929279 vs 7.865440), so no model wins on every measure. The forest is behind both on prediction and Sharpe."))
    add(p("The plain OLS top-16 rule put as much as 87.5000% in one sector in a validation week. We therefore tested one simple risk limit: move down the ranking after a sector fills six of the 16 slots. Each position stays at 6.2500%, below the 10% stock cap. With that limit, validation Sharpe rises to 4.764914 and maximum drawdown improves to -0.042543; IR slips to 7.707589. The largest sector allocation under the final rule is 37.5000% in Commerce & Industry, Week 79. We chose this rule for its Sharpe and drawdown, but it was chosen on only 26 validation weeks. A sector shock or weekly trading costs could overturn the result. Figure A1 shows the path behind the summary ratios."))
    add(p("Here r<sub>p</sub> is portfolio total return, r<sub>f</sub> is the known risk-free return, r<sub>EW</sub> is the rebalanced 80-stock benchmark, and s is the sample standard deviation across 26 weeks. Maximum drawdown starts wealth at 1 and measures its worst fall from a running peak. Ratios are set to zero if their sample standard deviation is below 10<super>-12</super>.", "SmallCustom"))
    add(formula("Maximum drawdown = min<sub>t</sub> [wealth<sub>t</sub> / prior peak<sub>t</sub> - 1]"))
    add(PageBreak())

    # 7 implementation
    add(heading("Implementation and submission checks"))
    add(p("After selecting the model and rule on validation evidence, we refit the scaler and pooled OLS on Weeks 1-104 only. We then keep both fixed and rank the 80 private-week rows separately for Weeks 105-260. The private block has no visible ret_next_week, so it cannot be used to compute or tune performance. Each output row has 16 weights of 0.06250000 and 64 weights of 0.00000000, in the official ticker and date order. The position cap is 10%, and the six-per-sector rule limits sector concentration to 37.5000%. We assume initial equal weights at the end of Week 104 and ignore transaction costs, as directed."))
    add(p("The official Python checker reports: 'Valid file: 156 dates, 80 stocks; all weight constraints satisfied.' This establishes format and constraints only; it says nothing about hidden performance. Source inputs, the model-selection grid, tables, figures, and the draft weight CSV are produced by EF5560-A01-step-by-step.ipynb. Its saved outputs also contain the 26 weekly validation returns and all 17 drop-to-zero scores, so the report's summary numbers can be traced to calculations."))
    add(p("<b>Display precision.</b> MSE uses 10 decimal places; target moments, coefficients and alpha use 8; OOS R<super>2</super>, correlations, importance scores, portfolio returns and ratios use 6; sector percentages use 4. Figure ticks use readable scale labels. All calculations and choices use unrounded values; rounding happens only for display.", "SmallCustom"))
    add(p("<b>Software:</b> Python " + DATA["versions"]["python"] + "; pandas " + DATA["versions"]["pandas"] + "; NumPy " + DATA["versions"]["numpy"] + "; scikit-learn " + DATA["versions"]["sklearn"] + "; Matplotlib " + DATA["versions"]["matplotlib"] + "; ReportLab 4.4.9 for PDF layout. <b>Random seed:</b> 2026 for the forest. OLS and LASSO are deterministic given the data and settings. <b>Main notebook (code ZIP):</b> EF5560-A01-step-by-step.ipynb."))
    add(p("<b>AI use statement - team confirmation required:</b> AI coding assistance was used in preparing this draft. The team must confirm the tools used and personally verify at least two checks before replacing this draft sentence. The current code checks the 80-by-260 panel, the time split and absence of private outcomes; the supplied weight checker also passes. The team remains responsible for every claim, calculation and conclusion."))
    add(p("<b>Limitations.</b> All numeric observations are simulated. We did not estimate transaction costs or turnover losses; these can be important for weekly rebalancing. The validation period contains only 26 weeks, and selecting a sector rule after seeing those weeks can still overfit. The private-period score is unknown until grading. No reported validation result is presented as a private-period result."))
    add(PageBreak())

    # 8 optional appendix
    add(heading("Optional one-page appendix"))
    add(image("figure_A1_validation_paths.png", 6.3, 4.8))
    add(p("Figure A1. Compounded validation wealth and drawdown for the final OLS sector-capped rule versus rebalanced equal weight.", "CaptionCustom"))
    add(p("The strategy's wealth path ends above equal weight and its validation maximum drawdown is smaller (-0.042543 vs -0.077666). The path also shows setbacks around Weeks 82 and 89, which a single Sharpe ratio hides. This chart uses the same 26 weeks used to choose the rule; it is not an independent test or evidence about private-period results.", "SmallCustom"))

    target = SUBMISSION / "DRAFT_EF5560_LEAD_ID_report.pdf"
    temp = SUBMISSION / ".DRAFT_EF5560_LEAD_ID_report.pdf"
    doc = SimpleDocTemplate(str(temp), pagesize=(8.27 * inch, 11.69 * inch),
                            leftMargin=.7 * inch, rightMargin=.7 * inch,
                            topMargin=.7 * inch, bottomMargin=.75 * inch)
    doc.build(story, onFirstPage=page_footer, onLaterPages=page_footer)
    os.replace(temp, target)
    print(target)
    return target


if __name__ == "__main__":
    build()
