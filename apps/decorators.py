from django.contrib import messages
from django.http import HttpResponseRedirect

decorator_with_arguments = lambda decorator: lambda *args, **kwargs: lambda func: decorator(func, *args, **kwargs)


@decorator_with_arguments
def custom_permission_required(function, perm):
    def _function(request, *args, **kwargs):
        if request.user.has_perm(perm):
            return function(request, *args, **kwargs)
        else:
            mensaje = "ACCESO RESTRINGIDO | Permiso Requerido: "+str(perm)
            messages.add_message(request, messages.ERROR, mensaje, extra_tags='danger')
            try: url = request.META['HTTP_REFERER']
            except: url = '/' 

            return HttpResponseRedirect(url)
    return _function