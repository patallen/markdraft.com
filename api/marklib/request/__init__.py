from flask import Response
import json


class XHRResponse(Response):
    default_mimetype = 'application/json'


class MakeResponse(object):
    _response = XHRResponse()
    res_dict = {}

    def __init__(self, status_code=None, body=None, error=None):
        self.response.set_data({})
        self.set_status(200)

        self.res_dict = {"status": "success"}

        if status_code:
            self.set_status(status_code)
        if body:
            self.set_body(body)
        if error:
            self.set_error(msg=error)

    def add_header(self, header, override=True):
        for k, v in header.items():
            if self._response.headers.get(k) is None or override:
                self.set_header(k, v)

    def set_header(self, header, value):
        self._response.headers[header] = value

    def set_body(self, data):
        self.res_dict["results"] = data
        if self.res_dict.get("error"):
            self.res_dict.pop("error")

    def set_status(self, code=None):
        self._response.status_code = code
        if code < 200 or code >= 300:
            self.res_dict["status"] = "error"
        else:
            self.res_dict["status"] = "success"

    def set_error(self, code=None, msg=None):
        self.res_dict["error"] = msg
        self.res_dict["status"] = "error"
        if self.res_dict.get('results'):
            self.res_dict.pop("results")
        if code:
            self.set_status(code)

    def set_content_type(self, content_type):
        self.set_header('Content-Type', content_type)

    @property
    def response(self):
        self._response.set_data(json.dumps(self.res_dict, indent=4))
        return self._response
