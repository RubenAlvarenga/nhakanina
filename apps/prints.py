#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unipath import Path
import subprocess
import cups




#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unipath import Path
import subprocess
import cups
BASE_DIR=Path(__file__).ancestor(2)


# import sys, os
# sys.path.append("/home/ruben/apps/iseapp/iseapp")
# os.environ["DJANGO_SETTINGS_MODULE"] = "iseapp.settings.local"
# from apps.finanzas.models  import Recibo
# BASE_DIR='/home/ruben/apps/iseapp/iseapp'



def reemplazar_ascii(cadena):
    d = {'\xc3\xa1' : chr(160), # á
        '\xc3\xa9' : chr(130), # é
        '\xc3\xad' : chr(161), # í
        '\xc3\xb3' : chr(162), # ó
        '\xc3\xba' : chr(163), # ú
        '\xc3\x81' : chr(65), # Á
        '\xc3\x89' : chr(69), # É
        '\xc3\x8d' : chr(73), # Í
        '\xc3\x93' : chr(79), # Ó
        '\xc3\x9a' : chr(85), # Ú
        '\xc3\xb1' : chr(164), # ñ
        '\xc3\x91' : chr(165), # Ñ
    }
    for c in d.keys():
        cadena = cadena.replace(c,d[c])
    return cadena


entre_col = 5
col_1=16
col_2=50
col_3=7
col_4=16
col_5=21


ESC  = chr(27)
CRLF = chr(13) + chr(10)
FF   = chr(12)
NEGRITA_ON  = ESC + 'E'
NEGRITA_OFF = ESC + 'F'
CONDENSADA_ON  = chr(15)
CONDENSADA_OFF = chr(22)
GRANDE_ON  = ESC + 'w' + chr(1) + ESC + 'W' + chr(1)
GRANDE_OFF = ESC + 'w' + chr(0) + ESC + 'W' + chr(0)



def parsear_en_lineas(cadena):
    lst=[]
    linea=''
    palabras = cadena.split(" ")
    for palabra in palabras:
        if len(linea) > col_2:
            lst.append(linea+CRLF+''.ljust(col_1, ' '))
            linea=palabra+' '
        else:
            linea = linea+palabra+' '
    lst.append(linea)
    return lst

from num2words import num2words
from apps.functions import mes_en_letras
def armar_impresion_recibo(recibo):
    filepath = BASE_DIR+'/tmp/recibos/'
    file_name = 'impresion_%s.prt' % (str(recibo.nro_recibo))
    f=open(filepath+file_name, "w")
    
    dia=str(recibo.fecha.day)
    mes=str(mes_en_letras(recibo.fecha.month))
    anho=str(recibo.fecha.year)[-2:]

    serie = str(recibo.serie)
    nro_recibo = str(recibo.nro_recibo)
    persona = str(recibo.persona)
    cajero = recibo.cajero
    cantidad = str(recibo.cantidad)
    monto = str(recibo.monto)
    if recibo.concepto.concepto.fraccionable  or recibo.descuentos.all(): unitario = "-" 
    else: unitario =  str('{:,}'.format(recibo.concepto.monto).replace(",", "."))
    #concepto = str(recibo.concepto)


    linea=CRLF*4
    f.write(NEGRITA_OFF+CONDENSADA_ON+linea+''.rjust(120,' ')+str(nro_recibo))

    linea=CRLF*2
    f.write(NEGRITA_ON+CONDENSADA_ON+linea+''.rjust(52,' ')+dia+mes.rjust(18, ' ')+anho.rjust(24, ' '))

    linea=CRLF*2
    f.write(linea+''.rjust(75, ' ')+reemplazar_ascii(persona))




    linea=CRLF*4
    f.write(linea+str(recibo.concepto.concepto.id).ljust(col_1, ' '))

    if len(recibo.get_concepto_recibo) > col_2:
        lista = parsear_en_lineas(recibo.get_concepto_recibo)

        for l in lista:
            f.write(reemplazar_ascii(str(l)).ljust(col_2, '-'))

        linea=CRLF*(13-len(lista))
    else:
        f.write(str(recibo.get_concepto_recibo).ljust(col_2, '-'))
        linea=CRLF*12





    f.write(''.rjust(entre_col, ' ')+cantidad.rjust(col_3, ' '))
    f.write(''.rjust(entre_col, ' ')+unitario.rjust(col_4, ' '))
    f.write(''.rjust(entre_col, ' ')+str('{:,}'.format(recibo.monto).replace(",", ".")).rjust(col_5, ' '))


    f.write(linea+''.rjust(col_1+col_2+col_3+col_4+entre_col*3, ' ')+str('{:,}'.format(recibo.monto).replace(",", ".")).rjust(col_5, ' '))


    linea=CRLF*2

    f.write(linea+''.rjust(25, ' ')+num2words(recibo.monto, lang='es').ljust(50, "-"))
     
    f.write(''.rjust(30, ' ')+cajero.last_name+', '+cajero.first_name)
    f.write(CRLF*7)
    f.close()
    return filepath+file_name

