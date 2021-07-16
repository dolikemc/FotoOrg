import unittest
from main import start_application
from os import getenv


class ApplicationTestCase(unittest.TestCase):
    """These methods are going to be the same for every GUI test,
    so refactored them into a separate class
    """

    # this will run on a separate thread.
    async def _start_app(self):
        self.app.mainloop()

    def setUp(self):
        if getenv('DISPLAY', '') == '':
            self.skipTest('no display set')
        self.app = start_application()
        self._start_app()

    def tearDown(self):
        pass

    def test_startup(self):
        title = self.app.winfo_toplevel().title()
        expected = 'tk'
        self.assertEqual(title, expected)
