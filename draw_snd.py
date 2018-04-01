import audio
import struct
import appuifw
import e32
import os
from graphics import*

path = "d:\\snd.wav"

def redraw(rect):
  canvas.blit(img)
  
canvas=appuifw.Canvas(redraw_callback=redraw)
appuifw.app.body=canvas
appuifw.app.screen='full'
img=Image.new(canvas.size)

def exit():
    global flag
    flag = 0
    sound.stop()
    sound.close()
    if os.path.isfile(path):
        os.remove(path)
appuifw.app.exit_key_handler = exit
sound = audio.Sound.open(u'%s' % path)
open(path, "w").write('')

X,Y=canvas.size
Y/=2

flag = 1
while flag:
    os.remove(path)
    sound.record()
    e32.ao_sleep(0.04)
    sound.stop()
    fo = open(path)
    header = fo.read(44)
    size = struct.unpack('l', header[40:44])[0]
    data = fo.read(size)
    fo.close()
    num=[ ord(data[i]) !=255 and (ord(data[i])>127 and ord(data[i])-255 or ord(data[i]))  for i in xrange(1,size,2) ]
   
    xz=len(num)/X
    if xz>2:
      lst=[ [max(num[i:i+xz]),min(num[i:i+xz])] for i in range(0,len(num),xz) ]
    else:  
      lst=[ [i,i] for i in num ]
      
    img.clear(0)
    
    for i in range(len(lst)-1):
       img.line(( i,(lst[i][0]+Y),i,(lst[i+1][0]+Y) ,  i,(lst[i][1]+Y),i,(lst[i+1][1]+Y)),0xeebb00)
    redraw(())
    