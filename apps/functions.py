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

def mes_en_letras(enteromes):
	if enteromes==1: mesificado='Enero'
	elif enteromes==2: mesificado='Febrero'
	elif enteromes==3: mesificado='Marzo'
	elif enteromes==4: mesificado='Abril'
	elif enteromes==5: mesificado='Mayo'
	elif enteromes==6: mesificado='Junio'
	elif enteromes==7: mesificado='Julio'
	elif enteromes==8: mesificado='Agosto'
	elif enteromes==9: mesificado='Septiembre'
	elif enteromes==10: mesificado='Octubre'
	elif enteromes==11: mesificado='Noviembre'
	elif enteromes==12: mesificado='Diciembre'
	else: mesificado='-'
	return mesificado