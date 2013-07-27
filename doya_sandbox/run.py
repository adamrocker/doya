#!/usr/bin/env python
# -*- coding: utf-8 -*-

print "HELLO Sketch Boxel!"

NONE = ''
N = 3
WORLD = [[[NONE for i in range(N)] for j in range(N)] for k in range(N)]#空間配列

L = 2#辺の長さ
class Box:
    V = ((0,0,0),(1,0,0),(0,1,0),(1,1,0),(0,0,1),(1,0,1),(0,1,1),(1,1,1))
    F = ((1,3,2,1),(2,3,4,1),(1,5,3,2),(3,5,7,2),(3,7,4,3),(4,7,8,3),(1,2,5,4),(2,6,5,4),(2,4,6,5),(4,8,6,5),(5,6,7,6),(6,8,7,6))
    def __init__(self, point):
        self.point = point
        self.dirty = False
        self.face = None #共有面の番号

    def __str__(self):
        return 'BOX' + str(self.point)

    def __repr__(self):
        return str(self.point)

    #共有面の面番号を保存
    def addFace(self, index):
        if not self.face:
            self.face = [index]
        else:
            self.face.append(index)

    def around(self):
        p = self.point
        x = p[0]
        y = p[1]
        z = p[2]
        return [(x-1,y,z),(x,y-1,z),(x,y,z-1),(x+1,y,z),(x,y+1,z),(x,y,z+1)]

    def distance(self, box):
        b = self.point
        return (box.point[0] - b[0]) + (box.point[1] - b[1]) + (box.point[2] - b[2])

    def nearby(self, vect):
        d = self.distance(vect)
        if d == -1 or d == 1:
            return True
        else:
            return False

    def dump(self, file, number):
        b = self.point
        file.write('#v-{n}\n'.format(n=number))
        for i in Box.V:
            file.write("v {x} {y} {z}\n".format( x=((i[0]+b[0])*L), y=((i[1]+b[1])*L), z=((i[2]+b[2])*L) ))
            
        file.write('#f-{n}\n'.format(n=number))
        num = 8 * number
        for i in Box.F:
            faceIndex = i[3]
            if not self.face or faceIndex not in self.face:
                file.write("f {a}//{n} {b}//{n} {c}//{n}\n".format( a=(i[0]+num), b=(i[1]+num), c=(i[2]+num), n=(faceIndex)))

    @staticmethod
    def removeFace(box1, box2):
        p1 = box1.point
        p2 = box2.point
        vector = (p2[0]-p1[0], p2[1]-p1[1], p2[2]-p1[2])
        faceIndex = 0
        if vector == (1,0,0):
            faceIndex = 5
        elif vector == (0,1,0):
            faceIndex = 3
        elif vector == (0,0,1):
            faceIndex = 6
        elif vector == (-1,0,0):
            faceIndex = 2
        elif vector == (0,-1,0):
            faceIndex = 4
        elif vector == (0,0,-1):
            faceIndex = 1

        if 0 < faceIndex:
            print "faceIndex={i}/{box1}, {box2}".format(i=faceIndex, box1=box1, box2=box2)
            box1.addFace(faceIndex)
            box2.addFace(7 - faceIndex)

    @staticmethod
    def head(file, name):
        file.write('g {n}\n'.format(n=name))
        file.write('vn 0 0 -1\n')
        file.write('vn -1 0 0\n')
        file.write('vn 0 1 0\n')
        file.write('vn 0 -1 0\n')
        file.write('vn 1 0 0\n')
        file.write('vn 0 0 1\n')

#すべて一辺を１で考える（ENV配列を考慮して）
b1 = Box( (1,  1,  1 ) )
b2 = Box( (2,  1,  1 ) )
b3 = Box( (1,  1,  2 ) )
b4 = Box( (1,  2,  1 ) )
b5 = Box( (0,  1,  1 ) )
b6 = Box( (1,  1,  0 ) )
b7 = Box( (1,  0,  1 ) )
list = [b1,b2,b3,b4,b5,b6,b7]

#空間にboxを配置
for box in list:
    p = box.point
    WORLD[p[0]][p[1]][p[2]] = box

#共有面探索
for box in list:
    around = box.around()
    for i in around:
        x = i[0]
        y = i[1]
        z = i[2]
        if x < N and y < N and z < N:
            box2 = WORLD[i[0]][i[1]][i[2]]
            if box2 != NONE:
                Box.removeFace(box,box2)

file = open('tmp.obj', 'w')
Box.head(file, 'tmp')
for index,box in enumerate(list):
    box.dump(file, index)

file.close()
