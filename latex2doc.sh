#!/bin/sh
echo 'Use: ./latextohtml Informe'
echo $(basename $1 .tex)
############################################################
echo "Convertendo os pdf da pasta figuras para png"
#if [ -d "$DIRECTORY" ]; then
if [ -d "figuras" ]; then
    echo 'Convertendo figuras/*.pdf (s) para png (s)...'
    cd figuras/
    for i in *.pdf; do convert -density 300 $i $(basename $i .pdf).png ;done
    cd .. 
fi
############################################################
echo "Depurando el fichero " $(basename $1 .tex).tex
cp $(basename $1 .tex).tex tempp.tex
sed -e 's/\\begin{Sinput}/ { \\color{red} \\begin{verbatim}/g
        s/\\end{Sinput}/ \\end{verbatim} }/g
        s/\\begin{Soutput}/ { \\color{blue} \\begin{verbatim}/g
        s/\\end{Soutput}/ \\end{verbatim} }/g
        s/\\begin{Schunk}/ /g
        s/\\end{Schunk}/ /g
        s/\\hfill/ /g
        s/tourgunereport/report/g
        s/\\subtitle/\\author/g
        s/DeclareGraphicsExtensions{.pdf/DeclareGraphicsExtensions{.png/g
        s/\\begin{document}/\\usepackage{graphicx}\\DeclareGraphicsExtensions{.png}\\begin{document}/g
        s/\\smallskip//g
        s/\\bigskip//g
        s/\\medskip//g
        s/\\hrule/\n\\hrule\n\n/g
        s/{babel}/{babel}\\makeatletter\\let\\ifes@LaTeXe\\iftrue\\makeatother/g
        s/\\vbox//g
        s/\\begin{spacing}{.*}/\\begin{spacing}{}/g
        s/\\vspace{[^}]*}//g' <tempp.tex >Index.tex 

######################################################################
echo "Borrando basura anterior"
rm -f  Index.idv Index.lg Index.tmp Index.html Index.css Index.4tc Index.xref Index.4ct Index.aux Index.dvi Index.log Index.zip Index.odt Index.doc tempp.tex Index.bbl Index.blg

###################################################
echo "Generando bibliografía, y el html"
pdflatex Index
bibtex Index
for var1 in 1 2 3 # Debemos correr dos o más veces para que el multicolumn funcione. Funciona para cada 3-6-9-...
do
    htlatex Index "html,word,css-in"  "symbol/!" " -cvalidate" # Debemos correr dos o más veces para que el multicolumn
done

###################################################
echo "Ajustando el tamaño de los gráficos en el html"
cp Index.html temp.html
sed -e 's/alt="PIC"/alt="PIC" width=500 height=500 align=center border=0/g
       ' <temp.html >Index.html 

###################################################
echo "Creando el doc"
unoconv -f doc Index.html

###################################################
rm -f  Index.idv Index.lg Index.tmp Index.4tc Index.xref Index.4ct Index.aux Index.dvi Index.log Index.zip temp.html  Index.css Index.bbl Index.blg Index.tex Index.toc

###################################################
echo 'Zipping...'
zip -r Index.zip Index.html Index.doc Dibujos/*.*
