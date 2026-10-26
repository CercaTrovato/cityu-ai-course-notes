from pathlib import Path
import json

folder = Path(__file__).parent
old_results = Path(r'E:\app-data\codex\scratchpad\ef5560-m05-20261008\recompute-interpretation-results.json')
previous = json.loads(old_results.read_text(encoding='utf-8'))
result = {
    'p_values_as_percent': {'momentum': 0.003 * 100, 'volatility': 0.42 * 100},
    't_ratio_no_unit': {'momentum': 0.30 / 0.10, 'volatility': -0.20 / 0.25},
    'zero_baseline_error_reduction_percent': {'full': (1-9.6/20)*100, 'zeroed': (1-11.2/20)*100},
    'threshold_variant_difference': .10-.25,
    'previous_results_read': str(old_results),
    'old_week_available': previous['momentum_week_available'],
    'old_rank_max_abs_recompute_error':previous['rank_max_abs_recompute_error'],
}
(folder/'recompute-interpretation-readable-results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
