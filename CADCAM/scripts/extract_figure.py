#!/usr/bin/env python3
"""Crop a lecture PDF page, preserving vectors. Box: left,top,right,bottom fractions.
Example: python extract_figure.py --source SOURCE --page 11 --box .1 .2 .9 .85 --output img/ch06-triangulation.pdf
"""
import argparse, copy, json
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--source',required=True,type=Path)
p.add_argument('--page',required=True,type=int)
p.add_argument('--box',nargs=4,type=float,default=[0,0,1,1])
p.add_argument('--output',required=True,type=Path)
a=p.parse_args()
page=copy.deepcopy(PdfReader(a.source).pages[a.page-1])
page.transfer_rotation_to_content()
l,t,r,b=a.box
if not (0<=l<r<=1 and 0<=t<b<=1):raise ValueError('invalid normalized crop')
x0,y0,x1,y1=map(float,page.mediabox)
w,h=x1-x0,y1-y0
box=RectangleObject((x0+l*w,y0+(1-b)*h,x0+r*w,y0+(1-t)*h))
page.mediabox=box
page.cropbox=box
page.trimbox=box
page.bleedbox=box
page.artbox=box
writer=PdfWriter();writer.add_page(page)
writer.add_metadata({'/Title':f'{a.source.stem}, PDF p.{a.page}', '/Subject':f'Normalized crop {a.box}'})
a.output.parent.mkdir(parents=True,exist_ok=True)
with a.output.open('wb') as f:writer.write(f)
record={'source':a.source.name,'page':a.page,'box':a.box,'output':a.output.name}
manifest=a.output.with_suffix('.source.json')
manifest.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(a.output)
