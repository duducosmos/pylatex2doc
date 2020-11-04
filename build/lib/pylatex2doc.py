#!/usr/bin/env python
# *-* Coding: UTF-8 *-*

__author__ = "Eduardo S. Pereira"
__email__ = "pereira.somoza@gmail.com"
__data__ = "08/10/2013"

"""
This program is an auxiliar tool to convert tex file to doc.
"""

import easygui as eg
import os
import sys
import shutil
import glob


def main(inputFile=None):
    if(inputFile is not None):
        myarq = inputFile
    else:
        myarq = eg.fileopenbox(msg="Enter the latex file to be converted",
               title="Open tex file", default='*', filetypes=["*.tex"])

    msg = """
The file:
         %s
will be used to generate the .doc,.html and .pdf files.
Do you want to continue ?""" % myarq

    if eg.ccbox(msg, 'Start Process'):
        pass
    else:
        sys.exit(0)

    msg = '''If you have some figures in pdf it will be necessary convert these
    images in png files? Have you somo pdf images
'''
    if eg.ccbox(msg, title='Convert pdf figures to png',
                choices=('Yes', 'No')):
        figuresDir = eg.diropenbox(msg='Open the Figure Directory',
                                     title='Figure Directory')
    else:
        pass

    changeDir(myarq)

    depurarFicheiro(myarq)

    cleantemp1()

    bibAndHtml()

    grafiAjust()

    docGen()

    cleantemp2()

    changeFinalName(myarq)

    loc = '/'.join(myarq.split('/')[:-1])

    eg.msgbox("The .doc,.html and .pdf are in the folder:\n %s/ " % loc)


def changeDir(name):
    newname = name.split('/')
    loc = newname[:-1]
    os.chdir('/'.join(loc))


def depurarFicheiro(name):
    newname = name.split('/')
    newname[-1] = 'tempp.tex'
    newname = '/'.join(newname)

    shutil.copyfile(name, newname)

    shcommant = """
sed -e 's/\\\\begin{Sinput}/ { \\\\color{red} \\\\begin{verbatim}/g
        s/\\end{Sinput}/ \\end{verbatim} }/g
        s/\\\\begin{Soutput}/ { \\\\color{blue} \\\\begin{verbatim}/g
        s/\\\\end{Soutput}/ \\\\end{verbatim} }/g
        s/\\\\begin{Schunk}/ /g
        s/\\\\end{Schunk}/ /g
        s/\\\\hfill/ /g
        s/tourgunereport/report/g
        s/\\\\subtitle/\\\\author/g
        s/DeclareGraphicsExtensions{.pdf/DeclareGraphicsExtensions{.png/g
        s/\\\\begin{document}/\\\\usepackage{graphicx}\\\\DeclareGraphicsExtensions{.png}\\\\begin{document}/g
        s/\\\\smallskip//g
        s/\\\\bigskip//g
        s/\\\\medskip//g
        s/\\\\hrule/\\n\\\\hrule\\n\\n/g
        s/{babel}/{babel}\\\\makeatletter\\\\let\\\\ifes@LaTeXe\\\\iftrue\\\\makeatother/g
        s/\\\\vbox//g
        s/\\\\begin{spacing}{.*}/\\\\begin{spacing}{}/g
        s/\\\\vspace{[^}]*}//g' < %s >Index.tex
    """ % newname

    return os.system(shcommant)


def cleantemp1():
    os.system('rm -f Index.idv Index.lg Index.tmp Index.html Index.css')
    os.system('rm -f Index.4tc Index.xref Index.4ct Index.aux Index.dvi')
    os.system('rm -f Index.log Index.zip Index.odt Index.doc tempp.tex ')
    os.system('rm -f Index.bbl Index.blg')


def bibAndHtml():
    pdflatex = os.system('pdflatex Index')
    if(not pdflatex):
        print('pdflatex is Not installed')
        print('ex: sudo apt-get install pdflatex')
    bibtex = os.system('bibtex Index')
    if(not bibtex):
        print('bibtex is Not installed')

    htmlGenCom = 'htlatex'
    htmlGen = " Index \"html,word,css-in\"  \"symbol/!\" \" -cvalidate\""

    for i in range(0, 3):
        htlatex = os.system(htmlGenCom + htmlGen)
        if(htlatex != 0):
            print(htlatex)
            print('htlatex is Not installed')
            print('ex: sudo apt-get install htlatex')


def grafiAjust():
    shutil.copyfile('Index.html', 'temp.html')
    sed = """sed -e 's/alt=\"PIC\"/alt=\"PIC\" width=500 height=500 align=center border=0/g
       ' <temp.html >Index.html"""
    os.system(sed)


def docGen():
    unoconv = os.system('unoconv -f doc Index.html')
    if(unoconv != 0):
        print(unoconv)
        print('unoconv is Not installed')
        print('ex: sudo apt-get install unoconv')


def cleantemp2():
    os.system('rm -f  Index.idv Index.lg Index.tmp Index.4tc')
    os.system('rm -f Index.xref Index.4ct Index.aux Index.dvi')
    os.system('rm -f Index.log Index.zip temp.html  Index.css')
    os.system('rm -f  Index.bbl Index.blg Index.tex Index.toc')


def changeFinalName(name):
    newname = name.split('/')
    newnameEnd = newname[-1].split('.')[0]
    loc = '/'.join(newname[:-1])
    docName = loc + '/' + 'Index.doc'
    newDocName = loc + '/' + newnameEnd + '.doc'
    htmlName = loc + '/' + 'Index.html'
    newHtmlName = loc + '/' + newnameEnd + '.html'
    pdfName = loc + '/' + 'Index.pdf'
    newPdfName = loc + '/' + newnameEnd + '.pdf'

    os.rename(docName, newDocName)
    os.rename(htmlName, newHtmlName)
    os.rename(pdfName, newPdfName)


def convertPdfToPng(figuresDir):
    os.chdir(figuresDir)
    pdfFiles = glob.glob('*.pdf')
    for pdfi in pdfFiles:
        pngFile = pdfi.split('.')[0] + '.png'
        convert = os.system('convert -density 300 %s %s' % (pdfi, pngFile))
        if(convert != 0):
            print('''ImageMagick Convert Command-Line Tool
            is Not installed.
            ex: sudo apt-get install imagemagick
            ''')
            sys.exit()


if(__name__ == '__main__'):
    main()
