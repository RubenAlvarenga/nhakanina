# -*- coding: utf-8 -*-
# taken from http://weitlandt.com/theme/2010/05/wir-djangonauten-csv-export-nach-excel-mit-umlauten/
# + mucho amor de @julian_amaya y @votaguz

import csv
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.template import Context, Template, RequestContext
from wkhtmltopdf.views import PDFTemplateResponse
from django.shortcuts import render_to_response, get_object_or_404, HttpResponseRedirect, urlresolvers
from datetime import datetime
from django.contrib import messages
from django.db import IntegrityError
from num2words import num2words


def xls_to_response(xls, fname):
    response = HttpResponse(content_type="application/vnd.ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s' % fname
    xls.save(response)
    return response


def get_csv_from_dict_list(field_list, data):
    csv_line = ";".join(['{{ row.%s|addslashes }}' % field for field in field_list])
    template = "{% for row in data %}" + csv_line + "\n{% endfor %}"
    return Template(template).render(Context({"data": data}))


def export_as_pdf(request, table, *args, **kwargs):
    pdf_name = 'localizaciones/pdfListarPaises.html'
    return render(request, pdf_name, {'table':table})

def eliminar_bulk(request, queryset, *args, **kwargs):
    eliminados=[]
    #errores=[]
    modelo=queryset.model._meta.verbose_name_plural.capitalize()
    for obj in queryset:
        try:
            obj.delete()
            eliminados.append(unicode(obj))
        except IntegrityError as e:
            #dic={'messages': (e,)}
            #return render_to_response(self.template_name, dic, context_instance=RequestContext(request))
            #import pdb; pdb.set_trace()
            #errores.append(+" "+str(e))
            messages.add_message(request, messages.ERROR,  str(obj)+" "+str(e), extra_tags='danger' )


    success_message = "los "+unicode(modelo)+": "+unicode(eliminados)+" han sido eliminados con exito"
    if eliminados: messages.add_message(request, messages.SUCCESS, success_message )
    #if errores: messages.add_message(request, messages.ERROR, "dewfefesfsf fdsf" + str(errores) )
    url = request.META['HTTP_REFERER']
    return HttpResponseRedirect(url)


def export_as_csv(modelo, request, queryset):
    #if not request.user.is_staff:
        #raise PermissionDenied
    replace_dc = {'\n': '* ', '\r': '', ';': ',', '\"': '|', '\'': '|', 'True': 'Si', 'False': 'No'}
    #opts = modelo.model._meta
    opts = modelo._meta
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    #response = HttpResponse(mimetype='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')
    w = csv.writer(response, delimiter=';')
    # import pdb; pdb.set_trace()
    try:
        field_names = modelo.get_csv_fields()
        v_field_names = field_names
    except:
        field_names = [field.name for field in opts.fields]
        v_field_names = [getattr(field, 'verbose_name') or field.name for field in opts.fields]
    v_field_names = map(lambda x: x.encode('utf-8') if x != 'ID' else 'Id', v_field_names)
    w.writerow(v_field_names)
    ax = []

    for obj in queryset:
        acc = {}
        for field in field_names:
            try:
                uf = unicode(getattr(obj, field)()).encode('utf-8')
            except:
                try:
                    uf = unicode(getattr(obj, field)).encode('utf-8')
                except:
                    uf = ''
            for i, j in replace_dc.iteritems():
                uf = uf.replace(i, j)
            if uf == 'None':
                uf = ''
            acc[field] = uf
        ax.append(acc)
    response.write(get_csv_from_dict_list(field_names, ax))
    return response

#export_as_csv.short_description = "Exportar como CSV"



def export_table_to_csv(modelo, request, table):
    #if not request.user.is_staff:
        #raise PermissionDenied
    replace_dc = {'\n': '* ', '\r': '', ';': ',', '\"': '|', '\'': '|', 'True': 'Si', 'False': 'No'}
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    #response = HttpResponse(mimetype='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(table.data.verbose_name_plural.title()+"_"+str(datetime.now().date())).replace('.', '_')
    w = csv.writer(response, delimiter=';')
    
    #try:
    #    field_names = modelo.get_csv_fields()
    #    v_field_names = field_names
    #except:
    field_names = [field.name for field in table.columns]
    v_field_names = [getattr(field, 'verbose_name') or field.name for field in table.columns]
    v_field_names = map(lambda x: x.encode('utf-8') if x != 'ID' else 'Id', v_field_names)
    w.writerow(v_field_names)
    ax = []



    for obj in table.rows:
        acc = {}
        for columna in range(len(field_names)):             
            uf = unicode(obj[columna]).encode('utf-8').replace("\'", "").replace("\"", "")
            acc[field_names[columna]]=uf
            # try:
            #     uf = unicode(getattr(obj.record, field)()).encode('utf-8')
            # except:
            #     try:
            #         uf = unicode(getattr(obj.record, field)).encode('utf-8')
            #     except:
            #         uf = ''
            # for i, j in replace_dc.iteritems():
            #     uf = uf.replace(i, j)
            # if uf == 'None':
            #     uf = ''
            # acc[field] = uf
        ax.append(acc)

    response.write(get_csv_from_dict_list(field_names, ax))
    return response



def rendiciones_to_csv(modelo, request, table):
    replace_dc = {'\n': '* ', '\r': '', ';': ',', '\"': '|', '\'': '|', 'True': 'Si', 'False': 'No'}
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(table.data.verbose_name_plural.title()+"_"+str(datetime.now().date())).replace('.', '_')
    w = csv.writer(response, delimiter=';')
    
    field_names = [field.name for field in table.columns]
    v_field_names = [getattr(field, 'verbose_name') or field.name for field in table.columns]
    v_field_names = map(lambda x: x.encode('utf-8') if x != 'ID' else 'Id', v_field_names)
    w.writerow(v_field_names)
    ax = []
    cont = 1
    totales=0
    for obj in table.rows:
        acc = {}
        for columna in range(len(field_names)):             
            uf = unicode(obj[columna]).encode('utf-8').replace("\'", "").replace("\"", "")
            acc[field_names[columna]]=uf
        totales = totales + int(acc[field_names[4]])
        ax.append(acc)
        cont = cont + 1
        if cont > 23:
            cont = 1
            corte = {}
            corte[field_names[0]] = "TOTAL DE INGRESOS"
            corte[field_names[1]] = ""
            corte[field_names[2]] = ""
            corte[field_names[3]] = ""
            corte[field_names[4]] = totales
            ax.append(corte)

            en_letras={}
            en_letras[field_names[0]] = "SON GUARANIES: " + num2words(totales, lang='es').upper()
            ax.append(en_letras)

            declaracion={}            
            declaracion[field_names[0]] = "NOTA: DECLARO BAJO FE DE JURAMENTO QUE LOS DATOS EXPUESTOS EN LA PRESENTE PLANILLA REPRESENTAN TODOS LOS INGRESOS PERCIBIDOS EN LA INSTITUCIÓN A MI CARGO. Y QUE LOS ERRORES EN LA PERCEPCION DE LOS INGRESOS Y LA CONFECCION DE LOS COMPROBANTES SON DE MI EXCLUSIVA RESPONSABILIDAD. ADJUNTO FOTOCOPIA DE CEDULA DE IDENTIDAD."
            ax.append(declaracion)
            ax.append("")



            encabezado={}
            for campo in range(len(field_names)):
                encabezado[field_names[campo]] = v_field_names[campo]
            ax.append(encabezado)


            transporte = {}
            transporte[field_names[0]] = "TRANSPORTE"
            transporte[field_names[1]] = ""
            transporte[field_names[2]] = ""
            transporte[field_names[3]] = ""
            transporte[field_names[4]] = totales

            ax.append(transporte)

    response.write(get_csv_from_dict_list(field_names, ax))
    return response



def print_header(table, fila, ws): 
    style0 = xlwt.easyxf('font: name Arial, bold on')
    style1 = xlwt.easyxf('',num_format_str='DD-MMM-YY')
    con_bordes = xlwt.easyxf('font: bold on, height 160; borders: left thin, right thin, top thin, bottom thin; align: wrap on,  horiz center;')

    style = xlwt.XFStyle()
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = xlwt.Style.colour_map['silver_ega']
    style.pattern = pattern

    field_names = [field.name for field in table.columns]
    v_field_names = [getattr(field, 'verbose_name') or field.name for field in table.columns]
    v_field_names = map(lambda x: x.encode('utf-8') if x != 'ID' else 'Id', v_field_names)

    ws.write_merge(fila, fila, 0, 7, unicode('PLANILLA DE EJECUCIÓN DE INGRESOS - DECLARACIÓN JURADA'), xlwt.easyxf("font: bold on, height 220; align: wrap on,  horiz center"))
    ws.row(fila).height = 60*20



    fila=fila+1
    ws.write_merge(fila, fila, 0, 5, unicode('INSTITUCIÓN EDUCATIVA:  INSTITUTO SUPERIOR DE EDUCACIÓN "DR. RAÚL PEÑA"'), xlwt.easyxf("font: bold on, height 160; align: wrap on,  horiz left"))
    ws.write_merge(fila, fila, 6, 7, unicode('TELEFONO: 503012'), xlwt.easyxf("font: bold on, height 160; align: wrap on,  horiz right"))
    ws.row(fila).height = 30*20

    fila=fila+1
    ws.write(fila, 0, unicode('CODIGO INSTITUCIÓN: 1-94-01'), xlwt.easyxf("font: bold on, height 160; align: wrap on,  horiz left"))
    fila=fila+1

    ws.write_merge(fila, fila, 0, 4, unicode('Detalles de Ingresos'), con_bordes)
    ws.write_merge(fila, fila, 5, 7,  unicode('Detalles de Depósitos'), con_bordes)


    fila=fila+1
    for columna in range(len(v_field_names)):
        ws.write(fila, columna, unicode(v_field_names[columna].upper()), xlwt.easyxf("font: bold on, height 120; borders: left thin, right thin, top thin, bottom thin; align: wrap on, vert centre, horiz center;"))
    ws.row(fila).height = 20*20
    fila = fila + 1
    
    return fila, ws



def print_footer(table, fila, ws, total_parcial):
    currency_format = xlwt.XFStyle()
    currency_format.num_format_str = "#,###"
    borders = xlwt.Borders()
    borders.bottom = xlwt.Borders.THIN
    currency_format.borders =borders

    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = xlwt.Style.colour_map['silver_ega']
    currency_format.pattern = pattern

    font = xlwt.Font()
    font.bold = True
    currency_format.font = font

    backgrond_grey = xlwt.easyxf("pattern: pattern solid, fore_color silver_ega; font: bold on, height 160; borders: left thin, right thin, top thin, bottom thin;")
    ws.write(fila, 0, "", backgrond_grey)
    ws.write(fila, 1, "", backgrond_grey)
    ws.write(fila, 2, "", backgrond_grey)
    ws.write(fila, 3, "", backgrond_grey)
    ws.write(fila, 4, total_parcial, currency_format)
    

    ws.write_merge(fila, fila, 5, 6, unicode("TOTAL DE DEPOSITO"), backgrond_grey)
    ws.write(fila, 7, "", backgrond_grey)

    fila=fila+1
    ws.write(fila, 0, unicode("SON GUARANIES: " + num2words(total_parcial, lang='es').upper()) +".------------", xlwt.easyxf("font: bold on, height 160; align: wrap on,  horiz left") )
    fila=fila+1

    ws.write_merge(fila, fila, 0, 7, unicode("NOTA: DECLARO BAJO FE DE JURAMENTO QUE LOS DATOS EXPUESTOS EN LA PRESENTE PLANILLA REPRESENTAN TODOS LOS INGRESOS PERCIBIDOS EN LA INSTITUCIÓN A MI CARGO. Y QUE LOS ERRORES EN LA PERCEPCION DE LOS INGRESOS Y LA CONFECCION DE LOS COMPROBANTES SON DE MI EXCLUSIVA RESPONSABILIDAD. ADJUNTO FOTOCOPIA DE CEDULA DE IDENTIDAD."), xlwt.easyxf("pattern: pattern solid, fore_color silver_ega; font: bold on, height 120; align: wrap on, horiz left"))
    ws.row(fila).height = 20*20
    fila=fila+1

    ws.write_merge(fila, fila, 2, 7, unicode("FIRMA DE LA ENCARGADA DE DESPACHO: ___________________________ "), xlwt.easyxf("font: bold on, height 160; align: wrap on,  horiz center"))
    ws.row(fila).height = 40*20
    fila=fila+1

    ws.write_merge(fila, fila, 2, 7, unicode("ACLARACIÓN  DE FIRMA: Mg. Maria Victoria Zavala"), xlwt.easyxf("font: bold on, height 160; align: wrap on,  horiz center"))
    fila=fila+1


    return fila, ws



from unipath import Path
import xlwt
def rendiciones_to_excel(rendicion, request, table):
    file_path=Path(__file__).ancestor(2) + '/apps/rendiciones/excels/'
    file_name='declaracion_nro_'+unicode(rendicion.nro_rendicion)+'_'+unicode(datetime.now())+'.xls'
    file_path = file_path+file_name


    style1 = xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin;')
    
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/mm/yyyy'


    currency_format = xlwt.XFStyle()
    currency_format.num_format_str = "#,###"
    borders = xlwt.Borders()
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.bottom = xlwt.Borders.THIN
    currency_format.borders =borders


    wb = xlwt.Workbook()
    ws = wb.add_sheet('Hoja1',cell_overwrite_ok=True)


        
    fila = 0

    total=0
    total_parcial=0
    contador=1
    transporte=0
    for obj in table.rows:
        if contador == 24: 
            fila, ws = print_footer(table, fila, ws, total_parcial)
            contador=1
        if contador==1:
            fila, ws = print_header(table, fila, ws)

        if contador==1 and total_parcial!=0:
            currency_format_bold = xlwt.XFStyle()
            currency_format_bold.num_format_str = "#,###"
            borders = xlwt.Borders()
            borders.right = xlwt.Borders.THIN
            currency_format_bold.borders =borders
            font = xlwt.Font()
            font.bold = True
            currency_format_bold.font = font

            ws.write(fila, 0, unicode("TRANSPORTE"), xlwt.easyxf("font: bold on, height 190; align: wrap on,  horiz left; borders: left thin, right thin, top thin, bottom thin;"))
            ws.write(fila, 4, total_parcial, currency_format_bold)
            ws.write(fila, 5, "", style1)
            ws.write(fila, 6, "", style1)
            ws.write(fila, 7, "", style1)

            transporte=total_parcial
            fila=fila+1

        ws.write(fila, 0, unicode(obj[0]), xlwt.easyxf('font: height 150; borders: left thin, right thin, top thin, bottom thin;'))
        ws.write(fila, 1, obj[1], style1)
        ws.write(fila, 2, unicode(obj[2]), xlwt.easyxf('align: wrap on, horiz center; borders: left thin, right thin, top thin, bottom thin;'))
        ws.write(fila, 3, (obj[3]), style1)
        ws.write(fila, 4, (obj[4]), currency_format)
        ws.write(fila, 5, "-", style1)
        ws.write(fila, 6, "-", style1)
        ws.write(fila, 7, "-", style1)

        # for columna in range(8):
        #     ws.write(fila, columna, unicode(obj[columna]), style1)
        total_parcial=total_parcial+obj[4]
        
        fila=fila+1
        contador=contador+1

    fila, ws = print_footer(table, fila, ws, total_parcial)
    wb.save(file_path)

    return xls_to_response(wb, file_name)






