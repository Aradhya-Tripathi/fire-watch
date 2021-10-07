from core import conf
from apis import model


def check_subscription():
    """
    Check all subscriptions mentioned in configuration
    return list of all subscriptions for alerts
    """
    alerts = conf["send_alerts"]
    if alerts:
        return alerts


def log_warnings(token: str):
    # TODO: Logging
    ...
