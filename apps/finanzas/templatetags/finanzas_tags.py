from django import template
register = template.Library()
from apps.finanzas.models import PlanPago
from apps.descuentos.models import Descuento

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

@register.filter("get_descuento_porcentaje")
def get_descuento_porcentaje(instance, id_descuento):
	descuento=Descuento.objects.get(pk=id_descuento)
	try: return descuento.porcentaje
	except: pass

