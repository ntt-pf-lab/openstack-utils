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
import time
import webob.dec

from nova import flags
from nova import log as logging
from nova import wsgi


FLAGS = flags.FLAGS

flags.DEFINE_integer('max_response_len', -1,
                     'maximum length of the API response body to include in '\
                     'the log (-1 means log complete value)')


class DebugLogger(wsgi.Middleware):
    """Helper class for debugging a WSGI application.

    Can be inserted into any WSGI application chain to log information
    about the request and response.

    """

    def __init__(self, application, **global_config):
        super(DebugLogger, self).__init__(application)
        self.LOG = logging.getLogger('nova.debug_logger')

    @webob.dec.wsgify(RequestClass=wsgi.Request)
    def __call__(self, req):
        if len(req.body):
            body = req.body
        else:
            body = '-'
        input_params = "METHOD: %s URL: %s BODY: '%s'" % (req.method,
                                                        req.url,
                                                        body)
        start_time = time.time()
        resp = req.get_response(self.application)
        end_time = time.time()

        #set the request_id in cookie
        request_id = 'NA'
        if req.environ.get('nova.context', None):
            request_id = req.environ['nova.context'].request_id
        resp.set_cookie('request_id', request_id)

        response_str = resp.body
        if FLAGS.max_response_len != -1:
            response_str = response_str[0:FLAGS.max_response_len]

        log_str = "REQUEST ID: %s TIME: %.3f %s RESPONSE STATUS: '%s' "\
                    "RESPONSE: '%s'" % \
                  (request_id,
                   end_time - start_time,
                   input_params,
                   resp.status,
                   response_str)
        self.LOG.info(log_str)
        return resp
