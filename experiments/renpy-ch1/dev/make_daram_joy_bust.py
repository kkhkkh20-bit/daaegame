"""Build assets/room13-pixel-dialogue-daram-joy.webp from the reviewed world joy pose.

usage: make_daram_joy_bust.py room13-pixel-world-family-extra-gray.(png|webp) OUT.png
Upper body only (dialogue bust), soft dark halo removed (alpha < 250 -> 0, else opaque).
"""
import sys
import numpy as np
from PIL import Image
im=Image.open(sys.argv[1]).convert('RGBA').crop((1101,44,1101+395,44+330))
a=np.asarray(im).copy()
a[...,3]=np.where(a[...,3]>=250,255,0)
a[a[...,3]==0]=0
Image.fromarray(a).save(sys.argv[2])
