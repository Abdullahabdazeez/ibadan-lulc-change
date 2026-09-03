from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

OUT = Path('outputs/charts')
OUT.mkdir(parents=True, exist_ok=True)
classes = ['Built-up','Vegetation','Water','Bare soil']
a13=np.array([99.866,3112.233,5.063,3.418])
a23=np.array([330.177,2881.903,4.199,4.302])

fig,ax=plt.subplots(figsize=(10,6)); x=np.arange(4); w=.36
ax.bar(x-w/2,a13,w,label='2013'); ax.bar(x+w/2,a23,w,label='2023')
ax.set_xticks(x,classes); ax.set_ylabel('Area (km²)'); ax.set_title('Land-Cover Area in Ibadan, 2013 and 2023'); ax.legend(); ax.spines[['top','right']].set_visible(False)
fig.tight_layout(); fig.savefig(OUT/'portfolio_area_comparison.png',dpi=300); plt.close(fig)

net=a23-a13
fig,ax=plt.subplots(figsize=(9,6)); ax.bar(classes,net); ax.axhline(0,lw=.8); ax.set_ylabel('Net change (km²)'); ax.set_title('Net Land-Cover Change in Ibadan, 2013–2023'); ax.spines[['top','right']].set_visible(False)
for i,v in enumerate(net): ax.text(i,v+(8 if v>=0 else -18),f'{v:+.1f}',ha='center',va='bottom' if v>=0 else 'top')
fig.tight_layout(); fig.savefig(OUT/'portfolio_net_change.png',dpi=300); plt.close(fig)

fig,ax=plt.subplots(figsize=(8,6)); ax.bar(['Vegetation','Other classes'],[246.104,248.235-246.104]); ax.set_ylabel('Area converted to built-up (km²)'); ax.set_title('Origin of New Built-up Land, 2013–2023'); ax.text(0,250,'99.14%',ha='center'); ax.text(1,7,'0.86%',ha='center'); ax.spines[['top','right']].set_visible(False)
fig.tight_layout(); fig.savefig(OUT/'portfolio_new_builtup_origin.png',dpi=300); plt.close(fig)

metrics=['Overall Accuracy','Balanced Accuracy','Macro F1',"Cohen's Kappa"]; vals=[.875,.9259,.6354,.7935]
fig,ax=plt.subplots(figsize=(9,6)); ax.barh(metrics,vals); ax.set_xlim(0,1); ax.set_xlabel('Score'); ax.set_title('Classification Validation'); ax.spines[['top','right']].set_visible(False)
for i,v in enumerate(vals): ax.text(v+.015,i,f'{v:.3f}',va='center')
fig.tight_layout(); fig.savefig(OUT/'portfolio_validation.png',dpi=300); plt.close(fig)
