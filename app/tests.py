import unittest
# import flaskr
from app import app


# app = Flask(__name__)

class BaseTestCase(unittest.TestCase):

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, b'Hello, World!')


if __name__ == '__main__':
    unittest.main()
