from free_watch import conf


def check_subscription():
    """
    Check all subscriptions mentioned in configuration
    return list of all subscriptions for alerts
    """
    alerts = conf["send_alerts"]
    if alerts:
        return alerts
