#!/usr/bin/env python
# -*- coding: utf-8 -*-
import calendar
import datetime


def ultimo_dia_del_mes(fecha):
    firstweekday, days=calendar.monthrange(fecha.year, fecha.month)
    return datetime.date(fecha.year, fecha.month, days)

def sumar_mes(fecha, months):
    month = fecha.month - 1 + months
    year = fecha.year + month / 12
    month = month % 12 + 1
    day = min(fecha.day,calendar.monthrange(year,month)[1])
    return datetime.date(year,month,day)
