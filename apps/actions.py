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
            uf = unicode(obj[columna]).encode('utf-8').replace("\'", "")
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
    v_field_names.append("Comprobante de Deposito Nro")
    v_field_names.append("Fecha de Deposito")
    v_field_names.append("Monto del Deposito")
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
        if cont > 18:
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