from django import template
register = template.Library()
from apps.finanzas.models import PlanPago

@register.filter("get_monto_plan")
def get_monto_plan(instance, id_plan):
	plan=PlanPago.objects.get(pk=id_plan)
	return plan.monto

@register.filter("get_mes_plan")
def get_monto_plan(instance, id_plan):
	plan=PlanPago.objects.get(pk=id_plan)
	return plan.vencimiento

@register.filter("get_materia_plan")
def get_materia_plan(instance, id_plan):
	plan=PlanPago.objects.get(pk=id_plan)
	try: return plan.materia.nombre
	except: pass

# def get_field_verbose_name(instance, arg):
#     #return instance._meta.get_field(arg).verbose_name
# 	return instance._meta.get_field(arg).verbose_name.title()
# register.filter('field_verbose_name', get_field_verbose_name)

# def get_verbose_name(object): 
#     return object._meta.verbose_name
# register.filter('get_verbose_name', get_verbose_name)

# @register.simple_tag
# def get_verbose_field_name(instance, field_name):
#     return instance._meta.get_field(field_name).verbose_name.title()

# @register.simple_tag
# def get_verbose_form_name(instance):
# 	#pass
#     return instance._meta.get_field(field_name).verbose_name.title()


# def get_queryset_verbose_name(queryset):
#     return queryset.model._meta.verbose_name
# register.filter('queryset_verbose_name', get_queryset_verbose_name)

# def get_queryset_verbose_name_plural(queryset):
#     return queryset.model._meta.verbose_name_plural
# register.filter('queryset_verbose_name_plural', get_queryset_verbose_name_plural)

# def form_model_name(form):
#     return form._meta.model._meta.verbose_name
# register.filter('form_model_name', form_model_name)



# @register.filter('klass')
# def klass(ob):
#     return ob.__class__.__name__