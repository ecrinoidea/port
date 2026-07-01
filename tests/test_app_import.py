import unittest

import app


class AppImportTest(unittest.TestCase):
    def test_flask_app_imports(self):
        self.assertIsNotNone(app.app)
        self.assertEqual(app.app.name, 'app')


if __name__ == '__main__':
    unittest.main()
