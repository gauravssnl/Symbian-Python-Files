import e32,appuifw,os
from graphics import *
import geticon
import multimbm
import applist

limit=2
entries=[]

def listapps():
    global entries,limit
    lapp=applist.applist()
    lapp1=[(el[1],el[0]) for el in lapp]
    lmbm=[]
    entries=[]
    c=0
    uidno=0xa89fd974  
    puz2=geticon.get(uidno,(50,50))
    ipuz=Image.from_cfbsbitmap(puz2[0])
    mpuz=Image.from_cfbsbitmap(puz2[1])
    sd=0

    for el in lapp1:
        try:
            i2=geticon.get(el[1],(50,50))
        except:
            print  'p: ',el
        try:
            i=Image.from_cfbsbitmap(i2[0])
            imask=Image.from_cfbsbitmap(i2[1])
        except:
            print i2[0]
            i=ipuz 
            imask=mpuz 
            
        lmbm.append(i)
        lmbm.append(imask)
        entries.append((el[0],unicode(hex(el[1])),appuifw.Icon(u'd:\\iapps.mbm', sd,sd+1)))
        sd+=2
        c+=1
        if c>=limit: break

    multimbm.create(u'd:\\iapps.mbm',lmbm)
  

app_lock = e32.Ao_lock() 

def exit():
  app_lock.signal()

def display():
  global entries
  listapps()
  lb=appuifw.Listbox(entries,lambda:None)
  appuifw.app.body=lb

def setlimit():
  global limit
  limit=appuifw.query(u'limit','number',1)

appuifw.app.menu=[(u'list apps',display),(u'set limit',setlimit)]

appuifw.app.exit_key_handler = exit

app_lock.wait()
