#!/usr/bin/env python
import sys

#f_par = 'par.k.pdos_tot'
#f_per = 'per.k.pdos_tot'
f_par = sys.argv[1]
f_per = sys.argv[2]

f = open(f_par)

nk_x = 20
nk_y = 20
nk_z = 1
nkpt = nk_x*nk_y*nk_z

sumpar_k = [ 0 for i in range(nkpt) ]
wk_k = [ 1.00/nkpt for i in range(nkpt) ]

tline = f.readline()    # discard header
tline = f.readline()
ik = 0
ndos = 0
ndos_tot = -1

while tline != '':
    tvec = tline.strip().split()
    if ( len(tvec) > 0 ):
        e = float(tvec[1])
        if (ndos == 0):
            E_dw = e
        elif (ndos == (ndos_tot-1)):
            E_up = e
        
        dos = float(tvec[2])
        sumpar_k[ik] = sumpar_k[ik] + e*dos*wk_k[ik]
        ndos = ndos + 1
    else:
        print('ik = ' + str(ik+1) + ', ndos_tot = ' + str(ndos))
        ndos_tot = ndos
        ndos = 0
        ik = ik + 1
    
    tline = f.readline()


f.close()

###

f = open(f_per);

sumper_k = [ 0 for i in range(nkpt) ]

tline = f.readline()    # discard header
tline = f.readline()
ik = 0
ndos = 0
ndos_tot = -1

while tline != '':
    tvec = tline.strip().split()
    if ( len(tvec) > 0 ):
        e = float(tvec[1])
        if (ndos == 0):
            E_dw = e
        elif (ndos == (ndos_tot-1)):
            E_up = e
        
        dos = float(tvec[2])
        sumper_k[ik] = sumper_k[ik] + e*dos*wk_k[ik]
        ndos = ndos + 1;
    else:
        print('ik = ' + str(ik+1) + ', ndos_tot = ' + str(ndos))
        ndos_tot = ndos
        ndos = 0
        ik = ik + 1
    
    tline = f.readline()


f.close()

###

# convert unit to meV
fact = (E_up - E_dw) / ndos_tot * 1000;
mae_k = [(sumpar_k[i] - sumper_k[i])*fact for i in range(nkpt)]
mae = sum(mae_k)


# BOHR_RADIUS_ANGS= 0.52917720858999995;

# final unit probably is eV
# mae = mae * (1/BOHR_RADIUS_ANGS)^3

f_kpts = 'kpts'
f = open(f_kpts)

ik = 0
# for mae_k_order, origin is at left down corner, x horizontal, y vertical
# discard row 0 & column 0 for displaying figure
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
inds = sorted(range(len(mae_k)), key=lambda x: mae_k[x], reverse=True)
for i in range(5):
    f.write('kpt: ' + str(inds[i]+1) + 
        ', [ix,iy] = ' + str(indxy[inds[i]]) + 
        ', mae_k = ' + str(mae_k[inds[i]]) + '\n')


# store matrix
for i in range(nk_x):
    for j in range(nk_y):
        f.write(str(mae_k_order[i][j]) + ' ')
    f.write('\n')

f.close()

