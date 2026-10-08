#!/usr/bin/env python3
"""Derive channel-art inputs from the real 4:19 Podcast logo (assets/419-podcast-logo.png, square).

Outputs:
  assets/419-logo-circle.png        rope ring cut out as a circle, transparent outside (banner, badges)
  assets/shield-canvas.png          Sharpening shield cut from the logo, on its own canvas (canvas banner)
  assets/shield-light.png           same shield, bone-colored with transparent background (charcoal banner)
  out/profile-800x800.*             ring on canvas, for a channel profile picture
  out/podcast-cover-2000x2000.*     the full square logo, for the podcast playlist
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageStat
here=os.path.dirname(os.path.abspath(__file__))
src=Image.open(os.path.join(here,'assets','419-podcast-logo.png')).convert('RGBA'); W,H=src.size
CANVAS=tuple(int(v) for v in ImageStat.Stat(src.convert('RGB').crop((10,10,120,120))).mean)+(255,)
os.makedirs(os.path.join(here,'out'),exist_ok=True)
a=np.asarray(src.convert('RGB')).astype(int); lum=a.mean(axis=2)
d=np.abs(a-np.array(CANVAS[:3])).sum(axis=2)>120

# ring extent -> circle cut-out
xs=np.where(d[H//2,:])[0]; ys=np.where(d[:,W//2])[0]
cx=(xs.min()+xs.max())//2; cy=(ys.min()+ys.max())//2; r=max(xs.max()-xs.min(), ys.max()-ys.min())//2+14
pad=Image.new('RGBA',(W+2*r,H+2*r),CANVAS); pad.paste(src,(r,r))
sq=pad.crop((cx, cy, cx+2*r, cy+2*r))
mask=Image.new('L',sq.size,0); ImageDraw.Draw(mask).ellipse((0,0,sq.size[0]-1,sq.size[1]-1),fill=255); mask=mask.filter(ImageFilter.GaussianBlur(1.2))
circ=sq.copy(); circ.putalpha(mask); circ=circ.resize((1024,1024),Image.LANCZOS)
circ.save(os.path.join(here,'assets','419-logo-circle.png'))

# shield: darkest blob in the lower middle, below the SHARPENING MINISTRIES line
y0,y1,x0,x1=int(H*0.70),int(H*0.86),int(W*0.42),int(W*0.58)
reg=lum[y0:y1,x0:x1]<80; sy,sx=np.where(reg)
bx0,bx1,by0,by1=sx.min()+x0, sx.max()+x0, sy.min()+y0, sy.max()+y0
m=12; box=(bx0-m,by0-m,bx1+m,by1+m)
shield=src.crop(box)
sa=np.asarray(shield.convert('RGB')).astype(int); sl=sa.mean(axis=2)
# silhouette = everything darker than canvas, with the S stripes (holes) filled in
edge=Image.fromarray(((sl<150)*255).astype('uint8'))
canvasish=(sl>=150)
# exterior = canvas pixels connected to the crop border (grow from the border until stable)
ext=np.zeros_like(canvasish); ext[0,:]=canvasish[0,:]; ext[-1,:]=canvasish[-1,:]; ext[:,0]=canvasish[:,0]; ext[:,-1]=canvasish[:,-1]
while True:
    grown=ext.copy()
    grown[1:,:]|=ext[:-1,:]; grown[:-1,:]|=ext[1:,:]; grown[:,1:]|=ext[:,:-1]; grown[:,:-1]|=ext[:,1:]
    grown&=canvasish
    if (grown==ext).all(): break
    ext=grown
sil=~ext
# canvas version: original pixels (dark shield + canvas stripes), transparent outside the outline
sc=shield.copy(); sc.putalpha(Image.fromarray((sil*255).astype('uint8')).filter(ImageFilter.GaussianBlur(0.8)))
sc.save(os.path.join(here,'assets','shield-canvas.png'))
# light version for dark backgrounds: the dark body -> bone, stripes and outside transparent
dark=(sl<120)&sil
light=Image.new('RGBA',shield.size,(243,238,227,255)); light.putalpha(Image.fromarray((dark*255).astype('uint8')).filter(ImageFilter.GaussianBlur(0.6)))
light.save(os.path.join(here,'assets','shield-light.png'))

# profile 800x800 and podcast cover 2000x2000
prof=Image.new('RGBA',(800,800),CANVAS); prof.alpha_composite(circ.resize((688,688),Image.LANCZOS),(56,56))
prof.convert('RGB').save(os.path.join(here,'out','profile-800x800.png')); prof.convert('RGB').save(os.path.join(here,'out','profile-800x800.jpg'),quality=92)
cov=src.resize((2000,2000),Image.LANCZOS).convert('RGB')
cov.save(os.path.join(here,'out','podcast-cover-2000x2000.png')); cov.save(os.path.join(here,'out','podcast-cover-2000x2000.jpg'),quality=92)
print('ring center',cx,cy,'r',r,'| shield box',box,'| canvas',CANVAS[:3])
