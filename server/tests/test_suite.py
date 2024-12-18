import unittest

from domain.test_strategy import TestStrategy


def create_test_suite():
    suite = unittest.TestSuite()

    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestStrategy))

    return suite


if __name__ == "__main__":
    suite = create_test_suite()
    runner = unittest.TextTestRunner()
    runner.run(suite)
