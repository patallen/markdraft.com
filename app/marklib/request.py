from flask import Response
import json


class XHRResponse(Response):
    default_mimetype = 'application/json'


class MakeResponse(object):
    _response = XHRResponse()

    def add_header(self, header, override=True):
        (k, v) = header.items()
        if self._response.headers.get(k) is None or override:
            self.set_header(k, v)

    def set_header(self, header, value):
        self._response.headers[header] = value

    def set_body(self, data):
        res = dict(results=data)
        self._response.set_data(json.dumps(res, indent=4))

    def set_status(self, code):
        self._response.staus_code = code

    def set_error(self, code=None, error=None):
        if isinstance(code, int):
            self.set_status(code)
        if isinstance(error, str):
            self.set_body(error)

    def set_content_type(self, content_type):
        self.set_header('Content-Type', content_type)

    @property
    def response(self):
        return self._response
