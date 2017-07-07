#!/vol6/home/weisheng/qiao/bin/anaconda3/bin/python3
import os
import re
from lxml import etree
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def getXmlInfo(ifile):
    AUTOEV = 27.211383860484776  # from pwuc.x ls
    tree = etree.parse(ifile)
    #print('    nbnd = ', tree.xpath('/Root/INFO/@nbnd')[0])
    mat_eig = [ float(i)*AUTOEV for i in tree.xpath('/Root/EIGENVALUES/text()')[0].split() ]
    mat_occ = [ float(i) for i in tree.xpath('/Root/OCCUPATIONS/text()')[0].split() ]
    return (mat_eig, mat_occ)

def getEmpBndNum(mat_occ):
    OCCTOL = 1e-80    # tolerance for occupation number
    test = np.abs(np.array(mat_occ)) < OCCTOL
    for i in range(len(mat_occ)-1, -1, -1):
        if test[i]:
            pass
        else:
            break
    return len(mat_occ)-i-1

def findDestDir(hdir):
    print(hdir)
    destpath = input("dir for *.save (./tempdir/*.save): ")
    #destpath = ''
    print()

    if destpath == '':
        try:
            tmp = os.listdir('./tempdir')
            destpath = ''
            for idir in tmp:
                if re.search('.+\.save$', idir):
                    destpath = os.path.join(hdir, 'tempdir', idir)
                    break
                else:
                    pass
            if destpath == '':
                raise FileNotFoundError
            else:
                pass
        except FileNotFoundError as e:
            e.args = ("Can't find *.save dir, plz input manually")
            raise e
    else:
        if os.path.isdir(os.path.join('.', destpath)):
            destpath = os.path.join(os.path.join('.', destpath))
        else:
            raise FileNotFoundError('Input dir not exist!')
    return destpath

def getKlistNbnd(destpath):
    kdir = [idir for idir in os.listdir(destpath) if os.path.isdir(os.path.join(destpath, idir))]
    kdir.sort(key=lambda x: int(x[1:]))
    eigxml = [tmp for tmp in os.listdir(kdir[0]) if re.search('eigenval.?\.xml', tmp)][0]
    tree = etree.parse(os.path.join(destpath, kdir[0], eigxml))
    nbnd = tree.xpath('/Root/INFO/@nbnd')[0]
    return kdir, nbnd


def traverseDestDir(homepath, destpath):
    global mat_all_eig, mat_all_occ
    ftxt = open(os.path.join(homepath, 'occ-' + os.path.split(homepath)[-1] + '.txt'), 'w')

    (kdir, nbnd) = getKlistNbnd(destpath)
    # -10 to debug abnormal situation
    mat_size = (len(kdir), int(nbnd))
    mat_all_eig[0] = np.full(mat_size, -10, dtype=np.float64)
    mat_all_occ[0] = np.full(mat_size, -10, dtype=np.float64)
    mat_all_eig[1] = np.full(mat_size, -10, dtype=np.float64)
    mat_all_occ[1] = np.full(mat_size, -10, dtype=np.float64)
    not_emp_count = [0, 0]
    min_emp_bnd = [-1, -1]

    for i, idir in enumerate(kdir):
        #print(idir)
        eigxml = [tmp for tmp in os.listdir(idir) if re.search('eigenval.?\.xml', tmp)]
        for j, jxml in enumerate(eigxml):
            (mat_eig, mat_occ) = getXmlInfo(os.path.join(destpath, idir, jxml))
            mat_all_eig[j][i] = np.array(mat_eig)
            mat_all_occ[j][i] = np.array(mat_occ)

            emp_bnd_num = getEmpBndNum(mat_occ)
            outstr = ('in ' + str(idir) + ' ' + str(jxml) + '\n' 
                     '       number of empty bands = ' + str(emp_bnd_num) + '\n')
            print(outstr, end='')
            ftxt.write(outstr)
            if (emp_bnd_num < min_emp_bnd[j]) or (min_emp_bnd[j]<0):
                min_emp_bnd[j] = emp_bnd_num
            else:
                pass

            tst_full = 1 if emp_bnd_num == 0 else 0
            if tst_full:
                outstr = ('in ' + str(idir) + ' ' + str(jxml) + '\n'
                         '****** highest band not empty ******, occ = ' + str(mat_occ[-1]) + '\n')
                print(outstr, end='')
                ftxt.write(outstr)
            else:
                pass
            not_emp_count[j] += tst_full
        outstr = '\n'
        print(outstr, end='')
        ftxt.write(outstr)
    outstr = '\n'
    print(outstr, end='')
    ftxt.write(outstr)
    if sum(not_emp_count) > 0:
        outstr = str(sum(not_emp_count)) + ' kpoints do not have empty bands'
        print(outstr, end='')
        ftxt.write(outstr)
    else:
        outstr = 'all kpoints have empty bands'
        print(outstr, end='')
        ftxt.write(outstr)
    ftxt.close()
    return not_emp_count, min_emp_bnd

def plotMat(figname, mat, not_emp_count, min_emp_bnd):
    if np.all(mat[1][0] == -10):
        # only eigenval1.xml exists
        plt.figure(figsize=(40, 10), dpi=300)
        plt.imshow(np.transpose(mat[0]), origin='lower', interpolation='none', cmap='cool', aspect='auto')
        plt.colorbar()
        plt.grid()
        plt.title('eigenval.xml')
        plt.xlabel('#kpoint', fontsize=14)
        plt.ylabel('#band', fontsize=14)
        plt.text(0, 0, 'min(#empty bands) = ' + str(min_emp_bnd[0]))
        plt.text(0, 2, '#kpoints no empty bands = '+str(not_emp_count[0]))
    else:
        plt.figure(figsize=(40, 10), dpi=300)
        plt.subplot(1, 2, 1)
        plt.imshow(np.transpose(mat[0]), origin='lower', interpolation='none', cmap='cool', aspect='auto')
        plt.colorbar()
        plt.grid()
        plt.title('eigenval1.xml')
        plt.xlabel('#kpoint', fontsize=14)
        plt.ylabel('#band', fontsize=14)
        plt.text(0, 0, 'min(#empty bands) = '+str(min_emp_bnd[0]))
        plt.text(0, 2, '#kpoints no empty bands = '+str(not_emp_count[0]))

        plt.subplot(1, 2, 2)
        #print(mat[1])
        plt.imshow(np.transpose(mat[1]), origin='lower', interpolation='none', cmap='cool', aspect='auto')
        plt.colorbar()
        plt.grid()
        plt.title('eigenval2.xml')
        plt.xlabel('#kpoint', fontsize=14)
        plt.ylabel('#band', fontsize=14)
        plt.text(0, 0, 'min(#empty bands) = '+str(min_emp_bnd[1]))
        plt.text(0, 2, '#kpoints no empty bands = '+str(not_emp_count[1]))

    plt.savefig(figname, dpi=300)

def main():
    homepath = os.getcwd()
    destpath = findDestDir(homepath)
    os.chdir(destpath)
    not_emp_count, min_emp_bnd = traverseDestDir(homepath, destpath)
    print()
    print('Ploting occupations ...')
    os.chdir(homepath)
    figname = 'occ-' + os.path.split(homepath)[-1] + '.jpg'
    plotMat(figname, mat_all_occ, not_emp_count, min_emp_bnd)
    print('Plot finished.')

if __name__ == '__main__':
    mat_all_eig = [0, 0]    # for eigenval1.xml & eigenval2.xml
    mat_all_occ = [0, 0]
    main()
else:
    pass
