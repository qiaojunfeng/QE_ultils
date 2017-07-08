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
