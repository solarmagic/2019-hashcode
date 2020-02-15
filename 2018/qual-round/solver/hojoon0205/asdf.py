inputfilename = input()
f = open("../../input/" + inputfilename + ".in", 'r')
lines = f.readlines()
#print(len(lines))

infos = lines[0].split()
for i in range(len(infos)):
    infos[i] = int(infos[i])

R = infos[0]
C = infos[1]
F = infos[2]
N = infos[3]
B = infos[4]
T = infos[5]

class Ride:
    def __init__(self, a, b, x, y, s, f, idx):
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        self.s = s
        self.f = f
        self.idx = idx
        self.d = self.dist()
        self.e = self.lastOrder()
        assert(self.e >= self.s)

    def dist(self):
        return abs(self.x - self.a) + abs(self.y - self.b)

    def lastOrder(self):
        return self.f - self.dist()

class Taxi:
    def __init__(self, x, y, t):
        self.x = x
        self.y = y
        self.t = t
        self.Rs = []

def dist(ax, ay, bx, by):
    return abs(ax-bx)+abs(ay-by)

rides = []

cnt = 0
for line in lines:
    cnt += 1
    if cnt == 1:
        continue
    l = line.split(' ')
    for i in range(len(l)):
        l[i] = int(l[i])
    
    rides.append( Ride(l[0], l[1], l[2], l[3], l[4], l[5], cnt-2) )

f.close()
rides.sort(key=lambda r: r.e)

taxis = []
for i in range(F):
    taxis.append( Taxi(0, 0, 0) )

for ride in rides:
    idx = -1
    for i in range(F):
        nexttime = taxis[i].t + dist(ride.a, ride.b, taxis[i].x, taxis[i].y)
        if nexttime <= ride.e:
            if idx < 0:
                idx = i
            elif nexttime <= ride.s:
                idx_nexttime = taxis[idx].t + dist(ride.a, ride.b, taxis[idx].x, taxis[idx].y)
                if idx_nexttime > ride.s:
                    idx = i
                elif idx_nexttime < nexttime:
                    idx = i
            else:
                idx_nexttime = taxis[idx].t + dist(ride.a, ride.b, taxis[idx].x, taxis[idx].y)
                if idx_nexttime > nexttime:
                    idx = i
    if idx == -1:
        continue
    
    taxis[idx].Rs.append( ride.idx )
    nexttime = taxis[i].t + dist(ride.a, ride.b, taxis[i].x, taxis[i].y)
    if nexttime>=ride.s:
        taxis[idx].t = nexttime + ride.d
    else:
        taxis[idx].t = ride.s + ride.d

for taxi in taxis:
    print(len(taxi.Rs), *taxi.Rs, sep=' ')