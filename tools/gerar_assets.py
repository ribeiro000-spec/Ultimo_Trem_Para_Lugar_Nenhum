"""Gera as texturas do jogo (pixel art procedural). Rode: python3 tools/gerar_assets.py
Substitua qualquer PNG por arte desenhada à mão mantendo nome e tamanho."""
import numpy as np, random, os
from PIL import Image, ImageDraw
W,H=128,64
OUT=os.path.join(os.path.dirname(__file__),'..','assets')
hx=lambda h:tuple(int(h[i:i+2],16) for i in (1,3,5))
M=Image.new('L',(W,H),0);ImageDraw.Draw(M).polygon([(W/2,0),(W-1,H/2),(W/2,H-1),(0,H/2)],fill=255)
def lite(c,k):return tuple(max(0,min(255,int(v*k))) for v in c)
def tile(base,alt,detail,seed,v):
    r=random.Random(seed*31+v);b=hx(alt if v else base)
    a=np.zeros((H,W,3))+np.array(b);n=np.random.RandomState(seed*13+v).randint(-12,13,(H//2,W//2))
    a+=np.kron(n,np.ones((2,2)))[:,:,None];im=Image.fromarray(np.clip(a,0,255).astype('uint8'));d=ImageDraw.Draw(im);detail(d,r,b,v)
    ov=Image.new('RGBA',(W,H),(0,0,0,0));o=ImageDraw.Draw(ov)
    o.line([(0,H/2),(W/2,0),(W,H/2)],fill=(255,255,255,50),width=2);o.line([(0,H/2),(W/2,H-1),(W,H/2)],fill=(0,0,0,110),width=2)
    out=im.convert('RGBA');out=Image.alpha_composite(out,ov);out.putalpha(M);return out
def sheet(path,base,alt,detail,seed):
    s=Image.new('RGBA',(W*2,H),(0,0,0,0))
    for v in(0,1):s.paste(tile(base,alt,detail,seed,v),(v*W,0))
    s.save(path)
def pts(r,n,m=14):return[(r.randint(m,W-m),r.randint(m,H-m)) for _ in range(n)]
def water(d,r,b,v):
    for x,y in pts(r,5):d.ellipse([x-12,y-4,x+12,y+4],outline=lite(b,1.6),width=1)
    for x,y in pts(r,6):d.line([x,y,x+10,y],fill=lite(b,.7))
def jungle(d,r,b,v):
    for x,y in pts(r,9):d.ellipse([x-6,y-3,x+6,y+3],fill=lite((40,120,50),r.uniform(.6,1.1)))
    for x,y in pts(r,10):d.line([x,y,x+r.randint(-2,2),y-r.randint(3,7)],fill=(70,170,80))
def desert(d,r,b,v):
    for x,y in pts(r,40):d.point((x,y),fill=lite(b,1.3))
    for x,y in pts(r,4):d.arc([x-18,y-5,x+18,y+9],200,340,fill=lite(b,.75))
def cave(d,r,b,v):
    for x,y in pts(r,6):d.polygon([(x,y),(x+9,y+2),(x+6,y+8),(x-3,y+6)],fill=lite(b,.7),outline=lite(b,1.3))
    x,y=pts(r,1)[0];d.line([x,y,x+14,y+5,x+22,y+3],fill=lite(b,.4),width=2)
def clock(d,r,b,v):
    g=(217,176,74);d.polygon([(64,10),(116,32),(64,54),(12,32)],outline=g);d.line([64,10,64,54],fill=lite(g,.6));d.line([12,32,116,32],fill=lite(g,.6))
    for x,y in pts(r,6):d.point((x,y),fill=g)
def snow(d,r,b,v):
    for x,y in pts(r,8):d.ellipse([x-9,y-3,x+9,y+3],fill=(244,251,255))
    for x,y in pts(r,6):d.ellipse([x-6,y-2,x+6,y+2],fill=(150,185,215))
def lab(d,r,b,v):
    t=(110,240,176)
    for k in range(-3,4):d.line([64+k*18,0,64+k*18+0,64],fill=lite(b,1.4))
    d.polygon([(64,18),(92,32),(64,46),(36,32)],outline=t);d.ellipse([60,28,68,36],fill=t)
def metal(d,r,b,v):
    for x,y in((30,32),(98,32),(64,14),(64,50)):d.ellipse([x-2,y-2,x+2,y+2],fill=lite(b,1.7))
    d.line([20,32,108,32],fill=lite(b,.6))
def planks(d,r,b,v):
    for y in range(8,64,10):d.line([0,y,W,y],fill=lite(b,.6),width=2)
    for y in range(8,64,10):d.line([r.randint(20,100),y,r.randint(20,100),y+10],fill=lite(b,.7))
def tech(d,r,b,v):
    d.line([20,32,108,32],fill=lite(b,1.7),width=2);d.line([64,12,64,52],fill=lite(b,.6))
def grate(d,r,b,v):
    for k in range(0,128,8):d.line([k,0,k-30,64],fill=lite(b,.55))
    for k in range(0,128,8):d.line([k,0,k+30,64],fill=lite(b,.55))
def hazard(d,r,b,v):
    for k in range(-64,128,16):d.polygon([(k,40),(k+8,40),(k+24,64),(k+16,64)],fill=(210,170,40))
    metal(d,r,b,v)
TC=[('#1d3d3b','#183331',tech),('#4a3626','#40301f',planks),('#1f3050','#192742',metal),('#3d3229','#342a21',grate),('#3c2531','#331f29',hazard)]
for i,(a,b,f) in enumerate(TC):sheet(f'{OUT}/tiles/vagao{i}.png',a,b,f,i)
TP=[('#2a3d44','#233840',water),('#2f4a2a','#274022',jungle),('#7a6540','#6d5a38',desert),('#3a3a42','#2f2f37',cave),('#3a3040','#2f2736',clock),('#8aa0b0','#7c93a4',snow),('#34444a','#2d3b41',lab)]
for i,(a,b,f) in enumerate(TP):sheet(f'{OUT}/tiles/plataforma{i}.png',a,b,f,50+i)
WL=['#1f4f49','#5c4030','#24426e','#50402f','#4d2b3d']
for i,c in enumerate(WL):
    w,h=512,192;b=np.array(hx(c),float);g=np.linspace(1.2,.6,h)[:,None,None];a=np.zeros((h,w,3))+b*g
    a+=np.kron(np.random.RandomState(i).randint(-9,10,(h//2,w//2)),np.ones((2,2)))[:,:,None]
    im=Image.fromarray(np.clip(a,0,255).astype('uint8'));d=ImageDraw.Draw(im);dk=lite(hx(c),.4);lt=lite(hx(c),1.5)
    for x in range(0,w,64):d.line([x,0,x,h],fill=dk,width=2);d.line([x+2,0,x+2,h],fill=lt)
    d.rectangle([0,int(h*.74),w,h],fill=lite(hx(c),.5));d.line([0,int(h*.74),w,int(h*.74)],fill=lt,width=2)
    for x in range(8,w,32):d.ellipse([x,10,x+3,13],fill=lt)
    im.save(f'{OUT}/walls/vagao{i}.png')
print('ok')
