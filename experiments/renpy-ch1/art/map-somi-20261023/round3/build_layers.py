"""Reproduce requested crops and previews from the generated map; no game writes."""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops

ROOT = Path(__file__).resolve().parent
SIZE = (2304, 1344)
SOURCE = Image.open(ROOT / 'generated-map.png').convert('RGB')
SX, SY = SIZE[0] / SOURCE.width, SIZE[1] / SOURCE.height
def xy(p): return [round(p[0]*SX), round(p[1]*SY)]
# Coordinates authored by inspection of the generated 1642 x 958 sheet.
# Each polygon encloses its own drawing and immediate yard, excluding ink labels.
SPECS = {
 'inn': ([(86,478),(198,412),(373,401),(516,467),(554,552),(538,578),(452,592),(304,581),(153,562),(90,531)], (327,505), (366,595), (335,577,63,31)),
 'clinic': ([(260,309),(315,267),(405,237),(459,277),(516,290),(532,331),(487,347),(375,347),(365,374),(287,354)], (398,300), (429,360), (387,341,84,33)),
 'school': ([(474,139),(538,105),(604,104),(645,77),(725,78),(752,124),(805,124),(849,155),(844,181),(760,199),(703,187),(601,191),(488,172)], (669,144), (687,204), (656,190,58,29)),
 'post': ([(750,544),(800,536),(834,499),(885,494),(929,538),(929,568),(985,574),(993,595),(957,612),(912,585),(853,596),(819,615),(759,599)], (864,551), (901,604), (865,587,75,30)),
 'workshop': ([(930,405),(975,386),(1045,340),(1074,344),(1076,356),(1113,351),(1139,397),(1173,413),(1180,462),(1120,476),(1021,471),(948,468)], (1056,426), (1080,491), (1041,476,81,31)),
 'store': ([(1227,428),(1265,394),(1302,367),(1417,378),(1458,411),(1499,439),(1518,478),(1490,511),(1414,510),(1285,497),(1222,479)], (1363,450), (1379,526), (1316,508,128,32)),
 'market': ([(657,265),(699,241),(773,243),(778,268),(807,247),(859,254),(876,284),(907,265),(953,284),(978,340),(939,354),(878,333),(844,317),(796,319),(779,299),(711,318),(656,306)], (815,283), (782,334), (752,316,61,35)),
 'square': ([(669,415),(708,394),(712,375),(748,350),(772,354),(797,379),(790,413),(831,427),(829,447),(778,464),(722,459),(676,447)], (753,416), (752,479), (725,463,59,31)),
 'gate': ([(520,611),(535,592),(552,610),(552,626),(627,627),(635,595),(656,595),(663,628),(702,616),(708,592),(731,594),(742,627),(818,639),(827,665),(769,670),(766,697),(783,770),(752,786),(703,778),(684,727),(665,680),(654,674),(535,668),(519,647)], (685,651), (579,687), (531,670,99,30)),
 'forest': ([(0,40),(45,16),(98,23),(120,2),(253,0),(281,41),(366,18),(418,48),(478,46),(503,98),(483,139),(451,192),(395,199),(371,174),(319,182),(299,160),(254,172),(219,194),(210,221),(186,246),(124,267),(75,292),(0,282)], (236,119), (237,124), (193,105,88,34)),
 'somi': ([(1207,807),(1252,791),(1293,762),(1365,757),(1398,761),(1421,800),(1496,798),(1510,822),(1503,845),(1444,870),(1390,854),(1315,855),(1234,839),(1209,837)], (1337,813), (1352,877), (1312,858,82,32)),
 'laundry': ([(853,779),(883,766),(921,767),(944,781),(969,777),(970,761),(1043,746),(1054,776),(1038,797),(1058,805),(1054,829),(1015,840),(986,830),(961,831),(946,839),(928,823),(901,819),(880,798)], (948,798), (956,849), (917,833,80,29)),
 'river': ([(1170,57),(1246,60),(1308,82),(1392,116),(1467,155),(1540,180),(1595,206),(1641,219),(1641,589),(1606,613),(1568,644),(1508,674),(1452,706),(1392,718),(1344,727),(1307,739),(1274,724),(1233,750),(1180,749),(1137,766),(1096,768),(1051,782),(1045,758),(968,773),(933,774),(904,766),(870,781),(833,774),(798,790),(782,787),(767,755),(752,705),(723,670),(700,675),(716,732),(723,776),(691,792),(646,803),(600,829),(546,840),(494,847),(442,865),(384,876),(333,867),(277,885),(230,878),(172,896),(110,907),(48,906),(0,922),(0,805),(59,799),(118,783),(178,770),(245,767),(304,752),(365,750),(423,735),(489,736),(550,726),(603,715),(658,709),(677,698),(672,688),(735,696),(798,692),(868,679),(932,674),(992,661),(1062,642),(1129,633),(1196,618),(1261,610),(1324,598),(1394,578),(1452,563),(1512,543),(1555,518),(1590,486),(1609,456),(1587,428),(1585,401),(1549,376),(1559,353),(1528,332),(1515,308),(1474,290),(1452,266),(1405,252),(1395,228),(1354,215),(1316,207),(1293,185),(1250,176),(1221,151),(1182,142),(1161,118),(1169,97),(1170,57)], (1395,654), (1446,649), (1409,629,72,37)),
}

def build():
 art = SOURCE.resize(SIZE, Image.Resampling.LANCZOS).convert('RGBA')
 art.save(ROOT/'room13-map-village.webp', lossless=True, method=6)
 art.save(ROOT/'preview_full.png')
 (ROOT/'nodes').mkdir(exist_ok=True)
 nodes = {}
 masks = {}
 for key, (poly, point, label, lb) in SPECS.items():
  polygon = [xy(p) for p in poly]
  xs, ys = zip(*polygon)
  x,y = min(xs)-3, min(ys)-3
  x,y = max(0,x),max(0,y)
  right,bottom = min(SIZE[0],max(xs)+4), min(SIZE[1],max(ys)+4)
  w,h = right-x,bottom-y
  local = [(a-x,b-y) for a,b in polygon]
  mask = Image.new('L',(w,h)); ImageDraw.Draw(mask).polygon(local,fill=255)
  cut = art.crop((x,y,right,bottom)); cut.putalpha(mask)
  line = Image.new('RGBA',(w,h)); ImageDraw.Draw(line).line(local+[local[0]], fill=(255,248,228,255),width=2,joint='curve')
  for suffix,im in [('',cut),('-outline',line)]:
   im.save(ROOT/'nodes'/f'room13-map-village-{key}{suffix}.webp',lossless=True,method=6)
  nodes[key] = dict(polygon=polygon,point=xy(point),label_point=xy(label),bounds=[x,y,w,h],label_bounds=xy(lb[:2])+xy(lb[2:]))
  masks[key] = (mask,line)
 data = dict(size=list(SIZE),nodes=nodes)
 (ROOT/'cartography_v2.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 scale=1248/1672
 views = {'village':(0,0),'somi':(round(SIZE[0]*scale)-1280,round(SIZE[1]*scale)-720)}
 for view,origin in views.items():
  shown=art.copy()
  if view=='somi':
   x,y,w,h=nodes['somi']['bounds']
   patch=shown.crop((x,y,x+w,y+h))
   bright=patch.point(lambda v:min(255,v+round(.09*255)))
   bright.putalpha(masks['somi'][0]); shown.alpha_composite(bright,(x,y))
  for key,node in nodes.items():
   line=masks[key][1]
   selected=view=='somi' and key=='somi'
   color='#694425' if selected else '#a18b6c'
   tint=Image.new('RGBA',line.size,color)
   tint.putalpha(line.getchannel('A') if selected else line.getchannel('A').point(lambda a:round(a*.85)))
   shown.alpha_composite(tint,tuple(node['bounds'][:2]))
  shown=shown.resize((round(SIZE[0]*scale),round(SIZE[1]*scale)),Image.Resampling.LANCZOS)
  x,y=origin
  shown.crop((x,y,x+1280,y+720)).convert('RGB').save(ROOT/f'preview_view_{view}.png')
 (ROOT/'preview_views.json').write_text(json.dumps(dict(scale=scale,size=[1280,720],origins=views),indent=2)+'\n')
 # Mechanical contract checks, including exact alpha/polygon correspondence.
 assert set(nodes)==set('inn clinic school post workshop store market square gate river forest somi laundry'.split())
 for key,node in nodes.items():
  x,y,w,h=node['bounds']
  for suffix in ('','-outline'):
   im=Image.open(ROOT/'nodes'/f'room13-map-village-{key}{suffix}.webp')
   assert im.mode=='RGBA' and im.size==(w,h)
  im=Image.open(ROOT/'nodes'/f'room13-map-village-{key}.webp')
  assert ImageChops.difference(im.getchannel('A'),masks[key][0]).getbbox() is None
  assert 0<=x<x+w<=SIZE[0] and 0<=y<y+h<=SIZE[1]
  px,py=node['point']; assert masks[key][0].getpixel((px-x,py-y))==255,key
 print('PASS: 13 nodes / 26 RGBA WebPs / bounds / alpha polygons / point inclusion / 3 previews')

if __name__=='__main__': build()
