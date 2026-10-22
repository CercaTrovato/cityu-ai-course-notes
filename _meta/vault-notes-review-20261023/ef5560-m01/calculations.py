import csv, json, math
from pathlib import Path

out=Path(__file__).parent
prices=[100,110,99,108.9]
simple=[prices[i]/prices[i-1]-1 for i in range(1,len(prices))]
logs=[math.log(prices[i]/prices[i-1]) for i in range(1,len(prices))]
mean=sum(simple)/3
sample_var=sum((x-mean)**2 for x in simple)/2
sample_sd=math.sqrt(sample_var)
geo=(prices[-1]/prices[0])**(1/3)-1
cagr=(prices[-1]/prices[0])**(12/3)-1
drawdowns=[]; peak=prices[0]
for p in prices:
    peak=max(peak,p); drawdowns.append(p/peak-1)
pdd=[0.01243853052,0.1356]
jd=[0.047758570,0.0666]
ls=[0.5*a-0.5*b for a,b in zip(pdd,jd)]
market_path=Path(r'D:\上课资料\CityU\EF5560_Fintech_and_AI_in_Finance\course_files_export\class01\class01\market_index_prices_monthly_240m.csv')
with market_path.open(encoding='utf-8-sig',newline='') as f:
    market=list(csv.DictReader(f))
hang_start=float(market[0]['HK_HangSeng']); hang_end=float(market[-1]['HK_HangSeng'])
hang_multiple=hang_end/hang_start
hang_cagr=hang_multiple**(12/(len(market)-1))-1
r2_actual=[1.0,-1.0,2.0,0.0]; r2_model=[0.8,-0.6,1.4,0.4]; r2_baseline=[0.5]*4
r2_model_sse=sum((a-m)**2 for a,m in zip(r2_actual,r2_model))
r2_baseline_sse=sum((a-b)**2 for a,b in zip(r2_actual,r2_baseline))
r2_demo=1-r2_model_sse/r2_baseline_sse
payload={
  'simple_returns':simple,'log_returns':logs,'log_sum_to_terminal':math.exp(sum(logs))-1,
  'geometric_monthly':geo,'cagr_3m_to_12m':cagr,'sample_sd':sample_sd,
  'annualized_sd':sample_sd*math.sqrt(12),'drawdowns':drawdowns,'max_drawdown':min(drawdowns),
  'pdd_jd_two_week_long_short':ls,
  'hang_seng_source':str(market_path),'hang_seng_rows':len(market),'hang_seng_multiple':hang_multiple,'hang_seng_239_interval_cagr':hang_cagr,
  'r2_demo':{'actual_percent':r2_actual,'model_percent':r2_model,'baseline_percent':r2_baseline,'model_sse_percentage_point_squared':r2_model_sse,'baseline_sse_percentage_point_squared':r2_baseline_sse,'r2':r2_demo},
  'leakage_full_sample_mean':[sum([1,2,3])/3,sum([1,2,3,100])/4],
  'checks':{
    'terminal_8_9pct':abs(math.exp(sum(logs))-1-0.089)<1e-12,
    'sample_sd_matches':abs(sample_sd-0.11547005383792516)<1e-12,
    'annualized_sd_40pct':abs(sample_sd*math.sqrt(12)-0.4)<1e-12,
    'max_drawdown_minus_10pct':abs(min(drawdowns)+0.1)<1e-12,
    'full_sample_scaling_leaks_test_extreme':sum([1,2,3,100])/4 != sum([1,2,3])/3,
    'hang_seng_cagr_1_511468pct':abs(hang_cagr-0.01511468)<1e-8,
    'r2_demo_0_856':abs(r2_demo-0.856)<1e-12,
  }
}
(out/'calculation-results.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(payload['checks'],ensure_ascii=False,indent=2))
