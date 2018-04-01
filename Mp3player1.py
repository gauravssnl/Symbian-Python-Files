import appuifw,e32,powlite_fm,key_codes
from audio import*
from sysinfo import display_pixels
from graphics import*
appuifw.app.screen='full'
pow=powlite_fm.manager()

t=0
run=1
def exit():
  global run,s
  run=0
  s.stop()

appuifw.app.exit_key_handler=exit

def start():
  try:
    if os.path.isfile('e:\\mp3.dat'):
      pass
    else:
      dir=pow.AskUser(find='dir')
      file=open('e:\\mp3.dat','w')
      file.write(dir)
      file.close()    
  except:pass
start()
r=open('e:\\mp3.dat','r')
idx=r.readlines()
r.close()
dir=idx[0]
files=map(unicode, os.listdir(dir))
s=Sound.open(dir+'\\'+files)

s.set_volume(1)

im=Image.new(display_pixels())
path='e:\\'

def redraw(rect):
    c.blit(im)

c=appuifw.Canvas(redraw_callback=redraw)
appuifw.app.body=c

gbr=['play.jpg','v_up.jpg','v_dw.jpg','pau.jpg','ply.jpg']

im1= Image.open(path+gbr[0])
im.blit(im1)
redraw(())
im2=Image.open(path+gbr[1])
im3=Image.open(path+gbr[2])
im4=Image.open(path+gbr[3])
im5=Image.open(path+gbr[4])
# define images
def io(m):
 x=Image.open(path + m)
 return x

im6=io('nex.jpg')
im7=io('prv.jpg')
im8=io('spk.jpg')
im9=io('mute.jpg')

pos=0

def play_callback(previous, current, err):
  global pos
  if previous==2:
    pos=0
    
def process(val):
  global pos
  if val=='up':
    s.set_volume(s.current_volume()+1)
    im.blit(im2,target=(146,148))
  elif val=='down':
    s.set_volume(s.current_volume()-1)
    im.blit(im3,target=(146,205))
  elif val=='left':
    im.blit(im7,target=(102,175))
  elif val=='right':  
    im.blit(im6,target=(176,175))
  else: #ok
    if s.state()==1:
        #s.set_position(pos)
        s.play(callback=play_callback)
        im1.blit(im4,target=(148,176))
    elif s.state()==2:
        pos=s.current_position()
        s.stop()
        s.set_position(pos)
        im1.blit(im5,target=(148,176))
        
  redraw(())
    
txt_m = u'help me to put music title here'  
end_pos=172

c.bind(63497,lambda:process('up'))
c.bind(63498,lambda:process('down'))
c.bind(63495,lambda:process('left'))
c.bind(63496,lambda:process('right'))
c.bind(63557,lambda:process('ok'))

while run:
  t-=1
  if t<-200:t=300
  im.blit(im1)
  im.text((t,10),txt_m,0xffffff,font=(u'default',12,appuifw.STYLE_BOLD))   
# Loading progress 
  sec=int(s.current_position())/1000000
  m=sec/60
  sec-=(m*60)
  dur=int(s.duration())/1000000
  dur_m=dur/60
  dur-=(dur_m*60)
  vol=s.current_volume()
  bbb=float(s.current_position())/s.duration()*end_pos
  im.rectangle((199,109,287,114),0xff0000,fill=0xffffff,width=1)
  im.rectangle((200+bbb/2,110,286,113),0x000099,fill=0x000099,width=1)  
# Time bar
  im.text((275,108),u''+str(m)+':'+str(sec),0xff9900,font=(u'default',14,appuifw.STYLE_BOLD))
  im.text((190,108),u''+str(dur_m)+':'+str(dur),0xff9900,font=(u'default',14,appuifw.STYLE_BOLD))
# volume  
  im.rectangle((277,189-vol*6,290,189),0xffffff,fill=0xffffff)
  im.rectangle((275,129,290,189),0xff9900,width=2)
  im.text((260,128),str(vol*10)+u'%',0xff0000,font=(u'default',14,appuifw.STYLE_BOLD))
  
  if vol==0:
    im.blit(im9,target=(275,195))
  else:im.blit(im8,target=(275,195))
  redraw(())
  e32.ao_sleep(0.1)
  