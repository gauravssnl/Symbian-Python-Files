'''WINFILE PLUGIN'''
#AIF plugin for WinFile
#It reads simply aif files. It reads only an image and display it.

#gira_schermo removed. Use ui.change_screen_mode(mode)

_plugin_version_=1.0
_winfile_version_=1.04
_description_=u'Plugin di WinFile che serve a visualizzare tutte le immagini contenute in un file .aif.'

import os

############################
#Classe per la gestione dei file aif
############################
#By Oper
#Edit by Snake87

import graphics, struct

class aiffile:
  def __init__(s):
    s.images=[]
    s.index=0

  def open(s,file,tmp="D:\\Temp.mbm"):
    s.__init__()
    txt = open(file).read()
    while 1:
      i = txt.find('(\x00\x00\x00')
      if (i < 4): break
      (l,) = struct.unpack('i', txt[(i - 4):i])
      if (l > 40):
        mbm = txt[(i - 4):((i - 4) + l)]
      else:
        txt = txt[(i + 4):]
        continue
      open(tmp, 'w').write(((('7\x00\x00\x10B\x00\x00\x10\x00\x00\x00\x009d9G' + struct.pack('i', (l + 20))) + mbm) + '\x01\x00\x00\x00\x14\x00\x00\x00'))
      try:
        img = graphics.Image.open(tmp)
      except:
        txt = txt[(i + 4):]
        continue
      s.images.append(img)
      txt = txt[((i - 4) + l):]
    try:
      del txt
      del mbm
      del l
      del img
    except:
      None
    try:
      os.remove(tmp)
    except:
      None
    if len(s.images)>0:
      return s.images
    else:
      return None

  def isaif(s,file):
    s.open(file)
    if len(s.images)>0:
      return True
    return False

  def next(s):
    if s.index==len(s.images)-1:
      s.index=0
    else:
      s.index+=1
    return s.images[s.index]

  def previous(s):
    if s.index==0:
      s.index=len(s.images)-1
    else:
      s.index-=1
    return s.images[s.index]
    
  def image(s,num):
    if num<0:
      s.index=0
      return s.images[s.index]
    if num>s.total():
      s.index=s.total()-1
      return s.images[s.index]
    s.index=num-1
    return s.images[s.index]

  def current(s):
    return s.index+1

  def total(s):
    return len(s.images)
############################

aiff=aiffile()
del aiffile


class init_plugin:
  def __init__(s,module,filename):
    globals().update(module)
    s.plugin_name=u"AIF Plugin"
    s.filename=filename
    s.content_of_dir=[]
    s.temp=u"D:\\AIF\\"
    s.data_file=directory.data_dir+"\\aif_plugin.dat"
    s.comp_type=1
    s.extractdir=os.path.splitext(filename)[0]+"\\"
    if not aiff.isaif(filename):
      user.note(u"File AIF danneggiato o non supportato!",s.plugin_name)
      plugins.plugin,plugins.active_plugin_name=None,None
      return
    s.remember(0)
    aiff.open(filename)
    if os.path.exists(s.temp):
      gestione_file.removedir(s.temp)
    os.makedirs(s.temp)
    i=1
    while i<aiff.total()+1:
      file=s.file_name(i)
      path=os.path.join(s.temp,file)
      s.content_of_dir.append((path,file,1))
      i+=1
    s.old_cbs=[ListBox.mode_cb,ListBox.sel_cb,ListBox.right_cb,ListBox.left_cb]
    ListBox.cbind()
    s.keys()
    ui.unbind(EKey0)
    ListBox.mode_cb=s.keys
    ListBox.left_cb=s.back_handler
    ListBox.right_cb=lambda:None
    ListBox.sel_cb=s.go
    ListBox.no_data=u"Il file AIF non contiene nessuna immagine oppure è danneggiato"
    ListBox.position,ListBox.page=0,0
    ui.menu.menu([(u"Estrai...",[(u"File singolo [2]",s.extract_one),(u"Tutto [8]",s.extract)]),(u"Tipo compressione [6]",[s.opzione_compressione]),(u"Dettagli AIF [5]",[s.info]),(u"Plugin Info",[s.about])]+main.exit_menu)
    s.set_list()

  def file_name(s,num):
    st=unicode(str(num))
    if num<10:
      st="0"+st
    if num<100:
      st="0"+st
    del num
    return u"image"+st+u".bmp"

  def about(s):
    user.note(s.plugin_name+u" by Snake87\nVisualizza tutte le immagini presenti nei file AIF\nVersion: "+to_unicode(str(_plugin_version_))+u"beta",s.plugin_name,-1)

  def info(s):
    d=time.localtime(os.path.getmtime(s.filename))
    d=u"%i/%i/%i %.2i:%.2i:%.2i"%(d[2],d[1],d[0],d[3],d[4],d[5])
    t=u'Immagini: %i\nDimensione: %s\n%s'%(aiff.total(),dataformatter.sizetostr(os.path.getsize(s.filename)),d)
    user.note(t,to_unicode(os.path.split(s.filename)[1]),timeout=-1)

  # def gira_schermo(s,num):
    # if ui.landscape!=num:
      # ui.switching_mode=1
      # ui.landscape=num
      # grafica.screen_change()
     # Schermo in landscape
      # if num:
        # ui.ui_image=Image.new((208,176))
        # ui.canvas_image=Image.new((208,176))
      # else:
        # ui.ui_image=Image.new((176,208))
        # ui.canvas_image=Image.new((176,208))
      # try:
        # if (ui.mode_callback!= None):
          # ui.mode_callback()
      # except Exception,e:
        # print ('Fatal Error in ui.mode_callback() in Multi-Bitmap Plugin:' + str(e))
      # ui.switching_mode=0

  def set_list(s,position=0):
    bakland=ui.landscape
    #s.gira_schermo(0)
    ui.change_screen_mode(0)
    d=progress_dialog(u"Caricamento file AIF in corso...",to_unicode(s.plugin_name+" - "+"0%"),max=len(s.content_of_dir))
    d.draw()
    ListBox.elements=[]
    ListBox.selected=[]
    titolo=os.path.split(s.filename)[1]
    titolo=to_unicode(titolo)
    i=1
    for path,name,type in s.content_of_dir:
      ListBox.elements.append(LType(name=to_unicode(name),undername=None,title=titolo,type=0,hid=0,icon=ext_util.search_path(name)[1]))
      d.set_title(to_unicode(s.plugin_name+" - "+str(i*100/aiff.total()))+u"%")
      d.forward()
      d.draw()
      i+=1
    d.close()
    del d
    #s.gira_schermo(bakland)
    ui.change_screen_mode(bakland)
    if len(ListBox.elements):
      ListBox.select_item(position)
    else:
      ListBox.redrawlist()

  def get_file(s):
    return s.content_of_dir[ListBox.current()][0]

  def get_name(s):
    return s.content_of_dir[ListBox.current()][1]

  def create_image(s):
    if not os.path.exists(s.temp+s.file_name(ListBox.current()+1)):
      s.imgtmp=aiff.image(ListBox.current()+1)
      s.imgtmp.save(s.temp+s.file_name(ListBox.current()+1)[:-4]+u".png")
      del s.imgtmp
      os.rename(s.temp+s.file_name(ListBox.current()+1)[:-4]+u".png",s.temp+s.file_name(ListBox.current()+1))

  def go(s):
    if len(s.content_of_dir)>0:
      s.create_image()

      class mod_viewer(mini_viewer):

        def next(self):
          if ListBox.current()<len(s.content_of_dir)-1:
            ListBox.position+=1
          else:
            ListBox.position=0
            ListBox.page=0
          s.create_image()
          self.file=s.get_file()
          self.name=s.get_name()
          e32.ao_sleep(0,self.carica_immagine)
          self.caricato=0
          self.create_image()
          self.redraw_img((),0)

        def previous(self):
          if ListBox.current()>0:
            ListBox.position-=1
          else:
            ListBox.position=len(s.content_of_dir)-1
          s.create_image()
          self.file=s.get_file()
          self.name=s.get_name()
          e32.ao_sleep(0,self.carica_immagine)
          self.caricato=0
          self.create_image()
          self.redraw_img((),0)

      
      mod_viewer(s.get_file(),s.restore_plugin_UI)

  def back_handler(s):
    if os.path.exists(s.temp):
      if len(os.listdir(s.temp))==0:
        s.tempo1=1
      else:
        s.tempo1=len(os.listdir(s.temp))
      bakland=ui.landscape
      ui.change_screen_mode(0)
      d=progress_dialog(u"Rimozione file temporanei in corso",s.plugin_name,max=s.tempo1)
      del s.tempo1
      d.draw()
      try:
        for c in os.listdir(s.temp):
          os.remove(s.temp+c)
          d.set_title(to_unicode(c))
          d.forward()
          d.draw()
        os.removedirs(s.temp)
        d.set_title(s.temp)
        d.forward()
        d.draw()
      except Exception,e:
        print str(e)
      d.close()
      ui.change_screen_mode(bakland)
    plugins.stop_module(1,s.restore)

  def keys(s):
    ui.bind(EKey5,s.info)
    ui.bind(EKey8,s.extract)
    ui.bind(EKey2,s.extract_one)
    ui.bind(EKey6,s.opzione_compressione)

  def opzione_compressione(s):
    s.comp_type=user.query(u"Scegliere il tipo di compressione per l'immagine.",s.plugin_name,left=u"PNG",right=u"JPG")
    s.remember(1)

  def remember(s,t):
    if t:
      try:
        open(s.data_file,'wb').write(chr(s.comp_type))
      except:
        pass
    else:
      try:
        s.comp_type=ord(open(s.data_file).read(1))
      except:
        pass

  def extract_one(s):
    if not user.query(u"Estrarre il file %s nella cartella %s"%(to_unicode(os.path.basename(s.get_file()))[:-4],to_unicode(s.extractdir)),s.plugin_name,left=u"Estrai"):
      return
    import sysinfo
    #molto approssimativa
    if os.path.getsize(s.filename)/aiff.total()>sysinfo.free_drivespace()[s.filename[0:2].capitalize()]:
      user.note(u"Spazio su disco insufficiente per continuare!\nEliminare qualche dato e riprovare",s.plugin_name)
      return
    d=progress_dialog(u"Estrazione immagine in corso...",u"Creazione cartella",max=1)
    d.draw()
    d.forward()
    if s.comp_type:
      d.set_title(to_unicode(os.path.basename(s.get_file()))[:-4]+".png")
    else:
      d.set_title(to_unicode(os.path.basename(s.get_file()))[:-4]+".jpg")
    d.draw()
    s.extract_file(ListBox.current()+1)
    d.close()
    user.note(u"Estrazione del file %s completata!"%(to_unicode(os.path.basename(s.get_file()))[:-4]),s.plugin_name)

  def extract(s):
    if not user.query(u"Estrarre il contenuto del file AIF nella cartella %s"%(to_unicode(s.extractdir)),s.plugin_name,left=u"Estrai"):
      return
    import sysinfo
    if os.path.getsize(s.filename)>sysinfo.free_drivespace()[s.filename[0:2].capitalize()]:
      user.note(u"Spazio su disco insufficiente per continuare!\nEliminare qualche dato e riprovare",s.plugin_name)
      return
    bakland=ui.landscape
    s.gira_schermo(0)
    d=progress_dialog(u"Estrazione immagini in corso...",u"Creazione cartella",max=aiff.total())
    i=1
    d.draw()
    while i<aiff.total()+1:
      d.forward()
      if s.comp_type:
        d.set_title(to_unicode(s.file_name(i)[:-4]+".png"))
      else:
        d.set_title(to_unicode(s.file_name(i)[:-4]+".jpg"))
      d.draw()
      s.extract_file(i)
      i+=1
    d.close()
    s.gira_schermo(bakland)
    user.note(u"Estrazione completata!",s.plugin_name)

  def extract_file(s,number):
    if not os.path.exists(s.extractdir):
      os.makedirs(s.extractdir)
    s.tempoimg=aiff.image(number)
    if s.comp_type:
      s.tempoimg.save(s.extractdir+s.file_name(number)[:-3]+u"png")
    else:
      s.tempoimg.save(s.extractdir+s.file_name(number)[:-3]+u"jpg")

  def restore(s):
    ListBox.mode_cb,ListBox.sel_cb,ListBox.right_cb,ListBox.left_cb=s.old_cbs

  def restore_plugin_UI(s,to_elem=None,ui_state=None):
    if ui_state:
      ui.set_state(ui_state)
    if ui.mode_callback!=None: ui.mode_callback()
    ListBox.select_item(ListBox.current())
    ui.unbind(EKey0)