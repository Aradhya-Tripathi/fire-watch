import free_watch


def check_subscription():
    """
    Check all subscriptions mentioned in configuration
    return list of all subscriptions for alerts
    """
    alerts = free_watch.conf.send_alerts
    if alerts:
        return alerts
