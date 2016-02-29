from marklib import request
from tests import BaseTestCase


class MakeResponseTestCase(BaseTestCase):
    def test_makeresponse_init(self):
        xhr = request.MakeResponse(404, error="ERROR")
        self.assertEqual(xhr.response.status_code, 404)
        self.assertTrue("ERROR" in xhr.response.data)

    def test_set_body(self):
        res = request.MakeResponse(200)
        res.set_body("This is the body.")
        self.assertEqual(res.response.status_code, 200)
        self.assertTrue("This is the body." in res.response.data)

    def test_init_with_body(self):
        res = request.MakeResponse(200, body="BODY")
        self.assertEqual(res.response.status_code, 200)
        self.assertTrue("BODY" in res.response.data)

    def test_add_header(self):
        res = request.MakeResponse(200)
        res.add_header({"Authorization": "Bearer"})
        self.assertTrue("Authorization" in res.response.headers.keys())

    def test_set_content_type(self):
        res = request.MakeResponse(200)
        res.set_content_type("text/html")
        ctype = res.response.headers.get('Content-Type')
        self.assertEqual(ctype, "text/html")
