from free_watch.errorfactory import SocketAuthenticationFailed


def authenticate(scope):
    if "error" in scope:
        raise SocketAuthenticationFailed()
