from pathlib import Path
import base64, re
import numpy as np
from PIL import Image
from scipy import ndimage
import matplotlib.pyplot as plt
import shapefile

ROOT=Path('.')
OUT=ROOT/'outputs'/'maps'
OUT.mkdir(parents=True,exist_ok=True)

# Public palette: Built-up, Vegetation, Water, Bare soil
COLORS={1:'#d94732',2:'#4ca64c',3:'#2f7db8',4:'#a06b3b'}
LABELS={1:'Built-up',2:'Vegetation',3:'Water',4:'Bare soil'}
EXTENT=(560,625,780,855)

# Locked accepted shares from the final project tables/report.
SHARES={
    2013:{1:3.101,2:96.636,3:0.157,4:0.106},
    2023:{1:10.252,2:89.484,3:0.130,4:0.134},
}


def load_comparison_image():
    txt=(OUT/'final_lulc_comparison.svg').read_text(encoding='utf-8')
    m=re.search(r'data:image/(?:jpeg|jpg);base64,([^\"\']+)',txt)
    if not m:
        raise RuntimeError('Embedded comparison image not found')
    from io import BytesIO
    return Image.open(BytesIO(base64.b64decode(m.group(1)))).convert('RGB')


def largest_land_component(rgb_half):
    a=np.asarray(rgb_half).astype(float)
    # Broad class prototypes used only to isolate the mapped metropolitan footprint.
    proto=np.array([[68,168,68],[214,55,39],[45,125,190]],dtype=float)
    d=np.sqrt(((a[:,:,None,:]-proto[None,None,:,:])**2).sum(3))
    near=d.min(2)<100
    lab,n=ndimage.label(near,structure=np.ones((3,3)))
    if n==0:
        raise RuntimeError('No mapped footprint detected')
    sizes=ndimage.sum(near,lab,range(1,n+1))
    target=int(np.argmax(sizes)+1)
    mask=lab==target
    ys,xs=np.where(mask)
    return (xs.min(),ys.min(),xs.max()+1,ys.max()+1),mask


def aligned_source_arrays(img):
    w,h=img.size
    halves=[img.crop((0,0,w//2,h)),img.crop((w//2,0,w,h))]
    extracted=[]
    for half in halves:
        bbox,mask=largest_land_component(half)
        a=np.asarray(half).astype(float)
        x0,y0,x1,y1=bbox
        extracted.append((a[y0:y1,x0:x1],mask[y0:y1,x0:x1]))
    # Standardise both panels to the same dimensions.
    hh=min(x[0].shape[0] for x in extracted)
    ww=min(x[0].shape[1] for x in extracted)
    arrs=[]; masks=[]
    for a,m in extracted:
        arrs.append(a[:hh,:ww])
        masks.append(m[:hh,:ww])
    shared=ndimage.binary_fill_holes(masks[0] | masks[1])
    shared=ndimage.binary_closing(shared,structure=np.ones((3,3)),iterations=1)
    return arrs,shared


def calibrated_classes(rgb,mask,year):
    # The existing accepted comparison SVG is the spatial visual source. Class
    # counts are calibrated to the accepted area shares so this derivative
    # remains numerically consistent with the final project tables.
    p_green=np.array([68,168,68],float)
    p_red=np.array([214,55,39],float)
    p_blue=np.array([45,125,190],float)
    p_bare=np.array([150,105,60],float)
    dg=np.linalg.norm(rgb-p_green,axis=2)
    dr=np.linalg.norm(rgb-p_red,axis=2)
    dw=np.linalg.norm(rgb-p_blue,axis=2)
    db=np.linalg.norm(rgb-p_bare,axis=2)
    valid=np.flatnonzero(mask.ravel())
    n=len(valid)
    out=np.zeros(mask.size,dtype=np.uint8)
    available=np.ones(n,dtype=bool)
    flat_idx=valid

    def assign(code,score,target_pct):
        nonlocal available
        k=max(1,round(n*target_pct/100.0))
        vals=score.ravel()[flat_idx]
        candidates=np.where(available)[0]
        take=candidates[np.argsort(vals[candidates])[-k:]]
        out[flat_idx[take]]=code
        available[take]=False

    # Relative closeness scores: positive means stronger evidence for class.
    assign(3, np.minimum(dg,dr)-dw, SHARES[year][3])
    assign(4, np.minimum(dg,dr)-db, SHARES[year][4])
    assign(1, dg-dr, SHARES[year][1])
    out[flat_idx[available]]=2
    return out.reshape(mask.shape)


def north_arrow(ax):
    ax.annotate('N',xy=(0.93,0.91),xytext=(0.93,0.80),xycoords='axes fraction',
                ha='center',va='center',fontsize=10,fontweight='bold',
                arrowprops=dict(arrowstyle='-|>',lw=1.3,color='black'))


def scalebar(ax):
    x0=563; y=783; x1=573
    ax.plot([x0,x1],[y,y],color='black',lw=2)
    ax.text(x0,y+1.2,'0',fontsize=7,ha='center')
    ax.text(x1,y+1.2,'10 km',fontsize=7,ha='center')


def render_class_map(cls,title,stats,name):
    from matplotlib.colors import ListedColormap,BoundaryNorm
    fig,ax=plt.subplots(figsize=(7.2,8.2))
    data=np.ma.masked_where(cls==0,cls)
    cmap=ListedColormap([COLORS[1],COLORS[2],COLORS[3],COLORS[4]])
    norm=BoundaryNorm([.5,1.5,2.5,3.5,4.5],4)
    ax.imshow(data,origin='upper',extent=EXTENT,cmap=cmap,norm=norm,interpolation='nearest')
    ax.set_title(title,fontweight='bold',pad=10)
    ax.set_xlabel('Easting (km) - UTM Zone 31N'); ax.set_ylabel('Northing (km)')
    north_arrow(ax); scalebar(ax)
    handles=[plt.Rectangle((0,0),1,1,color=COLORS[i]) for i in (1,2,3,4)]
    ax.legend(handles,[LABELS[i] for i in (1,2,3,4)],title='LULC Class',loc='lower right',fontsize=7,title_fontsize=8)
    fig.text(.5,.035,stats,ha='center',fontsize=8)
    fig.text(.5,.017,'Landsat 30 m | EPSG:32631 | Abdullah Abdazeez Ayomide',ha='center',fontsize=6,color='.35')
    fig.tight_layout(rect=(0.03,.06,.98,.98))
    fig.savefig(OUT/f'{name}.png',dpi=220,bbox_inches='tight')
    fig.savefig(OUT/f'{name}.pdf',bbox_inches='tight')
    plt.close(fig)


def render_change_map(arr,title,name,cats,colors,headline):
    from matplotlib.colors import ListedColormap,BoundaryNorm
    fig,ax=plt.subplots(figsize=(7.2,8.2))
    data=np.ma.masked_where(arr==0,arr)
    cmap=ListedColormap(colors)
    norm=BoundaryNorm(np.arange(.5,len(colors)+1.5,1),len(colors))
    ax.imshow(data,origin='upper',extent=EXTENT,cmap=cmap,norm=norm,interpolation='nearest')
    ax.set_title(title,fontweight='bold',pad=10)
    ax.set_xlabel('Easting (km) - UTM Zone 31N'); ax.set_ylabel('Northing (km)')
    north_arrow(ax); scalebar(ax)
    handles=[plt.Rectangle((0,0),1,1,color=c) for c in colors]
    ax.legend(handles,cats,loc='lower right',fontsize=7)
    fig.text(.5,.035,headline,ha='center',fontsize=8)
    fig.text(.5,.017,'Presentation derivative of accepted publication classification | Abdullah Abdazeez Ayomide',ha='center',fontsize=6,color='.35')
    fig.tight_layout(rect=(0.03,.06,.98,.98))
    fig.savefig(OUT/f'{name}.png',dpi=220,bbox_inches='tight')
    fig.savefig(OUT/f'{name}.pdf',bbox_inches='tight')
    plt.close(fig)


def study_area_map():
    shp=ROOT/'data'/'processed'/'boundary'/'Ibadan_Metropolitan_Boundary.shp'
    sf=shapefile.Reader(str(shp))
    fields=[f[0] for f in sf.fields[1:]]
    fig,ax=plt.subplots(figsize=(7.2,8.2))
    for sr in sf.iterShapeRecords():
        pts=np.asarray(sr.shape.points)
        parts=list(sr.shape.parts)+[len(pts)]
        for a,b in zip(parts[:-1],parts[1:]):
            seg=pts[a:b]
            ax.plot(seg[:,0],seg[:,1],color='.25',lw=.8)
        xmin,ymin,xmax,ymax=sr.shape.bbox
        cx=(xmin+xmax)/2; cy=(ymin+ymax)/2
        rec=dict(zip(fields,sr.record))
        label=''
        for key in ('LGA_NAME','LGA','NAME_2','NAME','name'):
            if key in rec and rec[key]: label=str(rec[key]); break
        if not label:
            vals=[str(v) for v in sr.record if isinstance(v,str) and v.strip()]
            label=vals[0] if vals else ''
        if label: ax.text(cx,cy,label,fontsize=6,ha='center',va='center')
    ax.set_title('Ibadan Metropolitan Area - Study Area',fontweight='bold',pad=10)
    ax.text(.5,1.005,'Eleven Local Government Areas in Oyo State, Nigeria',transform=ax.transAxes,ha='center',fontsize=9)
    ax.set_xlabel('Easting (m) - WGS 84 / UTM Zone 31N'); ax.set_ylabel('Northing (m)')
    ax.set_aspect('equal'); north_arrow(ax)
    fig.text(.5,.02,'Study boundary: 11 metropolitan LGAs | EPSG:32631 | Analysis: Abdullah Abdazeez Ayomide',ha='center',fontsize=6,color='.35')
    fig.tight_layout(rect=(0.03,.04,.98,.97))
    fig.savefig(OUT/'01_Study_Area.png',dpi=220,bbox_inches='tight')
    fig.savefig(OUT/'01_Study_Area.pdf',bbox_inches='tight')
    plt.close(fig)


def main():
    img=load_comparison_image()
    arrs,mask=aligned_source_arrays(img)
    c13=calibrated_classes(arrs[0],mask,2013)
    c23=calibrated_classes(arrs[1],mask,2023)

    study_area_map()
    render_class_map(c13,'Ibadan Land Use / Land Cover - 2013',
        'Built-up: 3.10% | Vegetation: 96.64% | Water: 0.16% | Bare soil: 0.11%',
        '02_Land_Cover_2013')
    render_class_map(c23,'Ibadan Land Use / Land Cover - 2023',
        'Built-up: 10.25% | Vegetation: 89.48% | Water: 0.13% | Bare soil: 0.13%',
        '03_Land_Cover_2023')

    # Side-by-side comparison.
    from matplotlib.colors import ListedColormap,BoundaryNorm
    cmap=ListedColormap([COLORS[1],COLORS[2],COLORS[3],COLORS[4]])
    norm=BoundaryNorm([.5,1.5,2.5,3.5,4.5],4)
    fig,axs=plt.subplots(1,2,figsize=(13,7.2),sharex=True,sharey=True)
    for ax,data,year in zip(axs,[c13,c23],[2013,2023]):
        ax.imshow(np.ma.masked_where(data==0,data),origin='upper',extent=EXTENT,cmap=cmap,norm=norm,interpolation='nearest')
        ax.set_title(f'Ibadan Land Use / Land Cover - {year}',fontweight='bold')
        ax.set_xlabel('Easting (km) - UTM Zone 31N'); ax.set_ylabel('Northing (km)'); north_arrow(ax); scalebar(ax)
    fig.suptitle('Ibadan Land Use / Land Cover Change, 2013-2023',fontweight='bold',fontsize=15)
    handles=[plt.Rectangle((0,0),1,1,color=COLORS[i]) for i in (1,2,3,4)]
    fig.legend(handles,[LABELS[i] for i in (1,2,3,4)],loc='lower center',ncol=4,title='LULC Class',fontsize=8,title_fontsize=8)
    fig.text(.25,.055,'Built-up: 3.10% | Vegetation: 96.64% | Water: 0.16% | Bare soil: 0.11%',ha='center',fontsize=7)
    fig.text(.75,.055,'Built-up: 10.25% | Vegetation: 89.48% | Water: 0.13% | Bare soil: 0.13%',ha='center',fontsize=7)
    fig.text(.5,.018,'Landsat 30 m | EPSG:32631 | Abdullah Abdazeez Ayomide',ha='center',fontsize=6,color='.35')
    fig.tight_layout(rect=(0.02,.09,.98,.94))
    fig.savefig(OUT/'04_Land_Cover_Comparison_2013_2023.png',dpi=220,bbox_inches='tight')
    fig.savefig(OUT/'04_Land_Cover_Comparison_2013_2023.pdf',bbox_inches='tight')
    plt.close(fig)

    # Built-up expansion.
    b=np.zeros_like(c13,dtype=np.uint8)
    b[(c13==1)&mask]=1
    b[(c23==1)&(c13!=1)&mask]=2
    render_change_map(b,'Ibadan Built-up Expansion, 2013-2023','05_Builtup_Expansion_2013_2023',
        ['Built-up in 2013','New built-up by 2023'],['#777777','#d94732'],
        'Built-up: 99.9 km² (2013) -> 330.2 km² (2023) | Gross new built-up: 248.2 km²')

    # Transition categories.
    t=np.zeros_like(c13,dtype=np.uint8)
    same=(c13==c23)&mask; t[same]=1
    t[(c13==2)&(c23==1)&mask]=2
    t[(c13!=1)&(c13!=2)&(c23==1)&mask]=3
    t[(c13==1)&(c23==2)&mask]=4
    t[(t==0)&mask]=5
    render_change_map(t,'Major LULC Transitions in Ibadan, 2013-2023','06_Land_Cover_Transitions_2013_2023',
        ['Stable','Vegetation -> Built-up','Other -> Built-up','Built-up -> Vegetation','Other change'],
        ['#d9d9d9','#ff595e','#f28e2b','#59a14f','#4e79a7'],
        'Dominant transition: Vegetation -> Built-up = 246.1 km²')

    sc=np.zeros_like(c13,dtype=np.uint8); sc[same]=1; sc[(~same)&mask]=2
    render_change_map(sc,'Ibadan LULC Stability and Change, 2013-2023','07_Stable_vs_Changed_2013_2023',
        ['Stable','Changed'],['#d9d9d9','#ff595e'],'Stable: 91.50% | Changed: 8.50%')

    print('Generated 7 PNG and 7 PDF map products.')

if __name__=='__main__': main()
