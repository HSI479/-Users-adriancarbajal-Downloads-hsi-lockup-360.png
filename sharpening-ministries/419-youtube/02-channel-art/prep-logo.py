#!/usr/bin/env python3
"""Derive the channel-art inputs from the real 4:19 Podcast logo (assets/419-podcast-logo.png).

Outputs (assets/ and out/):
  assets/419-logo-circle.png     rope ring cut out as a circle, transparent outside (badges, banner)
  out/profile-800x800.png/.jpg   ring on canvas, for a channel profile picture
  out/podcast-cover-2000x2000.*  square crop of the full logo (ring + net) for the podcast playlist
Usage: python3 prep-logo.py [--cx 790 --cy 442 --r 428]  (ring center and outer radius in source pixels)
"""
import argparse, os
from PIL import Image, ImageDraw, ImageFilter
ap=argparse.ArgumentParser(); ap.add_argument('--cx',type=int,default=786); ap.add_argument('--cy',type=int,default=441); ap.add_argument('--r',type=int,default=450)
A=ap.parse_args(); here=os.path.dirname(os.path.abspath(__file__))
src=Image.open(os.path.join(here,'assets','419-podcast-logo.png')).convert('RGBA'); W,H=src.size
CANVAS=(206,188,167,255)
os.makedirs(os.path.join(here,'out'),exist_ok=True)

# 1. circle cut-out
r=A.r; box=(A.cx-r, A.cy-r, A.cx+r, A.cy+r)
pad=Image.new('RGBA',(W+2*r,H+2*r),CANVAS); pad.paste(src,(r,r))
sq=pad.crop((box[0]+r, box[1]+r, box[2]+r, box[3]+r))
mask=Image.new('L',sq.size,0); ImageDraw.Draw(mask).ellipse((0,0,sq.size[0]-1,sq.size[1]-1),fill=255)
mask=mask.filter(ImageFilter.GaussianBlur(1.2))
circ=sq.copy(); circ.putalpha(mask)
circ=circ.resize((1024,1024),Image.LANCZOS); circ.save(os.path.join(here,'assets','419-logo-circle.png'))

# 2. profile 800x800: ring on canvas, ring fills 86% so the circular avatar crop keeps the rope
prof=Image.new('RGBA',(800,800),CANVAS); c=circ.resize((688,688),Image.LANCZOS); prof.alpha_composite(c,(56,56))
prof.convert('RGB').save(os.path.join(here,'out','profile-800x800.png')); prof.convert('RGB').save(os.path.join(here,'out','profile-800x800.jpg'),quality=92)

# 3. square podcast cover from the full logo (keeps the net at lower right)
side=H; x0=max(0,min(W-side, A.cx-side//2 + 35))   # nudge right so some net shows
cov=src.crop((x0,0,x0+side,side)).resize((2000,2000),Image.LANCZOS).convert('RGB')
cov.save(os.path.join(here,'out','podcast-cover-2000x2000.png')); cov.save(os.path.join(here,'out','podcast-cover-2000x2000.jpg'),quality=92)
print('circle', circ.size, 'profile 800x800', 'cover crop x0=',x0)
