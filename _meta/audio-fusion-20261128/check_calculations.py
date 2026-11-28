from pathlib import Path
import json,sys
root=Path(r'D:\上课资料\CityU');work=Path(r'E:\app-data\codex\scratchpad\ef5560-final-20261128')
sys.path.insert(0,str(root/'_meta/tools'));from safe_write import atomic_write
d={
'M11_p45':{'currency':'CNY','receivable':1000000,'financing_cap':.8,'bank_A_existing':600000,'remaining_upper_bound':1000000*.8-600000,'meaning':'upper bound; Bank B may lend less after credit assessment'},
'M11_p49':{'principal':1000,'recovered':600,'loss':1000-600,'first_loss_cap':100,'bank_under_guarantee':min(100,1000-600),'investor_under_guarantee':max(1000-600-100,0)},
'M11_p50':{'base_contribution':120-55-25-30,'operating_cost_20_contribution':120-55-25-20,'credit_loss_65_contribution':120-65-25-30,'scenario_relation':'two independent changes from the same baseline'},
'M12_p04':{'account_USD':1000,'annual_fee_rate':.0025,'annual_fee_USD':1000*.0025},
'M12_p10':{'portfolio_HKD':200000,'current_stock_weight':.5,'target_stock_weight':.4,'stock_sold_HKD':200000*(.5-.4),'bonds_bought_HKD':200000*(.5-.4),'per_trade_cost_rate':.001,'two_sided_cost_HKD':2*200000*(.5-.4)*.001,'portfolio_cost_bp':2*(.5-.4)*.001*10000},
'M12_selftest_7_2':{'stock_sold_HKD':200000*(.55-.5),'bonds_bought_HKD':200000*(.55-.5),'two_sided_cost_HKD':2*200000*(.55-.5)*.001,'portfolio_cost_bp':2*(.55-.5)*.001*10000},
'M12_p21':{'reports_2024':12536,'reports_2025':15877,'growth_count':15877-12536,'growth_percent':(15877-12536)/12536*100,'phishing_2024_rounded_estimate':12536*.62,'phishing_2025_rounded_estimate':15877*.57,'malware_share_change_percentage_points':15-8},
'source_S35':{'media_duration_seconds':7661.738667,'last_segment_start_seconds':7653.02,'last_speech_end_seconds':7659.58,'segment_start_span_seconds_floor':7653,'post_speech_media_tail_seconds':7661.738667-7659.58},
}
atomic_write(str(work/'calculation-results.json'),json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(d,ensure_ascii=False))
