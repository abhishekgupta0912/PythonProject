from app import app
import unittest
import requests
import os


class test(unittest.TestCase):
    API_URI = 'http://127.0.0.1:5000'

    # Ensure flask api is Listening
    def test_delete(self):
        # tester = app.test_client(self)
        # r = tester.get(test.API_URI)
        r1 = requests.get(test.API_URI)
        self.assertEqual(r1.status_code, 200)

    def test_insert(self):
        data = {
            'name': "Mr.A",
            'email': "abhishek.gupta1_cs18@yahoo.com",
            'phone': "8630444356"

        }
        # tester = app.test_client(self)
        # r = tester.post("http://127.0.0.1:5000/insert", data=data, content_type='html/text')
        r1 = requests.post(test.API_URI + "/insert", data=data)
        self.assertEqual(r1.status_code, 200)



if __name__ == '_main_':
    unittest.main(exit=False)
