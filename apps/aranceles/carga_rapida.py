# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os, sys
#sys.path.append('/home/ruben/apps/iseapp/iseapp')
os.environ["DJANGO_SETTINGS_MODULE"] = "iseapp.settings.local"
print os.environ["DJANGO_SETTINGS_MODULE"]
from apps.aranceles.models import arancel, concepto, periodo
from django.contrib.auth.models import User

conceptos=concepto.objects.all().order_by('id')
for c in conceptos:
	print c
	monto = raw_input("MONTO :")
	a=arancel()
	a.resolucion  = periodo.objects.get(resolucion='5755')
	a.concepto  = c
	a.fraccionable  = False
	a.monto = int(monto)
	a.created_by = User.objects.get(pk=1)
	a.save()
	print a
