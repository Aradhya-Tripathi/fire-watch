from rest_framework.permissions import BasePermission
from .utils import get_token, validate_unit_id
from free_watch.errorfactory import InvalidUid


class ValidateUnit(BasePermission):
    def has_permission(self, request, view):
        """Token collected from headers, here token refers to
        the unit Id of the device. Set `request.unit_id` if token is validated.
        """
        token = get_token(request.headers)
        validate_unit_id(token)
        setattr(request, "unit_id", token)
        return True
