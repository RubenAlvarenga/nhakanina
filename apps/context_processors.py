from django.core.urlresolvers import reverse, resolve
from apps.middlewares import RequestTimeLoggingMiddleware
from django.http import HttpResponse
from apps.autorizaciones.models import Enlace, MenuApp, Agrupador
from django.contrib.auth.models import Permission
from django.db.models import Count

num2words1 = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten', 11: 'Eleven', 12: 'Twelve', 13: 'Thirteen', 14: 'Fourteen', 15: 'Fifteen', 16: 'Sixteen', 17: 'Seventeen', 18: 'Eighteen', 19: 'Nineteen'}
num2words2 = ['Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
def number(Number):
    if (Number > 1) or (Number < 19):
        return (num2words1[Number])
    elif (Number > 20) or (Number < 99):
        return (num2words2[Number])

from itertools import chain
def menu(request):
    url_actual = resolve(request.path)
    menu = {}
    active = None
    try: usuario=request.user
    except: usuario=False
    if usuario.is_authenticated():
        if usuario.is_superuser:
            enlaces = Enlace.objects.all()
            menu['sistemas'] = enlaces.values('app__titulo', 'app__icono', 'app__app_name', 'app__index').annotate(dcount=Count('app'))
        else:
            #permisos = usuario.get_all_permissions()
            permisos_user = Permission.objects.filter(user=usuario)
            permisos_group = Permission.objects.filter(group__user=usuario)
            permisos = list(chain(permisos_user, permisos_group))

            enlaces = Enlace.objects.filter(permiso__in=permisos)



            menu['sistemas'] = enlaces.values('app__titulo', 'app__icono', 'app__app_name', 'app__index').annotate(dcount=Count('app'))
            
        sistemaActual= request.session.get('sistema')

        menu['url_actual'] = url_actual
        if sistemaActual:
            sistema = MenuApp.objects.get(pk=sistemaActual)
            menu['sistema'] = sistema
            enlaces = enlaces.filter(app=sistema)
            for link in enlaces:
                if url_actual.view_name == link.enlace:
                    link.active=True
                    active = link.grupo
            print enlaces
            agrupador = enlaces.values('grupo__grupo', 'grupo__icono', 'grupo__id').annotate(dcount=Count('grupo'))
            for item in agrupador:
                item['url'] = 'collapse'+unicode(number(item['grupo__id']))
                if active:
                    if item['grupo__grupo'] == active.grupo: 
                         item['active'] = 'in'
                item['enlaces'] = enlaces.filter(grupo__id=int(item['grupo__id']))
                
            menu['enlaces'] = agrupador






# Request Method: GET
# Request URL:    http://localhost:8000/entidades/
# Django Version: 1.8.3
# Exception Type: UnboundLocalError
# Exception Value:    
# local variable 'enlaces' referenced before assignment
# Exception Location: /home/ruben/apps/iseapp/iseapp/apps/context_processors.py in menu, line 45    


    # secciones=request.path.split('/')
    # for item in menu['menu']:
    #   for i in item['submenu']:
    #       if i['url'].split('/')[1] == secciones[1]:
    #           item['active']='in'
    #           if request.path==i['url']:
    #               i['active']=True

    # breadcrumbs=[]
    # #breadcrumbs.append({'name':'index', 'url': '/'})
    # secciones.remove('')

    # anterior='/'
    # try:
    #   if int(secciones[-1]):
    #       item=secciones.pop(-1)
    #       secciones[-1]=secciones[-1]+'/'+item
    # except:
    #   pass

    # for secc in secciones:
    #   breadcrumbs.append({'name':secc, 'url': str(anterior)+str(secc) })      
    #   anterior=str(anterior)+str(secc)+'/'



    # menu['breadcrumbs']=breadcrumbs           #print 'path :', request.path
    return menu

