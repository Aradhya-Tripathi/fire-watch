from rest_framework.permissions import BasePermission

from authentication import issue_keys
import fire_watch

from .utils import get_token, validate_unit_id


class ValidateUnit(BasePermission):
    def has_permission(self, request, view):
        """Token collected from headers, here token refers to
        the unit Id of the device. Set `request.unit_id` if token is validated.
        """
        token = get_token(request.headers)
        request.unit_id, request.email = token, validate_unit_id(token)
        return True


class RefreshToAccessPermission(BasePermission):
    def has_permission(self, request, view):
        """Allow accessing refresh route with valid refresh token,
        check for blacklisted refresh tokens as well.
        """
        token = get_token(headers=request.headers)
        if issue_keys.is_valid_refresh(key=token) and not fire_watch.cache.sismember(
            "Blacklist", token
        ):
            request.refresh_token = token
            return True
