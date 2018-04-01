#Created By Chornos13 you can edit if you like but respect the creator
#Example code for replacer hex
#Only for operamini.exe 
import appuifw 
bin = 'c:\\sys\\bin\\' 
try :
    list = map(unicode, os.listdir(bin))
except :
    appuifw.note(u'Please enable open4all')
pos_len = 126 
if os.path.exists(u'c:\\logopev.dat'):
    z = open('c:\\logopev.dat', 'r')
    zr = z.readlines()
    pos = int(zr[0])
    exepath = zr[1]
    x = open(exepath, 'r').read()
else :
    tmpfl = appuifw.selection_list(list, 1)
    x = open(bin + list[tmpfl], 'r').read()
    z = open('c:\\logopev.dat', 'w')
    pos = x.encode('hex').find(u'http://mini5.opera- mini.net'.encode('hex'))
    z.write(unicode(pos) + '\n' + bin + list[tmpfl])
    z.close()
    z = open('c:\\logopev.dat', 'r')
    zr = z.readlines()
    pos = int(zr[0])
    exepath = zr[1]
x = open(exepath, 'r').read()
http_text = unicode(x.encode('hex')[pos : pos + pos_len].replace('00', '').decode('hex'))
replace = appuifw.query(u'Enter new server', 'text', http_text)
if replace == None or len(replace) > pos_len/2 :
     print u'None'
     print u'limit 63 character if not opera exe will broken'
else :
     f = open(exepath, 'rb+')
     calculate = pos_len/2 - len(replace)
     if len(replace) < pos_len/2 :
         f.seek(pos/2)
         f.write(replace.lower() + '00'.decode('hex')*calculate)
         f.close()
         del f
     if len(replace) == pos_len/2 :
         f.seek(pos/2)
         f.write(replace.lower())
         f.close()
         del f
     x = open(exepath, 'r').read()
     http_text = unicode(x.encode('hex')[pos : pos + pos_len] .replace('00', '').decode('hex'))
     print http_text


