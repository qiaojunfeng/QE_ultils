# sum_ildos.py
Get real space resolved MAE:

$MAE(r) = \int_{E_{dw}} ^{E_{up}} E * LDOS(r,E) dE$

where $LDOS(r,E) = \sum_{ibnd} ^{occ} \sum_{ik} w_{ik} * |\psi(r, ik, E)|^2$

Only compatible with my modified QE `pp.x` with `plot_num = 10`.

Usage: `./getemin.py dosfile`

where dosfile is the output file of dos.x
