import argparse
import unittest
from importlib import import_module

import patches
from authentication.tests import test_auth_model, test_jwt, test_refresh_to_access
from fire_watch.log.tests import test_logging
from tests import (
    test_admin,
    test_login,
    test_reset_password,
    test_units,
    test_user_operations,
    test_refresh_token,
    test_logout,
)


def configure_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--unit-tests", nargs=1, default=[0], type=int)
    parser.add_argument("--allow-both", nargs=1, default=[0], type=int)
    parser.add_argument("--module", nargs=2, default=[0, 0])
    return parser


def get_unittests(suite):
    suite.addTest(unittest.makeSuite(test_auth_model.TestAuthModel))
    suite.addTest(unittest.makeSuite(test_jwt.TestJwt))
    suite.addTest(unittest.makeSuite(test_logging.TestLog))
    suite.addTest(unittest.makeSuite(test_refresh_to_access.TestAccessToRefresh))


def get_server_tests(suite):
    suite.addTest(unittest.makeSuite(test_login.TestAuthentication))
    suite.addTest(unittest.makeSuite(test_units.TestUnit))
    suite.addTest(unittest.makeSuite(test_reset_password.TestResetPassword))
    suite.addTest(unittest.makeSuite(test_user_operations.UserTests))
    suite.addTest(unittest.makeSuite(test_admin.TestAdmin))
    suite.addTest(unittest.makeSuite(test_refresh_token.TestRefreshToAccess))
    suite.addTest(unittest.makeSuite(test_logout.TestLogout))


def main():
    suite = unittest.TestSuite()
    options = configure_options().parse_args()

    if value := options.module[0]:
        module = import_module(value)
        test_class = getattr(module, options.module[1])
        suite.addTest(unittest.makeSuite(test_class))

    elif not options.allow_both[0]:
        if options.unit_tests[0]:
            # Add module level unit tests to test suite
            get_unittests(suite)
        else:
            get_server_tests(suite)

    else:
        get_unittests(suite)
        get_server_tests(suite)

    output = unittest.TextTestRunner(verbosity=2).run(suite)
    if output.errors or output.failures:
        print("Failing Tests")


if __name__ == "__main__":
    main()
