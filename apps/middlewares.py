#!/usr/bin/env python
# -*- coding: utf-8 -*-
from apps.autorizaciones.models import MenuApp
from django.core.urlresolvers import resolve
import logging
import sys
import datetime
import uuid
from django.core import serializers
from apps.autorizaciones.models import Perfil


class RequestAddSessionVars(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try: sistema = MenuApp.objects.get(app_name=resolve(request.path).app_name).id
        except: sistema = False
        request.session["sistema"]=sistema







class RequestTimeLoggingMiddleware(object):
    """Middleware class logging request time to stderr.

    This class can be used to measure time of request processing
    within Django.  It can be also used to log time spent in
    middleware and in view itself, by putting middleware multiple
    times in INSTALLED_MIDDLEWARE.

    Static method `log_message' may be used independently of the
    middleware itself, outside of it, and even when middleware is not
    listed in INSTALLED_MIDDLEWARE.
    """

    @staticmethod
    def log_message(request, tag, message=''):
        """Log timing message to stderr.

        Logs message about `request' with a `tag' (a string, 10
        characters or less if possible), timing info and optional
        `message'.

        Log format is "timestamp tag uuid count path +delta message"
        - timestamp is microsecond timestamp of message
        - tag is the `tag' parameter
        - uuid is the UUID identifying request
        - count is number of logged message for this request
        - path is request.path
        - delta is timedelta between first logged message
          for this request and current message
        - message is the `message' parameter.
        """
        
        dt = datetime.datetime.utcnow()
        if not hasattr(request, '_logging_uuid'):
            request._logging_uuid = uuid.uuid1()
            request._logging_start_dt = dt
            request._logging_pass = 0

        request._logging_pass += 1
        # return sys.stderr, (
        #     u'%s %-10s %s %2d %s +%s %s' % (
        #         dt.isoformat(),
        #         tag,
        #         request._logging_uuid,
        #         request._logging_pass,
        #         request.path,
        #         dt - request._logging_start_dt,
        #         message,
        #         )
        #     ).encode('utf-8')
        return dt - request._logging_start_dt

    def process_request(self, request):
        self.log_message(request, 'request ')


    def process_template_response(self, request, response):
        if response.__class__.__name__ == "TemplateResponse":
            response.context_data['tiempo'] = self.log_message(request, 'response')
        return response


    def process_response(self, request, response):
        # s = getattr(response, 'status_code', 0)
        # r = str(s)
        # if response.__class__.__name__ == 'StreamingHttpResponse':
        #     if s in (300, 301, 302, 307):
        #         r += ' => %s' % response.get('Location', '?')
        #     elif response.streaming_content:
        #         r += ' (%db)' % len(response.streaming_content)

        # else:
        #     if s in (300, 301, 302, 307):
        #         r += ' => %s' % response.get('Location', '?')
        #     elif response.content:
        #         r += ' (%db)' % len(response.content)
        # #self.log_message(request, 'response', r)


        response = self.process_template_response(request, response)
        return response