import fire_watch
from functools import lru_cache


@lru_cache()
def check_subscription():
    """
    Check all subscriptions mentioned in configuration
    return list of all subscriptions for alerts
    """
    alerts = fire_watch.conf.send_alerts
    if alerts:
        return alerts
