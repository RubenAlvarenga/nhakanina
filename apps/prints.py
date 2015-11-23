#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unipath import Path
import subprocess
import cups


BASE_DIR=Path(__file__).ancestor(2)
saltolinea=chr(13)+chr(10)

def armar_impresion_recibo(recibo):
    filepath = BASE_DIR+'/tmp/recibos/'
    file_name = 'impresion_%s.prt' % (unicode(recibo.nro_recibo))
    f=open(filepath+file_name, "w")
    fecha = unicode(recibo.fecha)
    serie = unicode(recibo.serie)
    nro_recibo = unicode(recibo.nro_recibo)
    persona = unicode(recibo.persona)
    cajero = unicode(recibo.cajero)
    cantidad = unicode(recibo.cantidad)
    monto = unicode(recibo.monto)
    concepto = unicode(recibo.concepto)

    f.write(fecha+saltolinea)
    f.write(serie+saltolinea)
    f.write(nro_recibo+saltolinea)
    f.write(persona+saltolinea)
    f.write(cajero+saltolinea)
    f.write(cantidad+saltolinea)
    f.write(monto+saltolinea)
    f.write(concepto+saltolinea)
    f.close()
    return filepath+file_name

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
