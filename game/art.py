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
        path=self.root/('sprites/cast.png' if name=='cast' else ('scenes/act2/story.png' if name=='bridge-story' else 'scenes/act1/'+name+'.png'))
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
            source=self.panel(name,index,4,4) if name=='cast' else (self.panel(name,index,2,2) if name=='bridge-story' else self.panel(name,index))
            result=pygame.transform.scale(source,size)
            if flip:result=pygame.transform.flip(result,True,False)
            self.scaled[key]=result
        return self.scaled[key]

    def asset(self,relative,size,trim=False):
        """Cache fixed, repository-owned textures; callers do not supply user paths."""
        key=('asset',relative,size,trim)
        if key not in self.scaled:
            source=pygame.image.load(str(self.root/relative)).convert_alpha()
            if trim:source=source.subsurface(source.get_bounding_rect(min_alpha=20)).copy()
            self.scaled[key]=pygame.transform.scale(source,size)
        return self.scaled[key]

    def sequence(self,relative,index,columns,rows,size,flip=False,trim_row=False):
        """Equal atlas cells; shared row bounds preserve scale across animation frames."""
        key=('sequence',relative,index,columns,rows,size,flip,trim_row)
        if key not in self.scaled:
            source_key=('source',relative)
            if source_key not in self.cache:
                self.cache[source_key]=pygame.image.load(str(self.root/relative)).convert_alpha()
            source=self.cache[source_key];cw=source.get_width()//columns;ch=source.get_height()//rows
            row=index//columns
            rect=pygame.Rect(0,0,cw,ch)
            if trim_row:
                bounds=[source.subsurface((col*cw,row*ch,cw,ch)).get_bounding_rect(min_alpha=20) for col in range(columns)]
                rect=bounds[0].unionall(bounds[1:])
            cell=source.subsurface(((index%columns)*cw,row*ch,cw,ch)).subsurface(rect)
            frame=pygame.transform.scale(cell,size)
            self.scaled[key]=pygame.transform.flip(frame,True,False) if flip else frame
        return self.scaled[key]
