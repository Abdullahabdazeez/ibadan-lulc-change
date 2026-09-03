from pathlib import Path
import numpy as np
import rasterio
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Patch

ROOT=Path('.')
OUT=ROOT/'outputs'/'maps'; OUT.mkdir(parents=True, exist_ok=True)
P13=ROOT/'data'/'authoritative'/'Ibadan_LULC_2013_FINAL.tif.tiff'
P23=ROOT/'data'/'authoritative'/'Ibadan_LULC_2023_FINAL.tif.tiff'
BND=ROOT/'data'/'processed'/'boundary'/'Ibadan_Metropolitan_Boundary.shp'
COLORS=['#d84a3a','#4f9d55','#3b82b8','#a87948']
LABELS=['Built-up','Vegetation','Water','Bare soil']
CMAP=ListedColormap(COLORS); NORM=BoundaryNorm([.5,1.5,2.5,3.5,4.5],4)
PIX_KM2=0.0009

def read_inputs():
    with rasterio.open(P13) as d:
        a13=d.read(1); bounds=d.bounds; crs=d.crs
    with rasterio.open(P23) as d:
        a23=d.read(1)
    assert a13.shape==a23.shape
    assert str(crs)=='EPSG:32631'
    mask=(a13>0)&(a23>0)
    assert int(mask.sum())==3578423
    return a13,a23,mask,bounds

def extent_km(b): return (b.left/1000,b.right/1000,b.bottom/1000,b.top/1000)
def north(ax): ax.annotate('N',xy=(.93,.91),xytext=(.93,.80),xycoords='axes fraction',ha='center',fontweight='bold',arrowprops=dict(arrowstyle='-|>',lw=1.2,color='black'))
def scale(ax,e):
    x0=e[0]+6; y=e[2]+5; ax.plot([x0,x0+10],[y,y],lw=2,color='black'); ax.text(x0,y+1,'0',fontsize=7,ha='center'); ax.text(x0+10,y+1,'10 km',fontsize=7,ha='center')
def base(ax,title,e):
    ax.set_title(title,fontsize=14,fontweight='bold',pad=10); ax.set_xlabel('Easting (km) — WGS 84 / UTM Zone 31N'); ax.set_ylabel('Northing (km)'); north(ax); scale(ax,e)
def finish(fig,name):
    fig.text(.5,.012,'Landsat 30 m | EPSG:32631 | Analysis: Abdullah Abdazeez Ayomide',ha='center',fontsize=7,color='.35')
    fig.tight_layout(rect=(.02,.035,.98,.98)); fig.savefig(OUT/f'{name}.png',dpi=170,bbox_inches='tight',facecolor='white'); fig.savefig(OUT/f'{name}.pdf',bbox_inches='tight',facecolor='white'); plt.close(fig)

def main():
    a13,a23,mask,b=read_inputs(); e=extent_km(b)
    stats={y:{i:int((a==i).sum()) for i in (1,2,3,4)} for y,a in [(2013,a13),(2023,a23)]}
    g=gpd.read_file(BND).to_crs(32631); fig,ax=plt.subplots(figsize=(7.5,8)); g.plot(ax=ax,facecolor='#f2f2f2',edgecolor='#444',linewidth=.8)
    field=next((c for c in g.columns if c.lower() in ['lga_name','lga','name_2','name']),None)
    if field:
        for _,r in g.iterrows():
            p=r.geometry.representative_point(); ax.text(p.x,p.y,str(r[field]),fontsize=6,ha='center',va='center')
    ax.set_title('Ibadan Metropolitan Area — Study Area',fontsize=14,fontweight='bold'); ax.text(.5,1.01,'Eleven Local Government Areas in Oyo State, Nigeria',transform=ax.transAxes,ha='center',fontsize=9); ax.set_xlabel('Easting (m) — WGS 84 / UTM Zone 31N'); ax.set_ylabel('Northing (m)'); ax.set_aspect('equal'); north(ax); finish(fig,'01_Study_Area')
    for y,a,n in [(2013,a13,'02_Land_Cover_2013'),(2023,a23,'03_Land_Cover_2023')]:
        fig,ax=plt.subplots(figsize=(7.5,8)); ax.imshow(np.ma.masked_where(a==0,a),cmap=CMAP,norm=NORM,extent=e,origin='upper',interpolation='nearest'); base(ax,f'Ibadan Land Cover, {y}',e); ax.legend(handles=[Patch(color=c,label=l) for c,l in zip(COLORS,LABELS)],title='Land-cover class',loc='lower right',fontsize=8)
        vals=[stats[y][i]*PIX_KM2 for i in (1,2,3,4)]; pct=[v/(mask.sum()*PIX_KM2)*100 for v in vals]; fig.text(.5,.035,' | '.join(f'{l}: {p:.2f}%' for l,p in zip(LABELS,pct)),ha='center',fontsize=8); finish(fig,n)
    fig,axs=plt.subplots(1,2,figsize=(13,7))
    for ax,a,y in zip(axs,[a13,a23],[2013,2023]):
        ax.imshow(np.ma.masked_where(a==0,a),cmap=CMAP,norm=NORM,extent=e,origin='upper',interpolation='nearest'); base(ax,str(y),e)
    fig.suptitle('Ibadan Land-Cover Change, 2013–2023',fontsize=15,fontweight='bold'); fig.legend(handles=[Patch(color=c,label=l) for c,l in zip(COLORS,LABELS)],loc='lower center',ncol=4,title='Land-cover class'); finish(fig,'04_Land_Cover_Comparison_2013_2023')
    bup=np.zeros_like(a13,dtype=np.uint8); bup[(a13==1)&mask]=1; bup[(a23==1)&(a13!=1)&mask]=2
    fig,ax=plt.subplots(figsize=(7.5,8)); cm=ListedColormap(['#777','#d84a3a']); nm=BoundaryNorm([.5,1.5,2.5],2); ax.imshow(np.ma.masked_where(bup==0,bup),cmap=cm,norm=nm,extent=e,origin='upper',interpolation='nearest'); base(ax,'Where Ibadan Expanded: New Built-up Areas, 2013–2023',e); ax.legend(handles=[Patch(color='#777',label='Built-up in 2013'),Patch(color='#d84a3a',label='New built-up by 2023')],loc='lower right'); fig.text(.5,.035,'Built-up: 99.9 km² (2013) → 330.2 km² (2023) | Gross new built-up: 248.2 km²',ha='center',fontsize=8); finish(fig,'05_Builtup_Expansion_2013_2023')
    same=(a13==a23)&mask; t=np.zeros_like(a13,dtype=np.uint8); t[same]=1; t[(a13==2)&(a23==1)&mask]=2; t[(a13!=2)&(a23==1)&(a13!=1)&mask]=3; t[(a13==1)&(a23==2)&mask]=4; t[(t==0)&mask]=5
    cols=['#d9d9d9','#d84a3a','#f28e2b','#59a14f','#4e79a7']; labs=['Stable','Vegetation → Built-up','Other → Built-up','Built-up → Vegetation','Other change']; fig,ax=plt.subplots(figsize=(7.5,8)); cm=ListedColormap(cols); nm=BoundaryNorm(np.arange(.5,6.5,1),5); ax.imshow(np.ma.masked_where(t==0,t),cmap=cm,norm=nm,extent=e,origin='upper',interpolation='nearest'); base(ax,'How the Landscape Changed: Major Land-Cover Transitions',e); ax.legend(handles=[Patch(color=c,label=l) for c,l in zip(cols,labs)],loc='lower right',fontsize=8); fig.text(.5,.035,'Dominant transition: Vegetation → Built-up = 246.104 km²',ha='center',fontsize=8); finish(fig,'06_Land_Cover_Transitions_2013_2023')
    sc=np.zeros_like(a13,dtype=np.uint8); sc[same]=1; sc[(~same)&mask]=2; fig,ax=plt.subplots(figsize=(7.5,8)); cm=ListedColormap(['#d9d9d9','#d84a3a']); nm=BoundaryNorm([.5,1.5,2.5],2); ax.imshow(np.ma.masked_where(sc==0,sc),cmap=cm,norm=nm,extent=e,origin='upper',interpolation='nearest'); base(ax,'Stable and Changed Land, 2013–2023',e); ax.legend(handles=[Patch(color='#d9d9d9',label='Stable'),Patch(color='#d84a3a',label='Changed')],loc='lower right'); changed=((~same)&mask).sum()/mask.sum()*100; fig.text(.5,.035,f'Stable: {100-changed:.2f}% | Changed: {changed:.2f}%',ha='center',fontsize=8); finish(fig,'07_Stable_vs_Changed_2013_2023')
    print('Generated authoritative seven-map PNG/PDF suite')

if __name__=='__main__': main()
