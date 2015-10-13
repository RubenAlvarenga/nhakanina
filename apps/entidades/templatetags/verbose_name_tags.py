from django import template
register = template.Library()

# def get_field_verbose_name(instance, arg):
#     #return instance._meta.get_field(arg).verbose_name
# 	return instance._meta.get_field(arg).verbose_name.title()
# register.filter('field_verbose_name', get_field_verbose_name)

def get_verbose_name(object): 
    return object._meta.verbose_name
register.filter('get_verbose_name', get_verbose_name)

@register.simple_tag
def get_verbose_field_name(instance, field_name):
    return instance._meta.get_field(field_name).verbose_name.title()

@register.simple_tag
def get_verbose_form_name(instance):
    return instance._meta.get_field(field_name).verbose_name.title()


def get_queryset_verbose_name(queryset):
    return queryset.model._meta.verbose_name
register.filter('queryset_verbose_name', get_queryset_verbose_name)

def get_queryset_verbose_name_plural(queryset):
    return queryset.model._meta.verbose_name_plural
register.filter('queryset_verbose_name_plural', get_queryset_verbose_name_plural)

def form_model_name(form):
    return form._meta.model._meta.verbose_name
register.filter('form_model_name', form_model_name)

def get_list_pages(table):
    total=table.paginator.num_pages
    actual=table.page.number
    if actual > 0 and actual < 6: 
        desde = 0
        hasta = 5
    else:
        if actual > total - 4:
            desde = total -10
        else:
            desde = actual - 5
        hasta = actual
    rango_total = table.paginator.page_range
    rango_nuevo = rango_total[desde : hasta + 4]
    if rango_nuevo[0] != 1:
        rango_nuevo = [1, "..."] + rango_nuevo
    if rango_nuevo[-1] != total:
        rango_nuevo =  rango_nuevo + ["...", total]
    return  rango_nuevo
register.filter('get_list_pages', get_list_pages)


@register.filter('klass')
def klass(ob):
    return ob.__class__.__name__



 