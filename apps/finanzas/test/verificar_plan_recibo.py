#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
from django.core.wsgi import get_wsgi_application
sys.path.append('/home/ruben/apps/iseapp/iseapp')
os.environ["DJANGO_SETTINGS_MODULE"] = "iseapp.settings.local"
application = get_wsgi_application()
from apps.finanzas.models import PlanPago


planes = PlanPago.objects.filter(estado='PAG')
for plan in planes:
	if plan.get_recibo==None:
		print plan.curso_alumno
