import txtfield,e32,appuifw

canvas=appuifw.Canvas()
appuifw.app.screen="full"
appuifw.app.body=canvas
canvas.clear(0)

def preview(path):
    font=txtfield.LoadFont(path)
    txt=txtfield.New((5,5,170,150),cornertype=txtfield.ECorner5)
    txt.textstyle(u'LatinBold13',size=250,style=u'normal',color=0x225522)
    txt.add(unicode(str(copyright)))
    e32.ao_sleep(2)
    txt.textstyle(u'LatinPlain12',size=250,style=u'normal',color=0x225522)
    txt.add(unicode(str(copyright)))
    e32.ao_sleep(2)
    txt.textstyle(u'LatinBold19',size=250,style=u'normal',color=0x225522)
    txt.add(unicode(str(copyright)))
    e32.ao_sleep(2)
    del txt
    print font
    txtfield.RemoveFont(font)
    e32.ao_sleep(0.6)
    
preview(u"e:\\aquaduct.gdr")
