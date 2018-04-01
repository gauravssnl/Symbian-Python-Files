from struct import*
from graphics import*
import os
wav='E:\\bird.wav'
X,Y=176,208
img=Image.new((X,Y))
Y/=2
t=open(wav)
h=t.read(44)
s=unpack('l',h[40:44])[0]
bit=unpack('h',h[34:36])[0]
dat=t.read()
t.close()

if bit==8: #for 8 bit
  num=[(128-(ord( dat[i])))*0.75 for i in xrange(s)]
elif bit==16: #for 16 bit
  num=[ (ord(dat[i]) !=255 and (ord(dat[i])>127 and ord(dat[i])-255 or ord(dat[i])))*0.75  for i in xrange(1,s,2) ]

xz=len(num)/X
if xz>2:
 lst=[[max(num[i:i+xz]),min(num[i:i+xz])] for i in range(0,len(num),xz) ] 
else:  
 lst=[[i,i] for i in num]
img.clear(0)
for i in range(len(lst)-1):
 img.line(( i,(lst[i][0]+Y),i,(lst[i+1][0]+Y) ,  i,(lst[i][1]+Y),i,(lst[i+1][1]+Y)),0x00bb00)
img.save(os.path.splitext(wav)[0]+'.png')
