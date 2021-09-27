import random
from math import log, sin, pi



MIN_X=0
MAX_X=512
MIN_Y=0
MAX_Y=384

X_GRID=96
Y_GRID=round(X_GRID * sin(pi / 3))




#Direction.n 范围0~5，0指向右，每加一向逆时针方向旋转60度
class Direction:
    def simplify(self):
        while self.n > 5:self.n -= 6
        while self.n < 0:self.n += 6
    
    def __init__(self, n = 0):
        self.n = n
        self.simplify()
    
    def __add__(self, other):
        return Direction(self.n + other.n)
    
    def rotate(self, n = 0):
        return self + Direction(n)
    
    def __sub__(self, other):
        return Direction(self.n - other.n)
    
class Pos:
    def __init__(self, x = 256, y = 192):
        self.x = round(x)
        self.y = round(y)
    
    def isinfield(self):
        if self.x > MAX_X or self.x < MIN_X or self.y > MAX_Y or self.y < MIN_Y:return False
        return True
    
    def __add__(self, other):
        return Pos(self.x + other.x, self.y + other.y)
    
    def __mul__(self, other):
        return Pos(self.x * other, self.y * other)
    
    def __rmul__(self, other):
        return Pos(self.x * other, self.y * other)
    
    def __truediv__(self, other):
        return Pos(self.x / other, self.y / other)
    
    def step(self, d, times = 1):
        if d.n == 0:return self + Pos(X_GRID * times, 0)
        if d.n == 1:return self + Pos(X_GRID * times / 2, Y_GRID * times)
        if d.n == 2:return self + Pos(-X_GRID * times / 2, Y_GRID * times)
        if d.n == 3:return self + Pos(-X_GRID * times, 0)
        if d.n == 4:return self + Pos(-X_GRID * times / 2, -Y_GRID * times)
        if d.n == 5:return self + Pos(X_GRID * times / 2, -Y_GRID * times)

#176.47 bpm ar 9
def randmapgen(seed = 0, leng = 85, armul = 1, total = 4096):
    
    random.seed(a = seed)
    beatlength = leng * 4
    ar = '%.2f' % ((1200 - leng / 85 * 600) / 750 * 5 + 5)
    od = '%.2f' % ((1200 - leng / 85 * 600) / 750 * 5 + 4)
    version = 'NC %.3fBPM seed %d' % (90000 / beatlength, seed)
    
    file = open(f'obless_noob - mute (SCORE V2 SUCKS) [{version}].osu','w')
    file.write(r'''osu file format v14
[General]
AudioFilename: audio.mp3
AudioLeadIn: 0
PreviewTime: -1
Countdown: 0
SampleSet: Soft
StackLeniency: 0.7
Mode: 0
LetterboxInBreaks: 0
WidescreenStoryboard: 1

[Editor]
DistanceSpacing: 1
BeatDivisor: 4
GridSize: 32
TimelineZoom: 3

[Metadata]
Title:mute
TitleUnicode:mute
Artist:obless_noob
ArtistUnicode:obless_noob
Creator:SCORE V2 SUCKS
Version:''')
    file.write(f'{version}\n')
    file.write(r'''Source:
Tags:
BeatmapID:0
BeatmapSetID:-1

[Difficulty]
HPDrainRate:6
CircleSize:4
''')
    file.write(f'''OverallDifficulty:{od}
ApproachRate:{ar}
''')
    file.write(f'SliderMultiplier:{X_GRID * 0.02}\n')
    file.write(r'''SliderTickRate:1

[Events]

[TimingPoints]

''')
    file.write(f'0,{beatlength},4,2,0,100,1,0\n\n')
    file.write('[HitObjects]\n')

    i = 0
    d = Direction(random.randint(0,5))
    p = Pos()
    
    def writecircle(x, y, time, nc = 0, hs = ['0', '0:0:0:0:']):
        file.write(f'{x},{y},{time},{1 + nc * 4},{hs[0]},{hs[1]}\n')
        nonlocal i
        i += 1

    def writeslider(x1, y1, x2, y2, time, nc = 0, hs1 = ['0', '0:0:0:0:'], hs2 = ['0', '0:0:0:0:']):
        file.write(f'{x1},{y1},{time},{2 + nc * 4},0,L|{x2}:{y2},1,{X_GRID},{hs1[0]}|{hs2[0]},{hs1[1]}|{hs2[1]},0:0:0:0:\n')
        nonlocal i
        i += 3

    def autohs(n):
        return (['4', '0:0:0:0:'] if n % 64 == 0 else ['2', '0:0:0:0:'] if n % 8 == 0 else ['8', '0:0:0:0:'] if n % 8 == 4 else ['2', '0:0:0:0:'] if n % 16 == 10 else ['0', '0:0:0:0:'])

    while True:
        if i > total:break
        r = random.random()
        if r < 1 / 6:#五连+滑条
            if i <= total - 8 and i % 4 == 0:
                r1 = Direction(random.choice([2, 4]))
                r2 = Direction(random.choice([0, 1, 5]))
                r3 = Direction(random.choice([0, 1, 3, 5]))
                p0 = p
                d1 = d + r1
                p1 = p.step(d1)
                d2 = d1 + r2
                p2 = p1.step(d2)
                d3 = d2 + r3
                p3 = p2.step(d3, 2)
                if p1.isinfield() and p2.isinfield() and p3.isinfield():
                    writecircle(x = p.x, y = p.y, time = i * leng, nc = (1 if i % 8 == 0 else 0), hs = autohs(i))
                    p = (p0 * 3 + p1) / 4
                    writecircle(x = p.x, y = p.y, time = i * leng, nc = (1 if i % 8 == 0 else 0), hs = autohs(i))
                    p = (p0 + p1) / 2
                    writecircle(x = p.x, y = p.y, time = i * leng, nc = (1 if i % 8 == 0 else 0), hs = autohs(i))
                    p = (p0 + p1 * 3) / 4
                    writecircle(x = p.x, y = p.y, time = i * leng, nc = (1 if i % 8 == 0 else 0), hs = autohs(i))
                    writeslider(x1 = p1.x, y1 = p1.y, x2 = p2.x, y2 = p2.y, time = i * leng, nc = (1 if i % 8 == 0 else 0), hs1 = autohs(i), hs2 = autohs(i + 2))
                    d = d3
                    p = p3
                    i += 1
                    continue
        elif r < 2 / 6:#三连+滑条
            if i <= total - 6:
                r1 = Direction(random.choice([0, 1, 2, 3, 4, 5]))
                r2 = Direction(random.choice([0, 1, 3, 5]))
                p0 = p
                d1 = d + r1
                p1 = p.step(d1)
                d2 = d1 + r2
                p2 = p1.step(d2, 2)
                if p1.isinfield() and p2.isinfield():
                    writecircle(x = p0.x, y = p0.y, time = i * leng, nc = (1 if i % 8 == 0 else 0), hs = autohs(i))
                    writecircle(x = p0.x, y = p0.y, time = i * leng, nc = (1 if i % 8 == 0 else 0), hs = autohs(i))
                    writeslider(x1 = p0.x, y1 = p0.y, x2 = p1.x, y2 = p1.y, time = i * leng, nc = (1 if i % 8 == 0 else 0), hs1 = autohs(i), hs2 = autohs(i + 2))
                    d = d2
                    p = p2
                    i += 1
                    continue
        elif r < 3 / 6:#滑条
            if i <= total - 2:
                r1 = Direction(random.choice([0, 1, 2, 3, 4, 5]))
                r2 = Direction(random.choice([0, 1, 3, 5]))
                p0 = p
                d1 = d + r1
                p1 = p.step(d1)
                d2 = d1 + r2
                p2 = p1.step(d2, 2)
                if p1.isinfield() and p2.isinfield():
                    writeslider(x1 = p0.x, y1 = p0.y, x2 = p1.x, y2 = p1.y, time = i * leng, nc = (1 if i % 8 == 0 else 0), hs1 = autohs(i), hs2 = autohs(i + 2))
                    p = p2
                    d = d2
                    i += 1
                    continue
        elif r < 4 / 6:#五连
            if i <= total - 4 and i % 4 == 0:
                r1 = Direction(random.choice([2, 4]))
                r2 = Direction(random.choice([2, 4]))
                p0 = p
                d1 = d + r1
                p1 = p.step(d1)
                d2 = d1 + r2
                p2 = p1.step(d2, 2)
                if p1.isinfield() and p2.isinfield():
                    writecircle(x = p.x, y = p.y, time = i * leng, nc = (1 if i % 8 == 0 else 0), hs = autohs(i))
                    p = (p0 * 3 + p1) / 4
                    writecircle(x = p.x, y = p.y, time = i * leng, nc = (1 if i % 8 == 0 else 0), hs = autohs(i))
                    p = (p0 + p1) / 2
                    writecircle(x = p.x, y = p.y, time = i * leng, nc = (1 if i % 8 == 0 else 0), hs = autohs(i))
                    p = (p0 + p1 * 3) / 4
                    writecircle(x = p.x, y = p.y, time = i * leng, nc = (1 if i % 8 == 0 else 0), hs = autohs(i))
                    p = p1
                    writecircle(x = p.x, y = p.y, time = i * leng, nc = (1 if i % 8 == 0 else 0), hs = autohs(i))
                    p = p2
                    d = d2
                    i += 1
                    continue
        elif r < 5 / 6:#三连
            if i <= total - 2:
                r1 = Direction(random.choice([2, 4]))
                d1 = d + r1
                p1 = p.step(d1, 2)
                if p1.isinfield():
                    writecircle(x = p.x, y = p.y, time = i * leng, nc = (1 if i % 8 == 0 else 0), hs = autohs(i))
                    writecircle(x = p.x, y = p.y, time = i * leng, nc = (1 if i % 8 == 0 else 0), hs = autohs(i))
                    writecircle(x = p.x, y = p.y, time = i * leng, nc = (1 if i % 8 == 0 else 0), hs = autohs(i))
                    d = d1
                    p = p1
                    i += 1
                    continue
        else:#单点
            if i <= total:
                r1 = Direction(random.choice([2, 4]))
                d1 = d + r1
                p1 = p.step(d1, 2)
                if p1.isinfield():
                    writecircle(x = p.x, y = p.y, time = i * leng, nc = (1 if i % 8 == 0 else 0), hs = autohs(i))
                    d = d1
                    p = p1
                    i += 1
                    continue
    return


randmapgen()
