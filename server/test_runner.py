import unittest
from tests import test_login, test_units
from authentication.tests import test_auth_model, test_jwt

import argparse


def configure_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--unit-tests", nargs=1, default=[0], type=int)
    parser.add_argument("--allow-both", nargs=1, default=[0], type=int)
    return parser


def get_unittests(suite):
    suite.addTest(unittest.makeSuite(test_auth_model.TestAuthModel))
    suite.addTest(unittest.makeSuite(test_jwt.TestJwt))


def get_server_tests(suite):
    suite.addTest(unittest.makeSuite(test_login.TestServer))
    suite.addTest(unittest.makeSuite(test_units.TestUnit))


def main():
    suite = unittest.TestSuite()
    options = configure_options().parse_args()

    if not options.allow_both[0]:
        if options.unit_tests[0]:
            # Add module level unit tests to test suite
            get_unittests(suite)
        else:
            get_server_tests(suite)

    else:
        get_unittests(suite)
        get_server_tests(suite)

    output = unittest.TextTestRunner().run(suite)
    if output.errors or output.failures:
        print("Failing Tests")


if __name__ == "__main__":
    main()