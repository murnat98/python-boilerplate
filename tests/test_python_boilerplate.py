from unittest import TestCase

from python_boilerplate import __version__


class TestPythonBoilerplate(TestCase):
    def test_version(self):
        self.assertEqual('0.1.0', __version__)
