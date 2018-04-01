from lite_fm import *
import os
import e32
import appuifw
import uikludges
def copy(x, y):
    e32.file_copy(x, y)
    print ('copy ' + y + '\r\nin ' + x + '\r\n'),
    print
    e32.ao_yield()


def en(x):
    return x.decode('utf-8')


def Exit():
    x = appuifw.query(en('Are you sure?'), 'query')
    if x == 1 : 
        os.abort()


uikludges.set_right_softkey_text(en('Exit'))
appuifw.app.screen = 'normal'
appuifw.app.title = u'py2sis'
priv = en('While processing please be patient\nIt may take 2-3 minutes..\n\n\n\n\nby Gabriel\n\n@\n\nwww.roznida.com')
appuifw.app.body = appuifw.Text()
appuifw.app.body.color = (0, 0, 0)
appuifw.app.body.set(priv)
appuifw.app.body.focus = False
def exit_key_handler():
    create


def create():
    apps = manager('e:/system/apps', 'dir')
    if apps == None : 
        return 'Program not selected'
    appuifw.note(en('Please Wait...'))
    if len(os.path.split(apps)[1]) > 10 : 
        return 'name programs is long'
    apps += '\\'
    if  not os.path.exists((apps + 'default.py')) : 
        return 'default.py not exists'
    os.makedirs((apps + 'libs\\encodings'))
    for drive in ['c:\\system\\', 'e:\\system\\']:
        for dll in [('python222.dll', 'libs\\python222.dll'), ('python_appui.dll', 'libs\\python_appui.dll'), ('ui.rsc', 'data\\appuifwmodule.rsc')]:
            if os.path.exists((drive + dll[1])) : 
                copy((apps + dll[0]), (drive + dll[1]))
        for path in ['libs\\', 'libs\\encodings\\']:
            try :
                sp = os.listdir((drive + path))
            except :
                continue
            for name in sp:
                name = name.lower()
                if os.path.splitext(name)[1] in ['.py', '.pyc', '.pyd'] : 
                    copy((apps + path + name), (drive + path + name))
    f = open((apps + 'python_appui.dll'), 'r+')
    txt = f.read()
    i = txt.find('\x00'.join(list('data\\appuifwmodule.rsc')))
    f.seek(i)
    nt = '\x00'.join(list(('apps\\' + os.path.split(apps[ : -1])[1] + '\\ui.rsc')))
    nt += (((43 - len(nt)) / 2) * '\x00 ')
    (f.write(nt), f.close())
    f = open((apps + 'default.py'), 'r+')
    txt = f.read()
    f.seek(0)
    apps = (apps[1 : -1]).replace('\\', '\\\\')
    f.write(('import sys\r\nsys.path=["c' + apps + '","e' + apps + '","c' + apps + '\\\\libs","e' + apps + '\\\\libs"]\r\n' + txt))
    appuifw.note(en('Finished'))
    f.close()
    return 'ok'


print create(),
print
appuifw.app.menu = [(en('py2sis'), create)]
appuifw.app.exit_key_handler = Exit
