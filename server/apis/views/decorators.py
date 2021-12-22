from typing import List, Optional

from apis.views import api_view as base_api_view
from fire_watch.throttle import Throttle


def api_view(
    http_methods: List[str],
    throttle_classes: Optional[List[type]] = [Throttle],
    permission_classes: Optional[List[type]] = None,
):
    """Custom decorator behaves almost like `rest_framework.decorators.api_view`
    just adds all permissions and throttles in one wrapper.

    Args:
        http_methods (List[str]): HTTP methods
        throttle_classes (Optional[List[type]], optional): Throttle Classes for this view. Defaults to `Throttle`.
        permission_classes (Optional[List[type]], optional): Permission Classes for this view. Defaults to None.
    """

    def decorator(func):
        func.throttle_classes = throttle_classes if throttle_classes else []
        func.permission_classes = permission_classes if permission_classes else []
        func = base_api_view(http_methods)(func)
        return func

    return decorator
