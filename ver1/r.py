import random

random.seed(a=0)

timing=open('obless_noob - mute (SCORE V2 SUCKS) [timing].osu','r')
pos=open('obless_noob - mute (SCORE V2 SUCKS) [position].osu','r')

rand=open('obless_noob - mute (SCORE V2 SUCKS) [random].osu','w')

while True:
    i=timing.readline()
    if 'Version:' in i:
        rand.write('Version:random\n')
        continue
    rand.write(i)
    if '[HitObjects]' in i:break

while True:
    i=pos.readline()
    if '[HitObjects]' in i:break

poslist=[]

while True:
    i=pos.readline()
    if not i:break
    poslist.append(i.split(',',maxsplit=2)[0:2])

timelist=[]

while True:
    i=timing.readline()
    if not i:break
    timelist.append(i.split(',',maxsplit=2)[2])

i=0

p=0

while True:
    if i >= len(timelist):break
    r=random.random()
    if r<0.33:
    #五连
        if i <= len(timelist)-5:
            for a in range(5):
                rand.write(f'{poslist[p][0]},{poslist[p][1]},{timelist[i]}')
                i+=1
                p+=1
                if p < 0:p += len(poslist)
                if p >= len(poslist):p -= len(poslist)
            i+=1
            p+=16
            if p < 0:p += len(poslist)
            if p >= len(poslist):p -= len(poslist)
            continue
    if r<0.67:
    #三连
        if i <= len(timelist)-3:
            for a in range(3):
                rand.write(f'{poslist[p][0]},{poslist[p][1]},{timelist[i]}')
                i+=1
            i+=1
            p+=18
            if p < 0:p += len(poslist)
            if p >= len(poslist):p -= len(poslist)
            continue
    rand.write(f'{poslist[p][0]},{poslist[p][1]},{timelist[i]}')
    i+=2
    p+=18
    if p < 0:p += len(poslist)
    if p >= len(poslist):p -= len(poslist)



timing.close()
pos.close()
rand.close()
