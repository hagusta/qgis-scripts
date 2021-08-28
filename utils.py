from pathlib import Path
import os
import matplotlib.pyplot as plt
from PIL import Image,ImageDraw

def loadLabels(filename:Path) -> list:
    if not filename.exists():
        raise Exception('blah')
    boxes=[]
    with open(filename,'r') as f:
        for l in f.read().split('\n'):
            #print(l)
            box=[]
            if len(l) > 0:
                for n in l.split(','):
                    box.append(float(n))
                boxes.append(box)
        #print(boxes)
    return boxes

def showSample(filename:Path) -> Image:
    dataDirectoryError= Exception("data directory does "  \
        + "not contains 'labels' directory")
    if not isinstance(filename,Path):
        if isinstance(filename,str):
            filename=Path(filename).absolute()
        else :
            raise TypeError
        
    basedir=filename.parent.parent
    if not filename.exists():
        raise FileNotFoundError
    if 'labels' not in os.listdir(basedir):
        raise dataDirectoryError
    
    filelabel=Path(os.path.join(basedir),'labels',filename.name.replace('.jpg','.txt'))
    img=Image.open(filename)
    bboxes=loadLabels(filelabel)
    #print(bboxes)
    draw=ImageDraw.Draw(img)
    szW,szH=img.size
    
    for bbox in bboxes:
        ctr0,ctr1,w,h=bbox[1],bbox[2],bbox[3],bbox[4]
        x0,x1,y0,y1=(ctr0-w/2)*szW,(ctr0+w/2)*szW,(ctr1-h/2)*szH,(ctr1+h/2)*szH
        draw.rectangle((x0,y0,x1,y1))
    return img