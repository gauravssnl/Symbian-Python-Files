import TopWindow
from graphics import*
import appuifw, e32, asprite, time

screen = TopWindow.TopWindow()
img=Image.new((150, 60))
img.clear(0xddddde)
screen.add_image(img, (0,0))
screen.size = (150, 60)
screen.position=(30, 10)
screen.shadow = 3
screen.show()

sprite=asprite.New()
pic=Image.new((100,30))
pic_mask=Image.new((100,30))

h,m,s=time.localtime()[3:6]
pic.clear(0xddaa22)
pic.text((10,20),u'%02d:%02d:%02d'%(h,m,s),0x227722,font='title')
pic_mask.clear(0xffffff)
pic_mask.text((10,20),u'%02d:%02d:%02d'%(h,m,s),font='title')

s1=sprite.load_cadre(pic,pic_mask, [(0,0)], [100,30])
win=sprite.NewSprite(s1,1)
sprite.target(win,(50,30))
sprite.activate()

def exit_key_handler():
    app_lock.signal()

app_lock = e32.Ao_lock()

appuifw.app.exit_key_handler = exit_key_handler
app_lock.wait()

del screen, sprite