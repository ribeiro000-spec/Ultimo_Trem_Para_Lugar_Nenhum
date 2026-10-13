"""Gera sprites de móveis, cenário e personagens (camadas). Rode: python3 tools/gerar_sprites.py"""
import os,numpy as np
from PIL import Image,ImageDraw
O=os.path.join(os.path.dirname(__file__),'..','assets')
hx=lambda h:tuple(int(h[i:i+2],16) for i in(1,3,5))
def sh(c,f):c=hx(c) if isinstance(c,str) else c[:3];return tuple(max(0,min(255,int(v*f))) for v in c)+(255,)
class S:
  def __init__(s,w,d,h):
    s.w,s.d,s.h=w,d,h;s.im=Image.new('RGBA',(int((w+d)*64)+8,int((w+d)*32+h*60)+8),(0,0,0,0));s.g=ImageDraw.Draw(s.im);s.ox=int(d*64)+4;s.oy=int(h*60)+4
    s.poly([(-.1,-.1,0),(w+.1,-.1,0),(w+.1,d+.1,0),(-.1,d+.1,0)],(0,0,0,90),0)
  def P(s,x,y,z=0):return(s.ox+(x-y)*64,s.oy+(x+y)*32-z*60)
  def poly(s,pts,c,o=1):s.g.polygon([s.P(*p) for p in pts],fill=c,outline=sh(c,.4) if o else None)
  def box(s,x,y,z,w,d,h,c):
    s.poly([(x,y+d,z),(x+w,y+d,z),(x+w,y+d,z+h),(x,y+d,z+h)],sh(c,.8));s.poly([(x+w,y,z),(x+w,y+d,z),(x+w,y+d,z+h),(x+w,y,z+h)],sh(c,.55));s.poly([(x,y,z+h),(x+w,y,z+h),(x+w,y+d,z+h),(x,y+d,z+h)],sh(c,1.2))
  def fl(s,x0,x1,z0,z1,c):s.poly([(x0,s.d,z0),(x1,s.d,z0),(x1,s.d,z1),(x0,s.d,z1)],sh(c,1),0)
  def fr(s,y0,y1,z0,z1,c):s.poly([(s.w,y0,z0),(s.w,y1,z0),(s.w,y1,z1),(s.w,y0,z1)],sh(c,1),0)
  def save(s,n):
    a=np.array(s.im).astype(int);nz=np.random.RandomState(7).randint(-9,10,a.shape[:2])[:,:,None];a[:,:,:3]=np.clip(a[:,:,:3]+nz*(a[:,:,3:]>200),0,255);Image.fromarray(a.astype('uint8')).save(f'{O}/props/{n}.png')
def mk(n,w,d,h,fn):s=S(w,d,h);fn(s);s.save(n)
def sofa(c):
  def f(s):s.box(0,0,0,2,1,.5,c);s.box(0,0,.5,2,.28,.55,c);s.box(0,.28,.5,.25,.72,.3,c);s.box(1.75,.28,.5,.25,.72,.3,c);s.box(.3,.3,.5,.7,.68,.13,sh(c,1.3));s.box(1,.3,.5,.7,.68,.13,sh(c,1.3));s.fl(.3,1.7,.08,.12,sh(c,.6))
  return f
for i,c in enumerate(['#8a3e55','#2f6a8a','#7a5a2a']):mk(f'sofa{i}',2,1,1.05,sofa(c))
def crate(s):s.box(0,0,0,1,1,.9,'#9a6a35');[s.fl(0,1,z,z+.05,'#3a2812') for z in(.28,.6)];s.fl(.45,.55,0,.9,'#3a2812');s.fr(.45,.55,0,.9,'#3a2812')
mk('crate',1,1,.9,crate)
def gen(s):
  s.box(0,0,0,1.6,1,1.5,'#3a5066');s.box(.2,.2,1.5,1.2,.6,.1,'#16242e');s.box(1.2,.2,1.6,.25,.25,.6,'#8a98a6');s.fl(.2,1.4,.3,1.2,(61,255,160,255));[s.fl(.2+k*.2,.23+k*.2,.3,1.2,'#0a2a1c') for k in range(6)];s.fr(.2,.8,.4,1,(255,180,60,255))
mk('gen',1.6,1,1.8,gen)
def vend(s):
  s.box(0,0,0,1,.8,2,'#2a468a');s.fl(.1,.9,.5,1.85,'#0a1c3a');[s.fl(.15+q*.25,.33+q*.25,.6+r*.4,.85+r*.4,['#ff5c5c','#ffd24a','#4ad2ff','#6ef08a'][(r+q)%4]) for r in range(3) for q in range(3)];s.fl(.1,.9,1.88,1.98,(110,220,255,255));s.fr(.2,.6,.9,1.1,'#ffd24a')
mk('vend',1,.8,2,vend)
def locker(s):
  s.box(0,0,0,.9,.7,1.9,'#566676');s.fl(.1,.8,.2,1.7,'#3c4a58');[s.fl(.2,.7,1.3+k*.09,1.33+k*.09,'#10161c') for k in range(4)];s.fl(.68,.74,.9,1.1,'#cfd6dc');s.fl(.3,.6,1.5,1.6,'#e8c23a')
mk('locker',.9,.7,1.9,locker)
def plant(s):
  s.box(.05,.05,0,.5,.5,.4,'#9a5a35');x,y=s.P(.3,.3,.7)
  for a,b,r,c in((-16,-26,22,'#2e9a4a'),(16,-30,20,'#3dbb5c'),(0,-52,22,'#58d878'),(-4,-16,18,'#2e9a4a'),(8,-44,10,'#8af0a0')):s.g.ellipse([x+a-r,y+b-r,x+a+r,y+b+r],fill=hx(c),outline=sh(c,.5))
mk('plant',.6,.6,1.1,plant)
def lamp(s):
  s.box(.05,.05,0,.3,.3,.1,'#222d38');s.box(.17,.17,.1,.06,.06,1.3,'#7a8a98');x,y=s.P(.2,.2,1.55);s.g.polygon([(x-20,y+8),(x+20,y+8),(x+10,y-18),(x-10,y-18)],fill=(255,216,138,255),outline=(120,90,40,255));s.g.ellipse([x-12,y+4,x+12,y+13],fill=(255,246,208,255))
mk('lamp',.4,.4,1.8,lamp)
def shelf(s):
  s.box(0,0,0,1.3,.6,1.9,'#4a3322')
  for r in range(3):
    s.fl(.05,1.25,.25+r*.55,.8+r*.55,'#1a120c')
    for k in range(7):e=.32+(k%3)*.05;s.fl(.1+k*.16,.22+k*.16,.28+r*.55,.28+r*.55+e,['#c0504a','#4a8ac0','#d9b04a','#5aa070','#9a6ac0','#c07a3a'][(k+r)%6])
mk('shelf',1.3,.6,1.9,shelf)
def barrel(s):s.box(0,0,0,.7,.7,.9,'#6b3b2b');[(s.fl(0,.7,z,z+.07,'#2a1a14'),s.fr(0,.7,z,z+.07,'#2a1a14')) for z in(.22,.6)];s.poly([(.1,.1,.9),(.6,.1,.9),(.6,.6,.9),(.1,.6,.9)],(60,220,130,255),0)
mk('barrel',.7,.7,.9,barrel)
def bench(s):s.box(.1,.1,0,.12,.5,.35,'#2a2a30');s.box(1.78,.1,0,.12,.5,.35,'#2a2a30');s.box(0,.05,.35,2,.6,.15,'#7a5a3a');s.box(0,.05,.5,2,.1,.4,'#6a4a2a')
mk('bench',2,.7,.95,bench)
def table(s):
  for a,b in((0,0),(1.28,0),(0,.78),(1.28,.78)):s.box(a,b,0,.12,.12,.6,'#3a2a1c')
  s.box(0,0,.6,1.4,.9,.12,'#7a5233');s.box(.6,.35,.72,.2,.2,.3,'#d8e6f0');x,y=s.P(.7,.45,1.05);s.g.ellipse([x-14,y-8,x+14,y+8],fill=(255,210,120,150))
mk('table',1.4,.9,1.2,table)
def pillar(s):s.box(0,0,0,.6,.6,2.2,'#34424f');s.box(0,0,1.9,.6,.6,.3,'#1b2530');s.fl(.1,.5,.2,.5,'#1b2530');x,y=s.P(.3,.3,2.3);s.g.ellipse([x-10,y-6,x+10,y+6],fill=(255,210,140,255))
mk('pillar',.6,.6,2.5,pillar)
def tree(s):
  s.box(.3,.3,0,.3,.3,1.1,'#5a3a22');x,y=s.P(.45,.45,1.1)
  for a,b,r,c in((0,-60,36,'#2e7a3a'),(-26,-36,26,'#3d9a4a'),(24,-40,26,'#2a6a34'),(0,-78,22,'#58b868')):s.g.ellipse([x+a-r,y+b-r,x+a+r,y+b+r],fill=hx(c),outline=sh(c,.5))
mk('tree',.9,.9,2.3,tree)
def cactus(s):s.box(.3,.3,0,.3,.3,1.4,'#3f8a4a');s.box(.05,.3,.6,.25,.25,.3,'#3f8a4a');s.box(.05,.3,.6,.1,.25,.7,'#3f8a4a');s.box(.6,.35,.8,.25,.25,.3,'#3f8a4a');s.box(.75,.35,.8,.1,.25,.5,'#3f8a4a')
mk('cactus',.9,.9,1.5,cactus)
def gear(s):
  x,y=s.P(.45,.45,.6);s.g.ellipse([x-30,y-60,x+30,y],fill=(60,48,30,255),outline=(217,176,74,255),width=5)
  for k in range(12):a=k*np.pi/6;s.g.line([x+np.cos(a)*30,y-30+np.sin(a)*30,x+np.cos(a)*40,y-30+np.sin(a)*40],fill=(217,176,74,255),width=7)
  s.g.ellipse([x-8,y-38,x+8,y-22],fill=(217,176,74,255))
mk('gear',.9,.9,1.4,gear)
TH=[('#4a5a60','#6ab8d0'),('#5a6a50','#6fe08a'),('#b89860','#ffc070'),('#55555e','#ff9a3d'),('#5a4a60','#d9b04a'),('#dfeaf2','#cfeaff'),('#566a70','#6ef0b0')]
for i,(rk,tn) in enumerate(TH):
  def rock(s,rk=rk):s.box(0,.05,0,.9,.8,.4,rk);s.box(.15,.15,.4,.6,.55,.25,sh(rk,1.1));s.box(.5,.1,.4,.3,.3,.15,sh(rk,.9))
  mk(f'rock{i}',.9,.9,.8,rock)
  def crystal(s,tn=tn):
    x,y=s.P(.45,.45,0)
    for a,h,c in((-22,70,1),(4,100,1.2),(26,56,.75)):s.g.polygon([(x+a-16,y),(x+a,y-h),(x+a+16,y)],fill=sh(tn,c),outline=sh(tn,.4));s.g.line([x+a,y-h,x+a,y],fill=sh(tn,1.5))
  mk(f'crystal{i}',.9,.9,1.9,crystal)
  def tank(s,tn=tn):s.box(0,0,0,.9,.9,1.3,'#46606a');s.fl(.1,.8,.3,1.1,tn);s.fl(.1,.8,.3,.6,sh(tn,.6));s.box(.2,.2,1.3,.5,.5,.1,'#2a3a40')
  mk(f'tank{i}',.9,.9,1.5,tank)
# --- personagens em camadas (tingidas pelo jogo): 4 quadros de 96x168
G=(228,228,234,255);Sd=(170,172,186,255);D=(40,42,56,255);Wt=(255,255,255,255)
def sheet(path,layer,direct=False):
  im=Image.new('RGBA',(384,168),(0,0,0,0))
  for f in range(4):
    sw=[0,6,0,-6][f]
    if direct:fr=Image.new('RGBA',(96,168),(0,0,0,0));layer(ImageDraw.Draw(fr),sw)
    else:t=Image.new('RGBA',(96,144),(0,0,0,0));layer(ImageDraw.Draw(t),sw);fr=Image.new('RGBA',(96,168),(0,0,0,0));fr.paste(t,(0,24))
    im.paste(fr,(f*96,0))
  im.save(f'{O}/chars/{path}.png')
def body(g,sw):
  for x,s in((32,sw),(52,-sw)):g.rounded_rectangle([x,106,x+14,132+min(0,s)],5,fill=Sd,outline=D,width=2);g.ellipse([x-3,126+min(0,s),x+17,140+min(0,s)],fill=(80,82,100,255),outline=D,width=2)
  for x,s in((17,-sw),(69,sw)):g.rounded_rectangle([x,68,x+11,104+s//2],5,fill=Sd,outline=D,width=2)
  g.rounded_rectangle([28,62,68,112],12,fill=G,outline=D,width=2);g.rectangle([29,98,67,106],fill=(70,72,92,255));g.rectangle([44,97,52,107],fill=Wt,outline=D);g.rectangle([29,74,67,80],fill=Wt);g.ellipse([54,84,62,92],fill=Sd,outline=D)
def head(g,sw):
  for x,s in((23,-sw),(73,sw)):g.ellipse([x-6,100+s//2,x+6,112+s//2],fill=Wt,outline=D,width=2)
  g.ellipse([14,34,24,52],fill=Wt,outline=D,width=2);g.ellipse([72,34,82,52],fill=Wt,outline=D,width=2);g.ellipse([18,8,78,66],fill=Wt,outline=D,width=2)
  for x in(36,60):g.ellipse([x-5,36,x+5,50],fill=D);g.ellipse([x-1,38,x+3,42],fill=Wt)
  g.line([30,31,42,29],fill=D,width=2);g.line([54,29,66,31],fill=D,width=2);g.arc([42,48,54,58],20,160,fill=(130,70,60,255),width=2)
  for x in(28,68):g.ellipse([x-5,50,x+5,56],fill=(255,190,190,255))
def hair(g,sw):g.pieslice([15,-8,81,58],180,360,fill=G,outline=D,width=2);g.polygon([(18,24),(16,44),(26,34)],fill=G,outline=D);g.polygon([(78,24),(80,44),(70,34)],fill=G,outline=D)
sheet('body',body);sheet('head',head);sheet('hair',hair)
def hat(k):
  def f(g,sw):
    if k=='cap':g.pieslice([14,12,82,64],180,360,fill=Wt,outline=D,width=2);g.rounded_rectangle([46,40,92,50],5,fill=Sd,outline=D,width=2)
    if k=='beanie':g.pieslice([12,0,84,62],180,360,fill=Wt,outline=D,width=2);g.rounded_rectangle([12,28,84,42],5,fill=Sd,outline=D,width=2);g.ellipse([40,0,56,14],fill=Wt,outline=D)
    if k=='helmet':g.pieslice([10,8,86,66],180,360,fill=Wt,outline=D,width=2);g.rounded_rectangle([6,35,90,47],6,fill=Sd,outline=D,width=2);g.rectangle([44,8,52,36],fill=Sd,outline=D)
    if k=='ant':g.line([48,40,56,12],fill=D,width=4);g.ellipse([48,2,66,20],fill=Wt,outline=D,width=2)
    if k=='phones':g.arc([14,24,82,84],190,350,fill=Sd,width=8);g.rounded_rectangle([8,52,22,78],5,fill=Wt,outline=D,width=2);g.rounded_rectangle([74,52,88,78],5,fill=Wt,outline=D,width=2)
    if k=='halo':g.ellipse([22,4,74,24],outline=Wt,width=6)
  return f
for k in('cap','beanie','helmet','ant','phones','halo'):sheet('hat_'+k,hat(k),True)
print('sprites ok')
