import audio,appuifw2,os
class classsounds:
  def __init__(self,name="C:\\data_audio.txt"):
    self.name=name
    if os.path.isfile(name):
      self.allmark=eval(open(name,"r").read())
    else:
      self.allmark=[0,0L,None,None]
      #allmark=[UiPosition,CurrentSoundPosition,SoundPath,SoundName]
    dir="E:\\Sounds\\"
    alist=os.listdir(dir)
    sounditem=[appuifw2.Item(title=u"%02d. %s"%(it,alist[it]),soundpath="%s%s"%(dir,alist[it])) for it in xrange(len(alist)) if os.path.isfile(dir+alist[it]) and alist[it].lower().endswith("mp3")]
    del dir,alist
    self.amount=len(sounditem)
    appuifw2.app.title=u"ListBox2"
    appuifw2.app.navi_text=u"None"
    appuifw2.app.body=self.AuMain=appuifw2.Listbox2(sounditem,select_callback=self.select_playing)
    del sounditem
    appuifw2.app.exit_key_handler=self.exqt

  def state(self):
    #self.allmark=[UiPosition,CurrentSoundPosition,SoundPath,SoundName]
    if self.allmark[2]!=None and os.path.isfile(self.allmark[2]):
      self.AuMain.set_current(self.allmark[0])
      self.isvalidfile(self.allmark[2],self.allmark[3],self.allmark[0],self.allmark[1])
    else:self.nextitem()

  def select_playing(self):
    pos=self.AuMain.current()
    index=self.AuMain.current_item()
    navi_title=index.title
    path=index.soundpath
    if path.lower()==self.allmark[2].lower():
      if not self.isvalidsobj():
        self.isvalidfile(path,navi_title,uipos=pos,manual=True)
      elif self.isvalidsobj() is 1:
        self.soundobj.set_position(self.soundposition)
        self.soundobj.play()
        appuifw2.app.title=u"Playing:"
      elif self.isvalidsobj() is 2:
        self.soundposition=self.soundobj.current_position()
        self.soundobj.stop()
        self.changedata([(1,self.soundposition)])
        appuifw2.app.title=u"Pause:"
    else:
      self.isvalidfile(path,navi_title,uipos=pos,manual=True)

  def isvalidfile(self,path,navi_title,uipos=0,soundposition=0L,manual=False):
    try:
      if manual:
        self.backupobj=audio.Sound.open(path)
      else:
        self.soundobj=audio.Sound.open(path)
    except:
      appuifw2.note(u"file corrupt,or file not exists!","error")
      return
    self.continuework(path,navi_title,uipos,soundposition,manual)

  def close(self):
    try:
      self.soundobj.close()
    except:self.soundobj=None

  def isvalidsobj(self):
    try:
      return self.soundobj.state()
    except:return False

  def nextitem(self):
    if self.allmark[0]>=self.amount-1:
      pos=0
    else:pos=self.allmark[0]+1
    self.AuMain.set_current(pos)
    index=self.AuMain.current_item()
    self.isvalidfile(path=index.soundpath,navi_title=index.title,uipos=pos)

  def callselect(self,state,current,error):
    if state is 2:
      self.close()
      appuifw2.e32.ao_sleep(0,self.nextitem)
    pass

  def continuework(self,path,navi_title,uipos,soundposition,manual):
    if manual:
      self.close()
      self.soundobj=self.backupobj;del self.backupobj
    if soundposition:
      self.soundobj.set_position(soundposition)
    try:
      self.soundobj.set_volume(1)
      self.soundobj.play(callback=self.callselect)
    except:
      appuifw2.note(u"file corrupt!","error")
      return
    appuifw2.app.title=u"Playing:"
    appuifw2.app.navi_text=u"%s"%navi_title[:22]
    self.changedata([(0,uipos),(1,soundposition),(2,path),(3,navi_title)])

  def changedata(self,ar):
    for key,value in ar:
      self.allmark[key]=value
    open(self.name,"w").write("%s"%self.allmark)

  def exqt(self):
    if self.isvalidsobj():
      self.changedata([(1,self.soundobj.current_position())])
      self.close()
    appuifw2.app.set_exit()

if __name__=="__main__":
  sounds=classsounds()
  appuifw2.e32.ao_sleep(0,sounds.state)
  del sounds