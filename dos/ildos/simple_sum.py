#!/usr/bin/env python
import sys

#f = open('mae_ildos.xsf')
f = open(sys.argv[1])


# bohr
#L_x = 5.380370547;
#L_y = L_x;
#L_z = L_x * 6.268390298710899;

#delta_x = L_x/n_x*1000;
#delta_y = L_y/n_y*1000;
#delta_z = L_z/n_z*1000;

# discard line
for i in range(9):
	f.readline()

mae = 0
iline = 0
tline = f.readline()
while tline != '':
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
