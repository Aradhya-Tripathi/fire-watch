import unittest
from tests import test_server, test_units


def main():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(test_server.TestServer))
    suite.addTest(unittest.makeSuite(test_units.TestUnit))

    output = unittest.TextTestRunner().run(suite)
    if output.errors or output.failures:
        print("Failing Tests")


if __name__ == "__main__":
    main()
