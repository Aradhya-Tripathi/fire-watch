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


def pagination_utils(page, page_limit):
    page = 1 if (page == 0 or page < 0) else page
    skip = (page * page_limit) - page_limit
    return skip
