from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime

import argparse
parser=argparse.ArgumentParser(description='Reproduce the two lecture-based charts outside the vault.')
parser.add_argument('--output-dir',type=Path,default=Path('E:/app-data/codex/scratchpad/ef5560-m08-charts'))
HERE=parser.parse_args().output_dir
HERE.mkdir(parents=True,exist_ok=True)
data={
 'source':'Lec08_DeFi_NFT_and_RWA.pdf',
 'sha256':'1c296befc1a2233549b6355eda2f0c340ea7ef6657d6bf4b1ddbf53b0f254101',
 'tvl':{'page':6,'unit':'USD billion','points':[{'label':'Nov 2021 peak','date':'2021-11','value':177.5},{'label':'29 Jul 2026','date':'2026-07-29','value':75.4}],'limit':'Only the two labelled values. Complete weekly series unavailable; no interpolated line.'},
 'bonds':{'page':28,'unit':'HKD billion equivalent, rounded','years':[2023,2024,2025],'values':[0.8,6,10]}
}
(HERE/'chart-data.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
plt.rcParams.update({'font.family':'Microsoft YaHei','svg.fonttype':'none','font.size':12,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(figsize=(8,4),layout='constrained')
dates=[datetime(2021,11,1),datetime(2026,7,29)]
ax.scatter(dates,[177.5,75.4],s=100,c=['#B68A26','#A72B4D'],zorder=3)
for x,y,lab in zip(dates,[177.5,75.4],['Nov 2021: 177.5','29 Jul 2026: 75.4']):
    ax.annotate(lab,(x,y),xytext=(0,12),textcoords='offset points',ha='center')
ax.set(ylabel='TVL (USD billion)',ylim=(0,210),title='Two labelled TVL observations — lecture p.6')
ax.set_xlim(datetime(2020,8,1),datetime(2027,7,1))
ax.grid(axis='y',alpha=.2)
fig.savefig(HERE/'tvl-anchors.svg');fig.savefig(HERE/'tvl-anchors.png',dpi=160);plt.close(fig)
fig,ax=plt.subplots(figsize=(7.5,3.7),layout='constrained')
bars=ax.bar(['2023','2024','2025'],[.8,6,10],color='#08607E',width=.55)
ax.bar_label(bars,labels=['0.8','6','10'],padding=4)
ax.set(ylabel='HKD billion equivalent (rounded)',ylim=(0,12),title='HKSAR digital green bond issuance — lecture p.28')
ax.grid(axis='y',alpha=.18);ax.set_axisbelow(True)
fig.savefig(HERE/'green-bonds.svg');fig.savefig(HERE/'green-bonds.png',dpi=160);plt.close(fig)
print('charts generated; peak-to-end fall',100*(1-75.4/177.5))
