import hello
import unittest


class TestCase(unittest.TestCase):

    def setUp(self):
        hello.app.config['TESTING'] = True
        self.app = hello.app.test_client()

    def test_status_code(self):
        rv = self.app.get('/hello')
        assert rv.status_code == 200

    def test_message(self):
        rv = self.app.get('/hello')
        assert rv.data == 'Hello World!'

if __name__ == "__main__":
    unittest.main()