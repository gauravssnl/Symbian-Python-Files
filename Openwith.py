import appuifw,sys,os,tarfile
file=sys.argv
if not len(file)>1:
 appuifw.note(u"Please use open with")
 os.abort()
else:
 t=tarfile.open(file[1])
 o=[]
 for i in t.getmembers():
  o.append(unicode(i.name))
 appuifw.popup_menu(o)
 os.abort()