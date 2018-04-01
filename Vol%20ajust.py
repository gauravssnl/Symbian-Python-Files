import appuifw,e32,audio
from sysinfo import display_pixels
from graphics import*

appuifw.app.screen='full'

im=Image.new(display_pixels())
path='e:\\'
s=audio.Sound.open(path+'Vol.mp3')

def redraw(rect):
    c.blit(im)

c=appuifw.Canvas(event_callback=redraw)
appuifw.app.body=c
gbr=['vol.jpg','v_up.jpg','v_dw.jpg']

im1= Image.open(path+gbr[0])
im2=Image.open(path+gbr[1])
im3=Image.open(path+gbr[2])

def graph(): 
  vol=s.current_volume()
  im.blit(im1)
  im.blit(im2,target=(150,154))
  im.blit(im3,target=(150,202))
  im.rectangle((145,202-vol*4,165,202),0xff9900,fill=0xff9900)
  im.text((165,130),str(vol*10)+u' %',0xff0000)
  redraw(())

def up():
  v=s.set_volume(s.current_volume()+1)
  graph()
    
def down():
  v=s.set_volume(s.current_volume()-1)
  graph()

s.set_volume(1)
def play():
  s.play()
play()
graph()

c.bind(63497,up)
c.bind(63498,down)

lock=e32.Ao_lock()
def exit():
  lock.signal()
appuifw.app.exit_key_handler=exit
lock.wait()
