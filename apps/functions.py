#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.template import Template, Context


def msg_render(msg):
    return Template(msg).render(Context())


def mesificar(enteromes):
	if enteromes==1: mesificado='Ene'
	elif enteromes==2: mesificado='Feb'
	elif enteromes==3: mesificado='Mar'
	elif enteromes==4: mesificado='Abr'
	elif enteromes==5: mesificado='May'
	elif enteromes==6: mesificado='Jun'
	elif enteromes==7: mesificado='Jul'
	elif enteromes==8: mesificado='Ago'
	elif enteromes==9: mesificado='Sep'
	elif enteromes==10: mesificado='Oct'
	elif enteromes==11: mesificado='Nov'
	elif enteromes==12: mesificado='Dic'
	else: mesificado='-'
	return mesificado

