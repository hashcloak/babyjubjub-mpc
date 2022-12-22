import sys
sys.path.append("../MP-SPDZ")
from Compiler.types import sint
from random import randrange
from py_ecc.fields import bn128_FQ

## Constants
### Generator for babyjubjub curve
x = bn128_FQ(995203441582195749578291179787384436505546430278305826713579947235728471134)
y = bn128_FQ(5472060717959818805561601436314318772137091100104008585924551046643952123905)

## Babyjubjub parameters
a = 168700
d = 168696

## prime
q = 21888242871839275222246405745257275088548364400416034343698204186575808495617


class Point:
    def __init__(self, point):
        self.x, self.y = point

def point_add(point1, point2):
    if point1.x == 0 and point1.y == 0:
        return point2

    if point2.x == 0 and point2.y == 0:
        return point1
        
    x3 = (point1.x * point2.y + point1.y * point2.x) / (1 + (d * point1.x * point1.y * point2.x * point2.y))
    y3 = (point1.y*point2.y - a*point1.x*point2.x) / (1 - (d *point1.x * point1.y * point2.x * point2.y))
    return Point((x3, y3))

def double(point):
    return point_add(point, point)

def scalar_multiplication(scalar, point):
    px = point.x
    py = point.y
    ap = Point((0, 0))

    rem = scalar
    while(rem != 0):
        if ((rem & 1) != 0):
            ap = point_add(ap, point)
        point = double(point)

        rem //= 2

    return ap


generator = Point((x,y))

if __name__ == '__main__':
    for i in range(3):
        with open("./MP-SPDZ/Programs/Public-Input/babyjubjub", "w") as f:
            f.write("{}".format(a))
        with open("Player-Data/Input-P{}-0".format(i), 'w+') as f:
            r = randrange(0, q)
            R = scalar_multiplication(r, generator)
            aR = scalar_multiplication(a, R)
            f.write("{} {}\n{} {}".format(R.x, R.y, aR.x, aR.y))