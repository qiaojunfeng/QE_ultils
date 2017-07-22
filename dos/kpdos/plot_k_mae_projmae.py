#!/usr/bin/env python
import sys

#f_par = 'eband_par.dat.eband_k.dat'
#f_per = 'eband_per.dat.eband_k.dat'
f_par = sys.argv[1]
f_per = sys.argv[2]


nk_x = 20
nk_y = 20
nk_z = 1
nkpt = nk_x*nk_y*nk_z

f = open(f_par)

tline = f.readline()    # discard header
tline = f.readline()    # discard header
tline = f.readline()    # discard header

tline = f.readline()
ik = 0

sumpar_k = [ 0 for i in range(nkpt) ]

while tline != '':
    sumpar_k[ik] = float(tline.strip())
    print('ik = ' + str(ik+1))
    ik = ik + 1
    tline = f.readline()

f.close()

###

f = open(f_per);

sumper_k = [ 0 for i in range(nkpt) ]

tline = f.readline()    # discard header
tline = f.readline()    # discard header
tline = f.readline()    # discard header

tline = f.readline()
ik = 0

while tline != '':
    sumper_k[ik] = float(tline.strip())
    print('ik = ' + str(ik+1))
    ik = ik + 1
    tline = f.readline()

f.close()

###

mae_k = [(sumpar_k[i] - sumper_k[i]) for i in range(nkpt)]
mae = sum(mae_k)

# BOHR_RADIUS_ANGS= 0.52917720858999995;

# final unit is meV

f_kpts = 'kpts'
f = open(f_kpts)

ik = 0
# for mae_k_order, origin is at left down corner, x horizontal, y vertical
mae_k_order = [ [ 0 for i in range(nk_x) ] for i in range(nk_y) ]
indxy = []

for iline in f:
    iline = iline.strip()
    tvec = iline.split()
    kx = float(tvec[4])
    ky = float(tvec[5])
    iy = int(nk_x/2 + kx * nk_x)
    ix = int(nk_y/2 + ky * nk_y)
    indxy.append([ix, iy])
    mae_k_order[ix][iy] = mae_k[ik]
    ik = ik + 1


f_save = 'mae_k.dat'
f = open(f_save, 'w')

# store first five biggest mae_k and index
f.write('sum(mae_k) = ' + str(mae) + ' meV\n')
f.write('first five biggest mae_k in matrix' + '\n')
f.write('([ix,iy] is the [row,col] index of matrix, origin is [0,0] at left bottom corner, y increase from bottom to top' + '\n')
inds = sorted(range(len(mae_k)), key=lambda x: mae_k[x], reverse=True)
for i in range(5):
    f.write('kpt: ' + str(inds[i]+1) + 
        ', [ix,iy] = ' + str(indxy[inds[i]]) + 
        ', mae_k = ' + str(mae_k[inds[i]]) + '\n')

f.write('first five smallest mae_k in matrix' + '\n')
for i in range(len(inds)-1, len(inds)-6, -1):
    f.write('kpt: ' + str(inds[i]+1) + 
        ', [ix,iy] = ' + str(indxy[inds[i]]) + 
        ', mae_k = ' + str(mae_k[inds[i]]) + '\n')


# store matrix
for i in range(nk_x):
    for j in range(nk_y):
        f.write(str(mae_k_order[i][j]) + ' ')
    f.write('\n')

f.close()

#!/usr/bin/env python

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib import rc

f_save = 'mae_k.dat'
f = open(f_save)

# store first five biggest mae_k and index
for i in range(7):
    f.readline()    # discard header

# read matrix
mae_k_order = [];
i = 0
iline = f.readline()
while iline != '':
    iline = iline.strip();
    tvec = [ float(t) for t in iline.split() ]
    mae_k_order.append(tvec)
    iline = f.readline()
    i = i + 1

f.close()

rc('font',**{'family':'sans-serif',
    'sans-serif':['Helvetica'],
    'size' : 18,
    })
rc('text', usetex=True)

# single column
fig = plt.figure(figsize=(12, 8.5), dpi=600)
matplotlib.rcParams['xtick.direction'] = 'out'
matplotlib.rcParams['ytick.direction'] = 'out'
plt.imshow(mae_k_order, interpolation='none', origin='lower')
plt.colorbar()

plt.xlabel(r'$k_x$')
plt.ylabel(r'$k_y$')
#plt.xlim(0.5, nk_x+0.5)
#plt.ylim(0.5, nk_y+0.5)
plt.xticks(range(0,20,5),('$-0.5$', '$-0.25$', '$0$', '$0.25$'))
plt.yticks(range(0,20,5),('$-0.5$', '$-0.25$', '$0$', '$0.25$'))
#plt.show()

fig.savefig('mae_k.pdf', bbox_inches='tight')
