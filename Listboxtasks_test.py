import e32,appuifw
from graphics import *
import geticon
import multimbm
import appswitch
import applist

limit=2
entries=[]
appuifw.app.title=u'Task List'
def listapps():
    global entries,limit
    lapp=applist.applist()
    ltask=appswitch.application_list(1)
    lapp1=[(el[1],el[0]) for el in lapp]
    lmbm=[]
    ltask1=[]
    c=0
    # puzzle image for app with no image associated
    uidpuz=0xa89fd974  
    puz2=geticon.get(uidpuz,(50,50))
    ipuz=Image.from_cfbsbitmap(puz2[0])
    mpuz=Image.from_cfbsbitmap(puz2[1])
    
    for el in ltask:
        luid=[u[1] for u in lapp1 if u[0]==el]
        if luid==[]: #app with no uid found
            i2=geticon.get(uidpuz,(50,50))
            ltask1.append((el,0))
        else:
            i2=geticon.get(luid[0],(50,50))
            ltask1.append((el,luid[0]))
        try: #app with no image -> puzzle default
            i=Image.from_cfbsbitmap(i2[0])
            imask=Image.from_cfbsbitmap(i2[1])
        except:
            i=ipuz 
            imask=mpuz 
            
        lmbm.append(i)
        lmbm.append(imask)
        c=c+1
    multimbm.create(u'd:\\itasks.mbm',lmbm)

    entries=[]
    s=0
    for task in ltask1:
        entries.append((task[0],unicode(hex(task[1])),appuifw.Icon(u'd:\\itasks.mbm',s,s+1)))
        s=s+2

app_lock = e32.Ao_lock() 

def exit():
  app_lock.signal()

def handle_sel():
    global entries
    global lb

    sel=appuifw.popup_menu([u'Switch',u'Kill'])
    if sel==0:#switch
        appswitch.switch_to_fg(entries[lb.current()][0])
    elif sel==1:#kill
        appswitch.kill_app(entries[lb.current()][0])
        display()    
    else:
        pass #cancel

def display():
  global entries
  global lb
  listapps()
  lb=appuifw.Listbox(entries,handle_sel)
  appuifw.app.body=lb


appuifw.app.menu=[(u'List Tasks',display)]

appuifw.app.exit_key_handler = exit

app_lock.wait()
