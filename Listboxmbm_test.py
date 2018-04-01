import e32,appuifw
from graphics import *
import geticon
import multimbm

uid=0xe000b1a5 #pys60 uid for 1.4.5
_img=geticon.get(uid,(50,50))
img=Image.from_cfbsbitmap(_img[0])
img_mask=Image.from_cfbsbitmap(_img[1])

multimbm.create(u'd:\\test.mbm',[img,img_mask])
icon1=appuifw.Icon(u'd:\\test.mbm',0,1)
entries=[(u'pys60',unicode(hex(uid)),icon1)]
lb=appuifw.Listbox(entries,lambda:None)
app_lock = e32.Ao_lock() 

def exit():
  app_lock.signal()

appuifw.app.exit_key_handler = exit
appuifw.app.body=lb

app_lock.wait()
