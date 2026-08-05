from pathlib import Path
import json, sys
import pandas as pd
import numpy as np
import rasterio

ROOT=Path(__file__).resolve().parents[1]
fail=[]
required=['README.md','LICENSE','CITATION.cff','project.json','assets/project-cover.png',
'data/processed/rasters/Ibadan_Final_LULC_2013.tif','data/processed/rasters/Ibadan_Final_LULC_2023.tif',
'outputs/tables/lulc_area_change_summary.csv','scripts/gee/ibadan_lulc_final_gee_script.js']
for p in required:
    if not (ROOT/p).exists(): fail.append(f'Missing: {p}')
for name in ['Ibadan_Final_LULC_2013.tif','Ibadan_Final_LULC_2023.tif']:
    p=ROOT/'data/processed/rasters'/name
    if p.exists():
        with rasterio.open(p) as ds:
            if ds.crs.to_epsg()!=32631: fail.append(f'{name}: CRS is not EPSG:32631')
            if tuple(round(v,6) for v in ds.res)!=(30.0,30.0): fail.append(f'{name}: resolution is not 30 m')
            if not set(np.unique(ds.read(1))).issubset({0,1,2,3,4}): fail.append(f'{name}: unexpected class values')
s=ROOT/'outputs/tables/lulc_area_change_summary.csv'
if s.exists():
    df=pd.read_csv(s)
    b=float(df.loc[df.class_name=='Built-up','net_change_sqkm'].iloc[0])
    if abs(b-679.641195)>0.01: fail.append('Built-up change does not match final statistics')
for p in ROOT.rglob('*'):
    if p.is_file() and p.stat().st_size>95*1024*1024: fail.append(f'Large file: {p.relative_to(ROOT)}')
if fail:
    print('VALIDATION FAILED'); [print('-',x) for x in fail]; sys.exit(1)
print('VALIDATION PASSED')
print('Repository structure, key statistics, raster classes, CRS, resolution, and file sizes are valid.')
