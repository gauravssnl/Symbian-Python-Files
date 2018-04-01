# coding: utf-8
'''import appuifw, txtfield
appuifw.app.body.clear()
itimer=appuifw.e32.Ao_timer()

lock=appuifw.e32.Ao_lock()
itimer.after(15, lock.signal)
flag=1
list = [unicode(i) for i in range(10)]
def cb():
    pass

def cb1():

    print 1
    global flag
    if flag:
        search.visible(1)
        search.focus(1)
        flag=0
    appuifw.e32.ao_sleep(1)
    a=search.get()
    print type(a), len(a), a
    if len(a)==0:
        flag=1
    return
    if flag is 0:
        appuifw.e32.ao_sleep(1, cb1)
    
    
lb = appuifw.Listbox(list, cb)
for i in [42, 35, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57]:
    lb.bind(i, cb1)
appuifw.app.body = lb

search = txtfield.New((0, 0, 100, 50))
search.visible(0)
search.focus(0)


appuifw.app.exit_key_handler = lock.signal
lock.wait()
#print search.get()
search.visible(0)
search.focus(0)
flag=1
'''
import _progressnotes as progressnotes, e32
note = progressnotes.ProgressNote()
def cancel():
    print "cancel"
note.cancel_callback(cancel)

note.wait()
note.update(0, u"please wait")
e32.ao_sleep(5)
note.finish()
#['cancel_callback', 'finish', 'progress', 'update', 'wait']

note.progress(6)
for i in range(1,7):
    note.update(i, u"progress %d"%i)
    e32.ao_sleep(0.5)
note.finish()

