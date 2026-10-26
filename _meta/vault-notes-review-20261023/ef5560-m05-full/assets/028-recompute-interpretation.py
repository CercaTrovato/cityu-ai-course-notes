from pathlib import Path
import json
import pandas as pd

root = Path(r'D:\上课资料\CityU\EF5560_Fintech_and_AI_in_Finance\course_files_export\class05\class05')
out = Path(__file__).parent
panel = pd.read_csv(root / 'hsi_stock_excess_return_panel.csv')
week = panel.loc[panel.forecast_week.eq('2026-06-26')].dropna(subset=['mom60d_rank']).copy()
week['recomputed_rank'] = week.mom60d.rank(method='average', pct=True) - .5
imp = pd.read_csv(root / 'stock_drop_zero_importance.csv')
result = {
    'standardized_example':(12-4)/8,
    'coefficient_over_se':[.30/.10,-.20/.25],
    'excess_return_example_pct':1.2-.1,
    'four_rank_example':[q/4-.5 for q in [1,2,3,4]],
    'ols_forecast_pct': .10 + .30 * 1 - .20 * .5,
    'ols_changed_forecast_pct': .10 + .30 * 2 - .20 * .5,
    'lasso_forecast_pct': .10 + .24,
    'orthogonal_lasso': {'ols_slopes':[.30,-.20], 'lambda':.06, 'soft_threshold_slopes':[.24,-.14]},
    'orthogonal_lasso_variant':{'lambda':.25,'soft_threshold_slopes':[max(.3-.25,0),-max(.2-.25,0)]},
    'momentum_week_available':len(week),
    'rank_max_abs_recompute_error':float((week.mom60d_rank-week.recomputed_rank).abs().max()),
    'momentum_top_bottom':week.sort_values('mom60d_rank', ascending=False).iloc[list(range(5))+list(range(len(week)-5,len(week)))][['ticker','mom60d_rank']].to_dict('records'),
    'drop_zero':{'full_r2':1-9.6/20,'zeroed_r2':1-11.2/20,'delta_r2':(11.2-9.6)/20,'variant_negative':(8.8-9.6)/20},
    'importance_top3_pp':imp.head(3).assign(percentage_points=lambda d:d.delta_r2*100).to_dict('records'),
    'response_v0_pct':[.10+.40*max(0,m) for m in [-.5,0,.5]],
    'response_v025_pct':[.10+.40*max(0,m-.25) for m in [-.5,0,.5]],
}
(out/'recompute-interpretation-results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
