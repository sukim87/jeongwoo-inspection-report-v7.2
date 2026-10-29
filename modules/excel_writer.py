from io import BytesIO
from pathlib import Path
import re,tempfile
from openpyxl import load_workbook
from openpyxl.drawing.image import Image as XLImage
from PIL import Image,ImageOps
T=Path(__file__).resolve().parents[1]/'templates'/'검사결과서.xlsx'
S=[('검사결과서','A21'),('검사결과서','G21'),('검사결과서(을지)','A11'),('검사결과서(을지)','G11'),('검사결과서(을지)','A24'),('검사결과서(을지)','G24'),('검사결과서(을지)','A37'),('검사결과서(을지)','G37')]
def safe(v):return re.sub(r'[\\/:*?"<>|]+','-',str(v)).strip()
def build_report(d,photos,rots):
 wb=load_workbook(T);q=wb['간편입력'];m=wb['검사결과서'];e=wb['검사결과서(을지)']
 q['A21']='검사장소 / Inspection Location';q['B21']=d.get('inspection_location','')
 for c,v in {'B5':d['customer'],'B6':d['part_name'],'B7':d['order_no'],'B8':d['po_step_no'],'B9':d['date'],'B10':d['types'],'B11':d['spec'],'B14':d['inspection_result'],'B15':d['judgment'],'B16':'','B17':d['result'],'B18':d['action'],'B19':d['caption'],'B20':d['inspector']}.items():q[c]=v
 for c,v in {'J3':d['doc'],'C5':d['customer'],'I5':d['types'],'C6':d['part_name'],'I6':d['po_step_no'],'C7':d['order_no'],'I7':d['date'],'A11':d['spec'],'F11':d['inspection_result'],'J11':d['judgment'],'C13':d['result'],'C16':d['action'],'A33':d['caption'],'A37':d['inspector'],'J37':d['judgment']}.items():m[c]=v
 for c,v in {'J3':d['doc'],'C5':d['customer'],'I5':d['types'],'C6':d['part_name'],'I6':d['po_step_no'],'C7':d['order_no'],'I7':d['date']}.items():e[c]=v
 for ws in (m,e):ws._images=[]
 for c in ('A21','G21'):m[c]=''
 for c in ('A11','G11','A24','G24','A37','G37'):e[c]=''
 with tempfile.TemporaryDirectory() as td:
  for i,u in enumerate(photos[:8]):
   u.seek(0);im=ImageOps.exif_transpose(Image.open(u)).convert('RGB');deg=rots[i] if i<len(rots) else 0
   if deg:im=im.rotate(-deg,expand=True)
   im=ImageOps.fit(im,(1406,1000),Image.Resampling.LANCZOS);p=f'{td}/{i}.jpg';im.save(p,quality=91);x=XLImage(p);x.width=405;x.height=288;wb[S[i][0]].add_image(x,S[i][1])
  o=BytesIO();wb.save(o)
 return o.getvalue(),f"{safe(d['doc'])}.xlsx"
