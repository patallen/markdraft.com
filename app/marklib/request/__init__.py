from flask import Response
import json


class XHRResponse(Response):
    default_mimetype = 'application/json'


class MakeResponse(object):
    _response = XHRResponse()

    def __init__(self, status_code=None, body=None, error=None):
        super(MakeResponse, self).__init__()
        self.response.set_data({})
        if status_code:
            self.set_status(status_code)
        if body:
            self.set_body(body)
        if error:
            self.set_error(error=error)

    def add_header(self, header, override=True):
        (k, v) = header.items()
        if self._response.headers.get(k) is None or override:
            self.set_header(k, v)

    def set_header(self, header, value):
        self._response.headers[header] = value

    def set_body(self, data):
        res = dict(results=data)
        self._response.set_data(json.dumps(res, indent=4))

    def set_status(self, code=None, msg=None):
        self._response.status_code = code

    def set_error(self, code=None, error=None):
        res = dict(error=error)
        self._response.set_data(json.dumps(res, indent=4))

    def set_content_type(self, content_type):
        self.set_header('Content-Type', content_type)

    @property
    def response(self):
        return self._response
