#!/usr/bin/env python
# -*- coding: utf-8 -*-
from apps.entidades.models import Persona


def es_socio_afemec(request):
    try: persona = Persona.objects.get(pk=int(request.POST['id_persona']))
    except: persona = Persona.objects.get(pk=int(request.POST['persona']))
    if persona.socio_afemec: return True
    else: return False

def es_docente_ise(request):
    try: persona = Persona.objects.get(pk=int(request.POST['id_persona']))
    except: persona = Persona.objects.get(pk=int(request.POST['persona']))
    if persona.docente_ise: return True
    else: return False