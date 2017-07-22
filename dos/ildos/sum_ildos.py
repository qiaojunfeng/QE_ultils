#!/usr/bin/env python
import sys

#f = open('mae_ildos.xsf')
f = open(sys.argv[1])

iline = f.readline().strip()

while iline != 'DATAGRID_3D_UNKNOWN':
	iline = f.readline().strip()

iline = f.readline().strip()
tvec = [ int(i) for i in iline.split()]
n_x = tvec[0]
n_y = tvec[1]
n_z = tvec[2]

# discard
for i in range(4):
	f.readline()

# bohr
#L_x = 5.380370547;
#L_y = L_x;
#L_z = L_x * 6.268390298710899;

#delta_x = L_x/n_x*1000;
#delta_y = L_y/n_y*1000;
#delta_z = L_z/n_z*1000;

mae = 0
iline = 0
tline = f.readline()
while tline != 'END_DATAGRID_3D\n':
    tvec = [ float(t) for t in tline.strip().split() ]
    mae = mae + sum(tvec)
    tline = f.readline()
    iline = iline + 1
    print('iline = ' + str(iline))

f.close()

###

#BOHR_RADIUS_ANGS = 0.52917720858999995;
#RY_TO_EV = 13.605691930242388

#mae = mae * (L_x*L_y*L_z);
#mae = mae / (n_x*n_y*n_z)

# final unit is meV
#mae = mae * 1000 * RY_TO_EV
print( 'mae form ldos = ' + str(mae) + ' meV\n')
