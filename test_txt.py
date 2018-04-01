import txtfield, appuifw, lang

def ru(x): return x.decode('utf-8')

class Main:
    def __init__(s):
        s.ws_cb=s.ws_cb
        s.lock=appuifw.e32.Ao_lock()
        appuifw.app.exit_key_handler=s.lock.signal
        appuifw.app.body.clear()
        s.a=[]
        
    def lb_cb(s, a):
        pass
    
    def start(s):
        lang.set_predicative_input(0)
        s.window_search = txtfield.New(
            (90, 295, 150, 320), 
            txtlimit = 7, 
            callback = s.ws_cb)
        s.window_search.visible(1)
        s.window_search.focus(1) 
        s.lb=appuifw.Listbox([ru('мама'), ru('папа'), ru('сестра')], s.lb_cb)
        appuifw.app.body=s.lb


    def ws_cb(s, val):
        g=s.window_search.get()
        s.a.append([g,val])
    
main = Main()
main.start()
main.lock.wait()
print main.a
main.window_search.visible(0)
main.window_search.focus(0)
