#!/usr/bin/env python3
import sys
import os
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
from scipy.interpolate import spline
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D

class Params():
    # params:
    # states[natomwfc]
    # efermi
    # filproj
    # nks
    # plot_kpts[nks]
    # emin
    # emax
    # emin_hasdiff

    def __init__(self, kpdosout, fermi, plotin, plotout):
        kdosOut = self.KdosOut()
        kdosOut.getStates(kpdosout)
        self.states = kdosOut.states

        self.efermi = self.getFermi(fermi)

        plotIn = self.PlotIn()
        plotIn.getInput(plotin)
        self.filproj = plotIn.filproj
        self.nks = plotIn.nks
        self.plot_kpts = plotIn.plot_kpts
        self.emin = plotIn.emin
        self.emax = plotIn.emax

        plotOut = self.PlotOut()
        plotOut.getOutput(plotout)
        self.emin_hasdiff = plotOut.emin_hasdiff


    class KdosOut():

        def __init__(self):
            self.states = []

        def getStates(self, f_kpdos_out):
            """find states"""
            #f_kpdos_out = 'par_kpdos.out'
            f = open(f_kpdos_out)

            i = 0
            tline = f.readline()
            found = False
            while tline != '':
                if tline.strip().find('state #') == -1:
                    if (not found):
                        tline = f.readline()
                        continue
                    else:
                        break

                print(tline)
                self.states.append(tline.split(':')[1].strip())
                i = i + 1
                tline = f.readline()
                found = True

            f.close()


    def getFermi(self, f_fermi):
        """get fermi level"""
        #f_fermi = 'par_fermi'
        f = open(f_fermi)
        efermi = float(f.readline().strip())
        return efermi


    class PlotIn():

        def __init__(self):
            self.filproj = ''
            self.nks = 0
            self.plot_kpts = []
            self.emin = 0
            self.emax = 0

        def getInput(self, f_in):
            """read plotproj_k.in"""
            #f_in = 'plotproj_k.in'
            f = open(f_in)
            # discard header
            for i in range(5):
                tline = f.readline()

            self.filproj = tline.strip()

            # discard
            for i in range(3):
                tline = f.readline()

            self.nks = int(tline.strip())

            for i in range(self.nks):
                tline = f.readline().strip()
                print('ik = ' + tline)
                self.plot_kpts.append(int(tline))

            tline = f.readline().strip()
            self.emin = float(tline.split(',')[0].strip())
            self.emax = float(tline.split(',')[1].strip())

            f.close()


    class PlotOut():

        def __init__(self):
            self.emin_hasdiff = 0

        def getOutput(self, f_out):
            """read plotproj_k.out, get emin_hasdiff"""
            #f_out = 'plotproj_k.out'
            f = open(f_out)
            tline = f.readline()
            while (tline != ''):
                tmpstr = tline
                tline = f.readline()

            self.emin_hasdiff = float(tmpstr.strip().split('=')[1].strip())
            f.close()


class Plotter():

    def __init__(self, ikpt, params):
        self.params = params
        self.ikpt = ikpt
        self.parfiles = []
        self.perfiles = []
        self.k = []
        self.savedir = './pdf'

        if not os.path.exists(self.savedir):
            os.mkdir(self.savedir)

    def findFiles(self):
        filterer = lambda tstr: True if tstr.find(self.params.filproj) >= 0 else False
        tfiles = list(filter(filterer, os.listdir('.')))

        filterer = lambda tstr: True if tstr.find('.pdf') < 0 else False
        files = list(filter(filterer, tfiles))

        filterer = lambda tstr: True if tstr.find('_ikpt'+str(self.ikpt)) >= 0 else False
        files = list(filter(filterer, tfiles))

        filterer = lambda tstr: True if tstr.find('par') >= 0 else False
        self.parfiles = list(filter(filterer, files))

        filterer = lambda tstr: True if tstr.find('per') >= 0 else False
        self.perfiles = list(filter(filterer, files))

    def readFile(self, filename):
        f = open(filename)
        # first few lines are blank, discard
        print(filename)
        iline = f.readline()
        while iline == '\n':
            iline = f.readline()
        self.k = []
        # True then no need to update k
        kOk = False
        # for final result
        e = []
        proj = []
        # tmp for each line
        eline = []
        projline = []
        while iline != '':
            if iline == '\n':
                e.append(eline)
                proj.append(projline)
                eline = []
                projline = []
                kOk = True
                # discard empty lines
                while iline == '\n':
                    iline = f.readline()
            else:
                strs = iline.strip().split()
                if not kOk:
                    self.k.append(int(strs[0]))
                # subtract fermi energy
                eline.append(float(strs[1]) - self.params.efermi)
                projline.append(float(strs[2]))
                iline = f.readline()

        return e, proj


    def plotBandPartial(self, filename, e, proj):

        rc('font',**{'family':'sans-serif',
            'sans-serif':['Helvetica'],
            'size' : 18,
            })
        rc('text', usetex=True)

        # single column
        fig = plt.figure(figsize=(8.5, 12), dpi=600)
        #matplotlib.rcParams['xtick.direction'] = 'out'
        #matplotlib.rcParams['ytick.direction'] = 'out'
        # plot blue lines
        for i in range(len(e)):
            k_np = np.array(self.k)
            e_np = np.array(e[i])
            rgba_colors = np.zeros((len(k_np), 4))
            rgba_colors[:, 2] = np.ones(len(k_np))
            rgba_colors[:, 3] = np.array(proj[i])
            plt.scatter(k_np, e_np, color=rgba_colors)

        plt.plot([self.k[0], self.k[-1]], [0, 0], 'k--')

        #plt.colorbar()

        plt.xlabel(r'$kpoint$ $number$')
        plt.ylabel(r'$E-E_{\rm Fermi} [eV]$')
        plt.xlim(self.k[0], self.k[-1])
        plt.ylim(ymin = self.params.emin_hasdiff)
        symbols = []
        for ik in self.k:
            if ik == self.ikpt:
                symbols.append(r'$\mathbf{'+str(ik)+r'}$')
            else:
                symbols.append(r'$'+str(ik)+r'$')

        plt.xticks(range(1,6), symbols)
        print('  Processing ... ' + filename)
        n_stat = int(filename[filename.find('nwfc')+4:])
        plt.title(r'\begin{verbatim}'+'nwfc'+str(n_stat)+'_'
                  +self.params.states[n_stat-1]+r'\end{verbatim}')
        #plt.axis(xmin=, xmax=X[-1], ymin=emin, ymax=emax)
        #plt.show()

        fig.savefig(os.path.join(self.savedir,'band_'+filename+'.pdf')
                    , bbox_inches='tight')
        plt.close(fig)

    def plotBandTotal(self, e_par, e_per):

        rc('font',**{'family':'sans-serif',
            'sans-serif':['Helvetica'],
            'size' : 18,
            })
        rc('text', usetex=True)

        # single column
        fig = plt.figure(figsize=(8.5, 12), dpi=600)
        #matplotlib.rcParams['xtick.direction'] = 'out'
        #matplotlib.rcParams['ytick.direction'] = 'out'

        len_par = len(e_par)
        len_per = len(e_per)

        if (len_par != len_per):
            print('Warning: len(e_par) = ', len_par, 'len(e_per) = ', len_per)

        len_e = max(len_par, len_per)
        for i in range(len_e):
            knew = np.linspace(self.k[0], self.k[-1], 50)
            if (i < len_par):
                enew = spline(self.k, e_par[i], knew)
                plt.plot(knew, enew, 'r-', label='par', alpha=0.5)
            if (i < len_per):
                enew = spline(self.k, e_per[i], knew)
                plt.plot(knew, enew, 'b-', label='per', alpha=0.5)

        plt.plot([self.k[0], self.k[-1]], [0, 0], 'k--')

        #plt.colorbar()

        plt.xlabel(r'$kpoint$ $number$')
        plt.ylabel(r'$E-E_{Fermi} [eV]$')
        plt.xlim(self.k[0], self.k[-1])
        #plt.ylim(0.5, nk_y+0.5)
        symbols = []
        for ik in self.k:
            if ik == self.ikpt:
                symbols.append(r'$\mathbf{'+str(ik)+r'}$')
            else:
                symbols.append(r'$'+str(ik)+r'$')

        plt.xticks(range(1,6), symbols)
        plt.title("Par(red)/Per(blue) band structure")
        #plt.legend()
        #plt.axis(xmin=, xmax=X[-1], ymin=emin, ymax=emax)
        #plt.show()

        #plt.show()
        fig.savefig(os.path.join(self.savedir,'band_tot.pdf'),
                    bbox_inches='tight')
        plt.close(fig)

    def plotBandProj(self, files):

        rc('font', **{'family': 'sans-serif',
                      'sans-serif': ['Helvetica'],
                      'size': 18,
                      })
        rc('text', usetex=True)

        fig, axes = plt.subplots(figsize=(8.5, 12), dpi=600)

        # distinct color for each line
        #https://stackoverflow.com/questions/14720331/how-to-generate-random-colors-in-matplotlib
        numwfcs = len(files)
        linecolors = plt.cm.get_cmap(lut=numwfcs)

        # plot each wfc
        for ifile in range(numwfcs):
            e, proj = self.readFile(files[ifile])

            # plot each band
            nbnd = len(e)
            for ibnd in range(nbnd):

                # interpolate by spline
                #https://stackoverflow.com/questions/5283649/plot-smooth-line-with-pyplot
                knew = np.linspace(self.k[0], self.k[-1], 50)
                print(files[ifile])
                #print(self.k, e[ibnd], proj[ibnd])
                enew = spline(self.k, e[ibnd], knew)
                projnew = spline(self.k, proj[ibnd], knew)
                #projnew = np.ones(enew.shape)/3
                for t in projnew:
                    if t < 0 and abs(t) > 0.01:
                        print('  warning: interpolated projnew ', t,
                              " < 0, use abs(projnew) instead")
                projnew = abs(projnew)

                # plot line
                self.colorline(knew, enew, projnew, linecolors(ifile), ax=axes)

        plt.plot([self.k[0], self.k[-1]], [0, 0], 'k--')

        plt.xlabel(r'$kpoint$ $number$')
        plt.ylabel(r'$E-E_{Fermi} [eV]$')
        plt.xlim(self.k[0], self.k[-1])
        plt.ylim(ymin = self.params.emin_hasdiff)
        symbols = []
        for ik in self.k:
            if ik == self.ikpt:
                symbols.append(r'$\mathbf{' + str(ik) + r'}$')
            else:
                symbols.append(r'$' + str(ik) + r'$')

        plt.xticks(range(1, 6), symbols)

        def make_proxy(rgba, **kwargs):
            return Line2D([0, 1], [0, 1], color=rgba, **kwargs)

        #https://stackoverflow.com/questions/19877666/add-legends-to-linecollection-plot
        #https://matplotlib.org/users/legend_guide.html#creating-artists-
        # specifically-for-adding-to-the-legend-aka-proxy-artists
        proxies = [make_proxy(linecolors(i), linewidth=5)
                   for i in range(numwfcs)]
        names = [r'\begin{verbatim}'+self.params.states[i]+'\end{verbatim}'
                 for i in range(numwfcs)]
        axes.legend(proxies, names,
                    loc='center left', bbox_to_anchor=(1, 0.5))

        filename = files[0]
        filename = filename[:filename.find('_ibnd')]

        plt.title(r'\begin{verbatim}'+filename+'\end{verbatim}')

        fig.savefig(os.path.join(self.savedir,filename+'.pdf')
                    , bbox_inches='tight')
        plt.close(fig)

    #http://nbviewer.jupyter.org/github/dpsanders/matplotlib-examples/blob/master/colorline.ipynb
    # Data manipulation:
    def make_segments(self, x, y, alphas):
        '''
        Create list of line segments from x and y coordinates, in the correct format for LineCollection:
        an array of the form   numlines x (points per line) x 2 (x and y) array
        '''

        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        # average between points
        alphasegs = np.array([sum(alphas[i:i+2])/2 for i in range(len(alphas)-1)]).T

        return segments, alphasegs

    # Interface to LineCollection:
    def colorline(self, x, y, proj, cmap, ax=None, norm=plt.Normalize(0.0, 1.0), linewidth=1):
        '''
        Plot a colored line with coordinates x and y
        specify colors in cmap, and alpha in the array proj
        Optionally specify a norm function and a line width
        '''

        segments, alphas = self.make_segments(x, y, proj)
        # must be np.float, otherwise assignment of float to int will be lost!
        #linergba = np.concatenate((np.array(cmap, dtype=np.float), [0.0]), axis=0)
        #linergba = np.array(cmap, dtype=np.float)
        #colors = np.repeat([linergba], len(segments), axis=0)
        #colors[:,-1] = alphas
        rgb = list(cmap)[:-1]
        #print(cmap, rgb)
        colors = [ rgb+[i] for i in alphas]
        #print(colors)
        lc = LineCollection(segments, norm=norm, linewidth=linewidth, colors=colors)

        if ax is None:
            ax = plt.gca()
        ax.add_collection(lc)

        return lc

    def clear_frame(self, ax=None):
        # Taken from a post by Tony S Yu
        if ax is None:
            ax = plt.gca()
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        for spine in ax.spines.itervalues():
            spine.set_visible(False)


def main():
    """start drawing"""
    os.chdir('/home/joe/git/qe_test/3CoFe_Vacuum/kpt_20/4-nbnd_40/2-mae/calc_integral_ildos/plotproj_k')
    print(os.getcwd())

    kpdos = '../../1-par/kpdos/par_kpdos.out'
    #kpdos = '../../1-par/kpdos/out'
    fermi = '../../1-par/per_fermi'
    plotin = './plotproj_k.in'
    plotout = './plotproj_k.out'

    params = Params(kpdos, fermi, plotin, plotout)

    # loop on kpts
    for i in range(params.nks):
        plotter = Plotter(params.plot_kpts[i], params)
        plotter.findFiles()

        # plot total band structure
        e_par, dum = plotter.readFile(plotter.parfiles[0])
        e_per, dum = plotter.readFile(plotter.perfiles[0])
        plotter.plotBandTotal(e_par, e_per)

        # # plot partial band
        # for ifile in plotter.parfiles:
        #     e, proj = plotter.readFile(ifile)
        #     plotter.plotBandPartial(ifile, e, proj)
        #
        # # plot partial band
        # for ifile in plotter.perfiles:
        #     e, proj = plotter.readFile(ifile)
        #     plotter.plotBandPartial(ifile, e, proj)

        # plot projected band
        plotter.plotBandProj(plotter.parfiles)
        plotter.plotBandProj(plotter.perfiles)

if __name__ == '__main__':
    main()

