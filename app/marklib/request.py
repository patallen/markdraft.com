from flask import Response
import json


class XHRResponse(Response):
    default_mime_type = 'application/json'


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
        self._response.set_data(json.dumps(res))

    def set_status(self, code):
        self._response.staus_code = code

    def response(self):
        return self._response
