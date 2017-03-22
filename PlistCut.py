#!/usr/bin/python
__author__ = 'lichenyang'

import os
import re
import sys
import xml.dom.minidom
import json
import sys
import string
from biplist import *
from PIL import Image
import matplotlib.pyplot as plt

plistPath=sys.argv[1]+".plist"
pngPath=sys.argv[1]+".png"

im = Image.open(pngPath)
outDict = {}
outDict["frames"] = {}
try:
    plist = readPlist(plistPath)
except (InvalidPlistException, NotBinaryPlistException), e:
    print "Not a plist:", e
if plist.has_key("frames") == False:
    print plistPath+" is not sprite sheet file"
for key,value in plist.frames.items():
    frameTmp = re.compile(r'\d+').findall(value.frame)
    offsetTmp = re.compile(r'\d+').findall(value.offset)
    sourceSizeTmp = re.compile(r'\d+').findall(value.sourceSize)
    fameInfo = {}
    fameInfo["x"] = string.atoi(frameTmp[0])
    fameInfo["y"] = string.atoi(frameTmp[1])
    fameInfo["w"] = string.atoi(frameTmp[2])
    fameInfo["h"] = string.atoi(frameTmp[3])
    fameInfo["offX"] = string.atoi(offsetTmp[0])
    fameInfo["offY"] = string.atoi(offsetTmp[1])
    fameInfo["sourceW"] = string.atoi(sourceSizeTmp[0])
    fameInfo["sourceH"] = string.atoi(sourceSizeTmp[1])
    fameInfo["rotated"] = value.rotated
    childKey = re.compile(r'\.png').split(key)[0]
    outDict["frames"][childKey] = fameInfo
    print(fameInfo)
    x=int(fameInfo["x"])
    y=int(fameInfo["y"])
    w=int(fameInfo["w"])
    h=int(fameInfo["h"])
    if fameInfo["rotated"] == True:
        w=int(fameInfo["h"])
        h=int(fameInfo["w"])
    box=(x,y,x+w,y+h)
    copyImg = im.crop(box)
    saveImg = Image.new("RGBA", (w, h), (0,0,0,0))
    saveImg.paste(copyImg)
    copyImg.save(key,'png')

