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
            lst.append(linea+CRLF+''.ljust(col_1, 'x'))
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
    #concepto = str(recibo.concepto)


    linea=CRLF*3
    f.write(NEGRITA_OFF+CONDENSADA_ON+linea+''.rjust(120,' ')+str(nro_recibo))

    linea=CRLF*2
    f.write(NEGRITA_ON+CONDENSADA_ON+linea+''.rjust(52,' ')+dia+mes.rjust(18, ' ')+anho.rjust(24, ' '))

    linea=CRLF*2
    f.write(linea+''.rjust(75, ' ')+reemplazar_ascii(persona))




    linea=CRLF*4
    f.write(linea+str(recibo.concepto.concepto.id).ljust(col_1, ' '))

    if len(recibo.get_concepto_planpago) > col_2:
        lista = parsear_en_lineas(recibo.get_concepto_planpago)

        for l in lista:
            f.write(reemplazar_ascii(str(l)).ljust(col_2, '-'))



        linea=CRLF*(13-len(lista))
    else:
        f.write(str(recibo.get_concepto_planpago).ljust(col_2, '-'))
        linea=CRLF*12





    f.write(''.rjust(entre_col, ' ')+cantidad.rjust(col_3, ' '))
    f.write(''.rjust(entre_col, ' ')+str('{:,}'.format(recibo.concepto.monto).replace(",", ".")).rjust(col_4, ' '))
    f.write(''.rjust(entre_col, ' ')+str('{:,}'.format(recibo.monto).replace(",", ".")).rjust(col_5, ' '))


    f.write(linea+''.rjust(col_1+col_2+col_3+col_4+entre_col*3, ' ')+str('{:,}'.format(recibo.monto).replace(",", ".")).rjust(col_5, ' '))


    linea=CRLF*2

    f.write(linea+''.rjust(25, ' ')+num2words(recibo.monto, lang='es').ljust(50, "-"))
     
    f.write(''.rjust(30, ' ')+cajero.last_name+', '+cajero.first_name)
    f.write(CRLF*3)
    f.close()
    return filepath+file_name



# #def probar():
# from apps.finanzas.models import Recibo
# recibo=Recibo.objects.get(pk=231)
# archivo = armar_impresion_recibo(recibo)
# with open(archivo, 'r') as fin:
#     print fin.read()




#Ejecucion del Proceso
# def py_imptck01(camovcom_id,usuario):
#     fb=fecha_a_barra_format
#     nf=number_format
#     movcom=camovcom.objects.get(pk=camovcom_id)
#     mc=movcom.CAMI_CAMOID#camovicab
#     m=movcom # camovicom
#     id_caja=mc.CAMO_NUMCA.CACA_NUMCA
#     CAMC_SEG=mc.CAMO_CASID
#     hoy=hoydia()
#     hora=horadia()
#     #Archivo temporal de Impresion
#     path='/usr/local/django-apps/gico01_01/media/batch_results/imp/'
#     ahora=ahora_mismo_txt()
#     arc='imptck1_%s.prt' % (id_caja,)
#     ai=path+arc
#     f=open(ai,"w")
#     #Impresora a tilizar
#     impre=impre_dat(camovcom_id)
#     #Marcar el Item como Procesando
#     movdet=camovidet.objects.filter(CAMC_NUMID=camovcom_id)
#     movdet_val=movdet.values()
#     CAMC_OBS=''
#     sl=chr(13)+chr(10)
#     #Cabecera
#     x=mc #Datos camovicab
#     x1=str(x.CAMO_NUMCA)
#     x2=str(x.CAMO_DMAMO)
#     cajero=str(x.CAMO_NOMOP)
#     dia=x2[-2:]
#     mes=x2[5:7]
#     anio=x2[0:4]
#     x3=x.CAMO_MATRI
#     soso_matri=x.CAMO_MATRI.SOSO_MATRI
#     #Calcular totales por segmento
#     total=0
#     for d in movdet:
#         total=total+d.CAMC_IMPOR
#     totald=toWord(int(total))
#     ltp=28 #Longitud Total de Pagina
#     #Valores de Impresion de Cabecera
#     CAB=chr(27) + chr(120)+'0'+str(camovcom_id)
#     CAB=CAB+ chr(18)+avl(5)#Linea 5
#     CAB=CAB+ tdr('',53)+'Nro.'+tdl(str(m.CAMI_NUMCO),10)+avl(1)+chr(18)
#     CAB=CAB+ tdr('',12)+dia
#     CAB=CAB+tdr('',1)+ 'de ' +tdr( mesnom(mes),11) + ' de '
#     CAB=CAB+ anio
#     CAB=CAB+tdr('',23)+ 'X'+sl #Linea 6
#     CAB=CAB+ tdr('',7)+idl(soso_matri,10)
#     CAB=CAB+ tdr('',40)+x.CAMO_NRDOI+sl #Linea 7
#     CAB=CAB+tdr('',7)+str(x.CAMO_MATRI.SOSO_NOMBR)+' '+str(x.CAMO_MATRI.SOSO_APELL)+avl(3)#Linea 10
#     CAB=CAB+ chr(15)
#     CAB=CAB+ tdr('',48)+" CUOTA   SALDO"
    
#     CAB=CAB+avl(2)#Linea 12
#     f.write(CAB)
#     conlin=13 #Setea Linea 13
#     for d in movdet:
#         conlin=conlin+1
#         #Datos de Prestamos
#         if d.CAMC_SISTE=='PR':
#             valor=prmapres.objects.get(pk=d.CAMC_CTACO)
#             CAMC_OBS='%s %s' % (str(valor.PRMA_NROPR),str(valor.PRMA_TIPO.PRTP_CODTP))
#         if d.CAMC_SISTE=='PA':
#             valor=pamapres.objects.get(pk=d.CAMC_CTACO)
#             CAMC_OBS='%s %s' % (str(valor.PAMA_NROPR),str(valor.PAMA_TIPO.PATP_CODTP))
#         if d.CAMC_SISTE=='AH':
#             valor=ahahorro.objects.get(pk= d.CAMC_CTACO)
#             ctafor=ahorros_format_tipo_numero(valor.AHAH_TIPO.AHTP_TIPO,valor.AHAH_NROAH)
#             CAMC_OBS='%s' % (ctafor,)
#         if not CAMC_OBS:
#             CAMC_OBS=d.CAMC_OBS
#         if d.CAMC_OBS:
#             DET= CAMC_OBS.rjust(15,'@')
#         else:
#             DET=' '.rjust(15,'@')
#         concepto=str(d.CAMC_CODCO.CACO_NOMCO).ljust(30,'@')
#         DET='%s %s' % (DET,concepto)
#         if d.CAMC_CUOTA:
#             cuota='%s/%s' % (d.CAMC_CUOTA,d.CAMC_CANCU)
#             DET='%s %s' % (DET,cuota.center(7,'@'))
#         else:
#             DET='%s %s' % (DET,' '.center(7,'@'))
#         """
#         if d.CAMC_SALDO>0:
#             DET=DET+idl(str(d.CAMC_SALDO),13)
#         else:
#             DET=DET+tdr('',13)
#         DET=DET+tdr(' ',8)+idl(str(d.CAMC_IMPOR),13)
#         """
#         if d.CAMC_SALDO>0:
#             saldo=nf(d.CAMC_SALDO)
            
#         else:
#             saldo= ' '
#         DET='%s %s' % (DET,saldo.rjust(13,'@'))
#         importe=nf(d.CAMC_IMPOR)
#         DET='%s %s' % (DET,str(importe).rjust(13,'@'))
#         DET=DET+sl
#         DETT=DET
#         DET=DET.replace('@',' ')
#         f.write(DET)
#     #Reporte de Deudas
#     pd=20-conlin
#     DET=avl(pd) #Avanza a Linea 21
#     DET=DET+tdr(' ',3)+ 'Deudas: '
#     DET=DET+tdr(' ',10)+'1232323'
#     DET=DET+sl#Linea 22
#     f.write(DET)
#     #Montos Finales
#     DET=avl(1)#Linea 23
#     DET=DET+tdr(' ',75)+idl(str(total),13)
#     DET=DET+sl #Linea 24
#     DET=DET+tdr(' ',20)+tdr(totald,85)
#     DET=DET+tdr(' ',1)+idl(str(total),13)
#     f.write(DET)
#     #Ipresion de Datos de Caja
#     DET=avl(3)#Linea 27
#     DET=DET+tdr(' ',18)+'Cajero:'+tdr(cajero,30)+' Caja:'+x1+' Hora:'+str(hora)+' Fecha:'+str(hoy)
#     f.write(DET)
#     #Impresion de Pie de Pagina
#     pie=avl(2)
#     f.write(pie)
#     f.close()
#     cimpre='-d'+impre
#     #Imprimir
#     subprocess.call(['lp', cimpre,ai])
#     return
