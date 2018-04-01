
import struct, zut, os, appuifw
import TopWindow,sys,e32
from graphics import*

sys.setdefaultencoding('utf-8')

mydir=os.path.dirname(appuifw.app.full_name())+'\\'

def put(x,p=u'e://',y=0):
  global path
  p = (y and appuifw.query(unicode("Путь"), "text",unicode(p))) or p
  p = p[-1] != '/' and p+'/' or p
  fo=open(mydir+'dir',x and 'r' or 'w')
  path = (x and fo.read() ) or fo.write(p) or p
  fo.close()
  return 1

os.path.exists(mydir+'dir') and put(1) or put(0)

app_lock = e32.Ao_lock()    
z=zut.sound()

so=z.load_znd(mydir+'win.znd')
do=z.load_znd(mydir+'din.znd')
er=z.load_znd(mydir+'er.znd')

img=Image.new((176,208))

def handle_redraw(rect):
  canvas.blit(img)

class Buf:
 def __init__(self):
  self.buf=[]

buf=Buf()

class Top:
 def __init__(self):
   self.win=TopWindow.TopWindow()
   self.win.size = (170,40)
   self.win.position = (3,40)
   self.win.shadow = 2 
   self.win.corner_type = 'corner1' 
   self.top = Image.new((170,40))
   self.t=0; self.p=1
   self.vis()

 def pause(self,x):
  self.p=x
  if self.p and self.t: self.win.show()
  else: self.win.hide()
  
 def vis(self):
   self.top.rectangle((0,0,170,40),0,fill=0x007700)
   self.top.rectangle((10,15,160,35),0,fill=0xffffff)
   self.top.text((62,12),unicode('Прогресс'),0xffffff)
   self.win.add_image(self.top,(0,0))
   self.pause(self.p)

 def progress(self,p):
   self.win.remove_image(self.top)
   self.vis()
   x=(159-11)*p/100+11
   self.top.rectangle((11,16,x+2,20),fill=0x9999ff)
   self.top.rectangle((11,20,x+2,34),fill=0x2222dd)
   self.win.add_image(self.top, (0,0))
   e32.ao_yield()
   if p>98: self.win.hide();self.t=0
   return 0


 def note(self,text,x=1):
   self.win.remove_image(self.top)
   self.t=1; self.vis()
   self.top.rectangle((0,0,170,40),0,fill=x and 0x007700 or 0xaa0000)

   for t,y in zip(text,[13,25,37]):
     self.top.text((84- img.measure_text(t, font=u'LatinBold12')[1]/2,y),unicode(t),0xffffff,u'LatinBold12')   

   self.win.add_image(self.top, (0,0))
   x and z.play_znd(do) or not x and z.play_znd(er)
   e32.ao_sleep(3)
   self.win.hide(); self.t=0

top_w=Top()
appuifw.app.focus=top_w.pause

def format_w(f):
  fo=open(mydir+'formatw','r')
  format=fo.read()
  fo.close()
  format=eval(format)
  top_w.note(['Формат',format[f]+'       ',' Неподдерживается'],0)

# управление
class Use:
 def __init__(self,fm):
  self.mar_r=0; self.mar_l=-1
  self.xr=0; self.xl=175
  self.key=0; self.pix_xr=0
  self.pix_xl=0; self.trig=1
  self.list=[]; self.un=0
  self.name=fm.split('/')[-1][-20:]

  self.fm=fm; self.open_s(fm)
  self.func=lambda e,xt:  ((e==63496 and (xt<175) ) and 1) or ((e==63495 and (xt>0)) and -1)

 def trigger(self):
   self.trig=~self.trig+2
   self.key=0; self.linact()

 def tobuf(self,c=0):
   a=self.choice()
   buf.buf=self.num[a[0]:a[1]]
   if c:
     self.undo(a[0],a[0],self.num[a[0]:a[1]])
     self.num=self.num[:a[0]]+self.num[a[1]:]
     self.graph(0)
     tab.tab(self.name)
   self.foot();  self.key=0

# Ограничители
 def line(self,e='xl',x=0):
   if self.trig: e='xr'
   x=self.func(self.key,self.__dict__[e])
   self.__dict__[e]+=x
   if self.xr == self.xl: self.__dict__[e]-=x; return

   if self.__dict__['pix_'+e] : 
     [img.point((self.__dict__[e]-x,i),self.__dict__['pix_'+e][i][0]) for i in range(20,180)] 
   self.__dict__['pix_'+e]=[img.getpixel((self.__dict__[e],i)) for i in range(0,180)] 
   self.linact()

 def linact(self):
  n=self.trig and 'xr' or 'xl'
  ne=self.trig and 'xl' or 'xr'
  if (not self.trig and self.xr) or (self.trig and self.xl<175):
    img.line((self.__dict__[ne],20,self.__dict__[ne],180),0xffffff)
  if  (self.trig and self.xr) or (not self.trig and self.xl<175):
    img.line((self.__dict__[n],20,self.__dict__[n],180),0xffffff)
    img.line((self.__dict__[n],170,self.__dict__[n],180),0xff0000)
    img.line((self.__dict__[n],20,self.__dict__[n],30),0xff0000)

 def save(self,x):
  tip=appuifw.query(unicode("Сохранить как znd"), "query") and '.znd' or '.wav'

  name = appuifw.query(unicode("Имя файла (расширение "+tip+" не писать)"), "text") 

  if name:
   if os.path.exists(unicode(path+'/'+name+tip)):
     if not appuifw.query(unicode("Такой файл существует,перезаписать"), "query"): return
   a= self.choice() 
   fo=open(unicode(path+'/'+name+tip),'wb')

   top_w.t=1
   L=len(x and self.num[a[0]:a[1]] or self.num)
   d=range(L/20,L,L/20)

   if tip=='.znd':
#     --- As Znd ---
     fo.write(struct.pack('h',self.hz ) )
     for i in xrange(L):
       fo.write(struct.pack('i',-( x and self.num[i+a[0]] or (not x and self.num[i])) )[0] )
       i in d and top_w.progress(int( 100/(L/float(i) )))

   else:
#     --- As Wav ---
    h=open(mydir+'headwav','rb')
    header=h.read()
    h.close() 
    fo.write(header[0:4]+struct.pack('i',len( x and self.num[a[0]:a[1]] or self.num)+36 )+header[8:24]+struct.pack('i',self.hz)+header[28:40]+struct.pack('i',len( x and self.num[a[0]:a[1]] or self.num)) )
    for i in xrange(L):
       fo.write(struct.pack('i',255-((x and self.num[a[0]+i] or (not x and self.num[i]))+127) )[0] )
       i in d and top_w.progress(int( 100/(L/float(i) )))

   fo.close()
   top_w.note(['Файл',name+tip,' Сохраннен'])
    
 def play(self,x):
  if not x: a=self.choice()
  else: a=[0,-1]
  fo=open(u'd:\\temp','wb')  
  for i in x==2 and buf.buf or self.num[a[0]:a[1]]:
    fo.write(struct.pack('i',-i)[0] )
  fo.close()
  z.load_raw(u'd:\\temp',self.hz)
  z.play_raw()
  self.key=0

 def open_s(self,fm):
   self.num=0
   in_=open(fm, "rb") 
   if fm.lower()[-3:]=='znd':
     self.hz=struct.unpack('h',in_.read(2))[0]
     buf=in_.read()
     if len(buf)<175: top_w.note([' ','Размер менее 175'],0);in_.close(); return
     self.size=len(buf)
     top_w.t=1
     d=range(self.size/20,self.size,self.size/20)

     self.num=[  ord(buf[i])  and( ord(buf[i])<128 and ~ord(buf[i])+1 or 255-ord(buf[i]) )   for i in xrange(self.size) if (i in d and top_w.progress(int( 100/(self.size/float(i) ))) ) or 1 ]
 
     self.zoom(0,len(self.num),0)
     top_w.t=0;top_w.pause(1)
     in_.close(); return

   header=in_.read(44)
   f=struct.unpack('h',header[20:22])[0] 
   if f !=1: format_w(f); in_.close();  return # # # # #
   self.size=struct.unpack('l',header[40:44])[0]
   self.hz=struct.unpack('l',header[24:28])[0]
   bit=struct.unpack('h',header[34:36])[0]
   kk=struct.unpack('h',header[22:24])[0]-1
   bit2=struct.unpack('h',header[32:34])[0]
   buf= in_.read(self.size)
   in_.close()

   if self.hz>32000: top_w.note([' ','Частота больше 32000'],0); return
   if len(buf)<175: top_w.note([' ','Размер менее 175'],0); return
   if kk: 
     appuifw.app.screen='normal'
     k=appuifw.multi_selection_list([unicode('левый'),unicode('правый')],style='checkbox')
     appuifw.app.screen='full'
     if k: k=k[0]
     else:  return 
   top_w.t=1
   L=self.size
   d=range(L/20,L,L/20)

   if bit == 8 :  
    self.num=[ 255-(ord( buf[x])+127)  for x in xrange(L)   if  (x in d and top_w.progress(int( 100/(L/float(x) ))) ) or (~kk+2) or (kk and divmod(x+k,2)[1]) ]
    
   elif bit == 16 :     
    self.num=[ord(buf[x]) !=255 and (ord(buf[x])>127 and ord(buf[x])-255 or ord(buf[x]))  for x in xrange(L)   if ( x in d and top_w.progress(int( 100/(L/float(x) ))) ) or (~kk+2 and divmod(x,2)[1]) or (kk and divmod(x,4)[1]==3-(k+k) ) ]

   top_w.t=0;top_w.pause(1)
   self.zoom(0,len(self.num),0)
 
 def paste(self):
  a=self.choice()
  self.undo(a[0],a[0]+len(buf.buf),[])
  self.num=self.num[:a[0]]+buf.buf+self.num[a[0]:]
  self.graph(0)
  tab.tab(self.name); self.foot() 

 def invert(self):
  a=self.choice()
  num=self.num[a[0]:a[1]]
  self.undo(a[0],a[1],self.num[a[0]:a[1]])
  num.reverse()
  self.num=self.num[:a[0]]+num+self.num[a[1]:]
  self.graph(0)
  tab.tab(self.name); self.foot()

 def back(self):
  if len(self.list)>1:
   self.mar_r=self.list[-1][0]
   self.mar_l=self.list[-1][1]
   self.graph()
   self.list.pop()
   self.key=0
   tab.tab(self.name); self.foot()

 def zoom(self,_r,_l,x=1):
   self.list.append([self.mar_r,self.mar_l])
   self.mar_r=len(self.num[_r : _l])/175*self.xr+self.list[-1][0]
   if self.xl<175: 
    self.mar_l=len(self.num[_r : _l])/175*self.xl+self.list[-1][0]
   self.graph()
   self.foot()
   x and tab.tab(self.name)

# Прорисовка звука
 def graph(self,x=1):
   if x: self.xr,self.xl,self.pix_xr,self.pix_xl=0,175,0,0
   img.clear(0)
   num=self.num[self.mar_r : self.mar_l]
   xz=len(num)/175
   if xz>2:
     list=[ [max(num[i:i+xz])*0.635,min(num[i:i+xz])*0.635] for i in range(0,len(num),xz) ]
   else:   list=[ [i*0.635,i*0.635] for i in num ]
   # Рисуем
   for i in range(len(list)-1):
       img.line(( i,(list[i][0]+100),i,(list[i+1][0]+100) ,  i,(list[i][1]+100),i,(list[i+1][1]+100)),0x00bb00)
   self.linact()
 
 def foot(self):
   img.rectangle((0,182,176,208),fill=0)
   img.text((3,192),unicode(self.hz)+u' Hz',fill=0xaaaaaa)
   img.text((3,204),unicode(len(self.num))+u' Byte',fill=0xaaaaaa)
   img.text((134,192),u'zoom='+unicode(len(self.list)-1),fill=0xcccc00)
   if len(buf.buf): img.text((64,192),u'buf->'+unicode(len(buf.buf)),fill=0x009900)

 def choice(self):
  xr=len(self.num[self.mar_r : self.mar_l])/175*self.xr+self.mar_r
  xl=len(self.num[self.mar_r : self.mar_l])/175*self.xl+self.mar_r
  return (xr,xl)

# Нормализация и громкость
 def norm(self,x=0):
  a=self.choice()
  num=self.num[a[0]:a[1]]
  self.undo(a[0],a[1], num)
  X=float(127)/max(max(num),abs(min(num)))
  if x:
   vol = appuifw.query(unicode("Громкость в процентах" ), "number",int(round(100/X)))
   vol = vol>100 and 100 or vol<10 and 10 or vol
   X=vol*X/100  
  num=[int(round(i*X)) for i in num]
  self.num=self.num[:a[0]]+num+self.num[a[1]:]
  self.graph(0)
  tab.tab(self.name); self.foot()

# Нарастание & Спад
 def naspad(self,x):
  a=self.choice()
  num=self.num[a[0]:a[1]]
  self.undo(a[0],a[1], self.num[a[0]:a[1]])
  L=len(num)
  list=range(1,L+1)
  if x: num.reverse(); list.reverse()
  num=[ int(round( num[i-1] * (100/(float(L)/i)) /100) ) for i in list ]

  self.num=self.num[:a[0]]+num+self.num[a[1]:]
  self.graph(0)
  tab.tab(self.name); self.foot()

 def undo(self,x1=0,x2=0,data=0):
   if x2:
     self.un=[x1,x2,data]
   elif self.un :
     self.num=self.num[:self.un[0]]+self.un[2]+self.num[self.un[1]:]
     self.un=0
     self.graph(0)
     tab.tab(self.name); self.foot()


class Tab:
 def __init__(self):
   self.list=[]
   self.act, self.key, self.mem=0,0,0
   self.fu=lambda z,y:( img.rectangle((0,0,176,19),z) or  img.rectangle((0,19,176,181),y) )

   self.st=lambda : (  img.text((134,14),unicode('<'),fill=( len(self.list)>0 and 0<self.mem<=len(self.list)-1 and 0xffffff) or 0x444444 )  or img.text((142,14),unicode(str(self.mem+1)),fill=0xaaaaaa)  or  img.text((150,14),unicode('>'),fill=( (len(self.list)>0 and self.mem+1<len(self.list) )and 0xffffff) or 0x444444)  )

 def addf(self,filename):
   self.list.append(Use(filename))
   if not self.list[-1].num: self.list.pop(); return
   self.mem=len(self.list)-1
   self.act=self.list[ self.mem ]
   self.tab(self.act.name)
 
 def tab(self,name=0,z=0):
   img.text((3,14),unicode(name),fill=0xffffff)
   img.text((160,14),unicode(str(len(self.list) or 1)),fill=0xdddd00)
   self.fu(0,0x777777)
   self.st()
   
 def mov(self):
   if self.key==63496 and self.mem+1<len(self.list): self.mem+=1
   elif self.key==63495 and 0 < self.mem <= len(self.list)-1: self.mem-=1
   else: return
   self.list[self.mem].graph(0)
   self.tab(self.list[self.mem].name)
   self.fu(0x7777777,0)
   self.list[self.mem].foot()
   self.key=0; z.play_znd(so)

 def closef(self):
  if len(self.list)>1:
    del self.list[self.mem]
    self.mem=len(self.list)-1
    self.act=self.list[self.mem]
    self.act.graph(0)
    self.act.foot()
    self.tab(self.act.name)
  
tab=Tab()

canvas=appuifw.Canvas(redraw_callback=handle_redraw)
appuifw.app.body=canvas
appuifw.app.screen='full'

try:
  import image1st
  img.blit(Image.from_cfbsbitmap(image1st.convertimage(mydir+'def.gif')))

except: img.blit(Image.open(mydir+'def.gif'))

handle_redraw(())

wavfile=lambda x: os.path.splitext(x)[1].lower() ==  '.wav' or os.path.splitext(x)[1].lower() == '.znd'

def fileopen():
  appuifw.app.screen='normal'
  w_list = filter(wavfile, os.listdir(path))
  index = appuifw.selection_list(map(unicode, w_list))
  appuifw.app.screen='full'
  if index>-1:
    tab.addf(unicode(path+w_list[index]))
    len(tab.list)==1 and  app_lock.signal()


def help(): 
 e32.start_exe('z:\\system\\programs\\AppRun.exe', 'z:\\System\\Apps\\Browser\\Browser.app "file:///'+mydir+'help.htm"' )

appuifw.app.menu=[ (unicode('Открыть файл'),fileopen),
(unicode('Путь'),lambda:put(0,path,1)) ,
( (unicode('Help'),help ) )]
appuifw.app.exit_key_handler=os.abort

app_lock.wait()

#-----------------

menu=[ 
( unicode('Файл'), (( (unicode('Открыть'),fileopen),  (unicode('Сохранить'),lambda: tab.act.save(0)), (unicode('Сохранить выбранное'),lambda: tab.act.save(1)) ,(unicode('Закрыть'),tab.closef),(unicode('Путь'),lambda:put(0,path,1)) )) ),
 ( unicode('Play'), ((unicode('Выбранное (.)'),lambda: tab.act.play(0) ),  (unicode('Все (*)'),lambda: tab.act.play(1) ),(unicode('Буфер (AВC)'),lambda: tab.act.play(2) ))  ),
 ( unicode('Выбранное'), ((unicode('Реверс (7)'), tab.act.invert ), 
(unicode('Громкость (del)'), lambda: tab.act.norm(1) ), (unicode('Нормализация (0)'), tab.act.norm ),  (unicode('Нарастание (8)'),lambda: tab.act.naspad(0) ),(unicode('Спад (9)'),lambda: tab.act.naspad(1) ))  ),
 ( unicode('Буфер'), ((unicode('Копировать (4)'),lambda: tab.act.tobuf() ),  (unicode('Вырезать (5)'),lambda: tab.act.tobuf(1) ),  (unicode('Вставить (6)'),tab.act.paste  ))  ),
( unicode('Zoom'), ((unicode('Увеличить (2)'),lambda: tab.act.zoom(tab.act.mar_r,tab.act.mar_l) ),  (unicode('Уменьшить (3)'),tab.act.back ))  ),
( (unicode('Отменить (#)'),tab.act.undo ) ),
( (unicode('Help'),help ) )
 ]

def callback(event):
    if event['type'] == appuifw.EEventKey:
      tab.act.key=event['keycode']
      if event['keycode']==63497: tab.act=tab; tab.fu(0x7777777,0); appuifw.app.menu=[]
      if event['keycode']==63498: tab.act=tab.list[ tab.mem ]; tab.fu(0,0x777777); appuifw.app.menu=menu
    else: tab.act.key=0

appuifw.app.menu=menu
canvas=appuifw.Canvas(redraw_callback=handle_redraw,event_callback=callback)
appuifw.app.body=canvas

switch= { 63557: 's.play(0)', 51: 's.back()', 49: 's.trigger()' , 50: 's.zoom(s.mar_r,s.mar_l)', 52: 's.tobuf()',53: 's.tobuf(1)', 54: 's.paste()', 55: 's.invert()', 63496: 's.line()', 63495: 's.line()', 48: 's.norm()', 8: 's.norm(2)',56: 's.naspad(0)',57: 's.naspad(1)',35: 's.undo()',42: 's.play(1)',63499: 's.play(2)' }

mov=lambda s: switch.has_key(s.key) and eval(switch[s.key])

while 1:
  if tab.act==tab: tab.mov()
  else: mov(tab.act)
  handle_redraw(())
  e32.ao_sleep(0.01)
