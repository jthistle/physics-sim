#!/usr/bin/env python3

from objects import Fraction

a = Fraction(4, 1)

b = Fraction(1, 2)

print(a)
print(b)

c = a + b
print(c)

d = Fraction(1.5, 6)
print(d)

# 9/2 * 1/4
e = c * d
print(e)

f = e / Fraction(5, 4)
print(f)

g = f + 1
print(g)

h = g ** 2
print(h)

i = h * 3.4
print(i)