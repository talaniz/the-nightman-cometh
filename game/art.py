"""Cached production atlas loading. Layout/text/collision stay owned by game code."""
from pathlib import Path
import pygame

class Art:
    def __init__(self):
        self.root=Path(__file__).resolve().parents[1]/'assets'
        self.cache={};self.scaled={}

    def panel(self,name,index,columns=2,rows=3):
        key=(name,index,columns,rows)
        if key in self.cache:return self.cache[key]
        path=self.root/('sprites/cast.png' if name=='cast' else 'scenes/act1/'+name+'.png')
        image=pygame.image.load(str(path)).convert_alpha()
        x=index%columns;y=index//columns
        rect=pygame.Rect(x*image.get_width()//columns,y*image.get_height()//rows,
                        (x+1)*image.get_width()//columns-x*image.get_width()//columns,
                        (y+1)*image.get_height()//rows-y*image.get_height()//rows)
        result=image.subsurface(rect).copy()
        if name=='cast':
            bounds=result.get_bounding_rect(min_alpha=20)
            if bounds.width and bounds.height:result=result.subsurface(bounds).copy()
        self.cache[key]=result
        return result

    def image(self,name,index,size,flip=False):
        key=(name,index,size,flip)
        if key not in self.scaled:
            source=self.panel(name,index,4,4) if name=='cast' else self.panel(name,index)
            result=pygame.transform.scale(source,size)
            if flip:result=pygame.transform.flip(result,True,False)
            self.scaled[key]=result
        return self.scaled[key]
