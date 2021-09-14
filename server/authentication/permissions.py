from rest_framework.permissions import BasePermission
from .utils import get_token, validate_token
from core.errorfactory import InvalidUid


class ValidateUnit(BasePermission):
    def has_permission(self, request, view):
        try:
            token = get_token(request.headers)
        except Exception:
            return False
        try:
            validate_token(token)
        except InvalidUid:
            return False
        setattr(request, "unit_id", token)
        return True
