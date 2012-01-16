# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 OpenStack LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


"""Utility that logs each API request and response details"""
import logging
import time
import webob.dec

from glance.common import wsgi


class DebugLogger(wsgi.Middleware):
    """Helper class for debugging a WSGI application.

    Can be inserted into any WSGI application chain to log information
    about the request and response.

    """

    @classmethod
    def factory(cls, global_config, **local_config):
        def _factory(app):
            return cls(app, **local_config)
        return _factory

    def __init__(self, application, **kwargs):
        self.application = application
        self.LOG = logging.getLogger('glance.common.debug_logger')
        try:
            self.max_response_len = int(kwargs.get('MAX_RESPONSE_LEN', 200))
        except ValueError:
            msg = _("Invalid value specified for MAX_RESPONSE_LEN '%s'" %
                    kwargs.get('MAX_RESPONSE_LEN'))
            self.LOG.error(msg)
            raise RuntimeError(msg)

    @webob.dec.wsgify
    def __call__(self, req):
        if self.max_response_len != -1:
            if req.method in ('POST', 'PUT') and \
               req.content_type == 'application/octet-stream':
                body = ''
            else:
                body = req.body[:self.max_response_len]
        else:
            body = req.body

        if body == '':
            body = '-'

        start_time = time.time()
        resp = req.get_response(self.application)
        end_time = time.time()

        #set the request_id in cookie
        request_id = 'NA'
        if req.environ.get('context', None) and \
           hasattr(req.environ['context'], request_id):
            request_id = req.environ['context'].request_id

        resp.set_cookie('request_id', request_id)

        if self.max_response_len != -1:
            if resp.headers['Content-Type'] == 'application/octet-stream':
                response_str = ''
            else:
                response_str = resp.body[:self.max_response_len]
        else:
            response_str = resp.body
        log_str = "REQUEST ID: %s TIME: %.3f METHOD: %s URL: %s BODY: '%s' "\
                    "RESPONSE STATUS: '%s' RESPONSE: '%s'" % \
                  (request_id,
                   end_time - start_time,
                   req.method,
                   req.url,
                   body,
                   resp.status,
                   response_str)

        self.LOG.info(log_str)
        return resp
