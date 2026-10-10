"""Reproduce the adjacent p.17 dataset; does not read or write the vault.

Python dependencies: matplotlib, numpy. Run from any directory:
  python plot-common-size.py --output-dir OUTPUT_DIRECTORY
Default input is data.json next to this script. Outputs common-size.svg/png.
The dataset's source field is provenance, not a runtime filesystem dependency.
"""
from pathlib import Path
import argparse, json, io, os, tempfile
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def atomic_write(path, content):
    """Same-directory replacement, including binary PNG; never truncate target."""
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    data=content.encode('utf-8') if isinstance(content,str) else content
    fd,tmp=tempfile.mkstemp(dir=path.parent,prefix='.render-',suffix=path.suffix)
    try:
        with os.fdopen(fd,'wb') as f:
            f.write(data);f.flush();os.fsync(f.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)

def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--data',type=Path,default=Path(__file__).with_name('data.json'))
    cli.add_argument('--output-dir',type=Path,default=Path(__file__).parent)
    args=cli.parse_args()
    data=json.loads(args.data.read_text(encoding='utf-8'));amounts=data['input']
    percentages={}
    for company,items in amounts.items():
        total=items['Current assets']+items['Non-current assets']
        assert total>0
        assert items['Current liabilities']+items['Non-current liabilities']+items['Equity']==total
        percentages[company]={k:v/total*100 for k,v in items.items()}
        for k,v in percentages[company].items():
            assert abs(v-data['computed_percentages'][company][k])<1e-10
    plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none','font.size':11,'svg.hashsalt':'cityu-m03-common-size'})
    fig,axes=plt.subplots(1,2,figsize=(11,4.2),sharey=True)
    groups=[['Current assets','Non-current assets'],['Current liabilities','Non-current liabilities','Equity']]
    colors=['#316b91','#adc9dd','#cc9b56']
    for ax,keys,title in zip(axes,groups,['Assets: each total = 100%','Financing: liabilities + equity = 100%']):
        bottom=np.zeros(2)
        for key,color in zip(keys,colors):
            values=np.array([percentages[c][key] for c in amounts])
            ax.bar(list(amounts),values,bottom=bottom,label=key,color=color,edgecolor='white')
            for x,y,b in zip(range(2),values,bottom):
                ax.text(x,b+y/2,f'{y:.1f}%',ha='center',va='center',color='white' if color=='#316b91' else '#172c3b')
            bottom+=values
        ax.set_title(title);ax.set_ylim(0,100)
        ax.set_ylabel('Percent of each company total assets')
        ax.legend(loc='upper center',bbox_to_anchor=(0.5,-0.1),frameon=False)
        ax.spines[['top','right']].set_visible(False)
    fig.suptitle('Common-size balance sheets - Week 3 p.17 source amounts')
    fig.tight_layout(rect=[0,0.08,1,0.93])
    svg=io.StringIO();fig.savefig(svg,format='svg',metadata={'Date':None})
    atomic_write(args.output_dir/'common-size.svg',svg.getvalue())
    png=io.BytesIO();fig.savefig(png,format='png',dpi=150)
    atomic_write(args.output_dir/'common-size.png',png.getvalue())
    plt.close(fig)
    print(json.dumps({'input':str(args.data.resolve()),'output':str(args.output_dir.resolve()),'percentages':percentages},ensure_ascii=False))

if __name__=='__main__':main()
