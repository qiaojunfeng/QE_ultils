#!/usr/bin/env python
import sys

thr = 1e-70

f = open(sys.argv[1])

iline = f.readline()  # discard 1st line
iline = f.readline()

while iline != '':
  tvec = [ float(i) for i in iline.split()]
  e = tvec[0]
  dos = tvec[1]
  #print(e, dos)
  if abs(dos) > thr:
  	break
  iline = f.readline()

emin = e - 1    # with 1 eV margin
print(emin)
