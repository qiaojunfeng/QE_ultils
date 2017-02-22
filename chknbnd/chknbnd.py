#!/vol6/home/weisheng/qiao/bin/anaconda3/bin/python3
import os
import re
from lxml import etree


def getXmlInfo(ifile):
    AUTOEV = 27.211383860484776  # from pwuc.x ls
    OCCTOL = 1e-80    # tolerance for occupation number
    tree = etree.parse(ifile)
    print('    nbnd = ', tree.xpath('/Root/INFO/@nbnd')[0])
    eig = tree.xpath('/Root/EIGENVALUES/text()')[0].split()
    occ = tree.xpath('/Root/OCCUPATIONS/text()')[0].split()
    print('    highest band(eig/eV, occ): ', float(eig[-1])*AUTOEV, occ[-1])
    if abs(float(occ[-1])) < OCCTOL:
        return 0
    else:
        print('****** highest band not empty ******, occ = ', occ)
        return 1

def main():
    homepath = os.getcwd()
    print(homepath)
    destpath = input("dir for *.save (./tempdir/*.save): ")
    notEmptyCount = 0

    if destpath == '':
        try:
            tmp = os.listdir('./tempdir')
            destpath = ''
            for idir in tmp:
                if re.search('.+\.save$', idir):
                    destpath = os.path.join(homepath, 'tempdir', idir)
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
        pass
    os.chdir(destpath)

    kdir = [ idir for idir in os.listdir(destpath) if os.path.isdir(os.path.join(destpath, idir)) ]
    for idir in kdir:
        print(idir)
        eigxml = [ tmp for tmp in os.listdir(idir) if re.search('eigenval.?\.xml', tmp) ]
        for ixml in eigxml:
            print(ixml)
            notEmptyCount += getXmlInfo(os.path.join(destpath, idir, ixml))
    print()
    print()
    if notEmptyCount > 0:
        print(str(notEmptyCount), 'kpoints do not have empty bands')
    else:
        print('all kpoints have empty bands')

if __name__ == 'main':
    main()
else:
    pass
