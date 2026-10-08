#!/usr/bin/env python3
"""Fit a wide banner image onto YouTube's 2560x1440 canvas so the given content box lands inside the
1546x423 "all devices" band. Surroundings are filled with a blurred, scaled copy of the same image.
Usage: python3 fit-banner.py <image> <x0> <y0> <x1> <y1> <out-basename>
"""
import sys
from PIL import Image, ImageFilter, ImageDraw
src=Image.open(sys.argv[1]).convert('RGB'); W,H=src.size
cx0,cy0,cx1,cy1=map(int,sys.argv[2:6]); base=sys.argv[6]
SAFE_W,SAFE_H,margin=1546,423,30
scale=min((SAFE_W-2*margin)/(cx1-cx0),(SAFE_H-2*margin)/(cy1-cy0),1.0)
sw,sh=int(W*scale),int(H*scale); img=src.resize((sw,sh),Image.LANCZOS)
CW,CH=2560,1440; cover=max(CW/W,CH/H); bg=src.resize((int(W*cover)+1,int(H*cover)+1),Image.LANCZOS)
bg=bg.crop(((bg.width-CW)//2,(bg.height-CH)//2,(bg.width-CW)//2+CW,(bg.height-CH)//2+CH)).filter(ImageFilter.GaussianBlur(30))
ox=int(CW/2-(cx0+cx1)/2*scale); oy=int(CH/2-(cy0+cy1)/2*scale)
mask=Image.new('L',(sw,sh),0); ImageDraw.Draw(mask).rectangle((36,36,sw-36,sh-36),fill=255); mask=mask.filter(ImageFilter.GaussianBlur(24))
out=bg.copy(); out.paste(img,(ox,oy),mask)
out.save(f'out/{base}.png'); out.save(f'out/{base}.jpg',quality=94)
proof=out.copy(); ImageDraw.Draw(proof).rectangle((507,508,507+SAFE_W,508+SAFE_H),outline=(255,59,48),width=4); proof.save(f'out/{base}-GUIDES.png')
print(f'scale {scale:.3f}  placed {sw}x{sh} at {ox},{oy}  content x {int(cx0*scale+ox)}-{int(cx1*scale+ox)} y {int(cy0*scale+oy)}-{int(cy1*scale+oy)}  (safe 507-2053 / 508-931)')
