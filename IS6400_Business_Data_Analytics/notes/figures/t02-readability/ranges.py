from pathlib import Path
import sys,io,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0,'D:/上课资料/CityU/_meta/tools')
from safe_write import atomic_write
import argparse
_parser=argparse.ArgumentParser(description='只读图源与独立输出目录；SVG保留可检索文字')
_parser.add_argument('--output-dir',type=Path,default=Path(__file__).parent)
_args=_parser.parse_args()
HERE=_args.output_dir.resolve()
HERE.mkdir(parents=True,exist_ok=True)
plt.rcParams['svg.fonttype']='none'
fig,ax=plt.subplots(figsize=(9,3.7),layout='constrained')
for y,end,label in [(3,2,'cell 5 training support [0,2)'),(2,3,'cell 13 new support [0,3)'),(1,2,'cell 13 x display window [0,2]')]:
 ax.plot([0,end],[y,y],lw=8,color='tab:blue' if y==3 else 'tab:orange' if y==2 else 'gray')
 ax.scatter([0],[y],s=70,color='black');ax.scatter([end],[y],s=70,facecolor='white' if y>1 else 'black',edgecolor='black',zorder=5)
 ax.text(.05,y+.18,label,fontsize=10)
ax.axvspan(2,3,color='tab:red',alpha=.12,label='new support beyond training / cropped')
ax.plot([2.5],[2],marker='*',ms=12,color='black');ax.annotate('teaching x=2.5 (not saved observation)',(2.5,2),xytext=(1.3,.4),arrowprops={'arrowstyle':'->'},fontsize=9)
ax.set(xlim=(-.1,3.25),ylim=(.2,3.7),xlabel='x (synthetic input unit)',title='Input support differs from display window; no fitted curve')
ax.set_yticks([]);ax.legend(loc='upper right',fontsize=8)
b=io.StringIO();fig.savefig(b,format='svg');atomic_write(str(HERE/'input-ranges.svg'),b.getvalue());
atomic_write(str(HERE/'input-ranges.json'),json.dumps({'source':'T02 cells5/13','training_support':[0,2],'training_right_open':True,'new_support':[0,3],'new_right_open':True,'display_window':[0,2],'teaching_point':2.5,'actual_saved_outside_count':'unknown; raw random arrays not saved'},indent=2)+'\n')
