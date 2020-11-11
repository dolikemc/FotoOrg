import unittest
import mock
import main


class TestMain(unittest.TestCase):
    def test_cover_main(self):
        with mock.patch.object(main, "main", return_value=True):
            with mock.patch.object(main, "__name__", "__main__"):
                with mock.patch.object(main.sys, 'exit') as mock_exit:
                    main.init()
                    self.assertTrue(mock_exit.call_args[0][0])

    def test_main(self):
        self.assertTrue(main.main())
