from django.http import request
from django.http.response import JsonResponse
from fire_watch.throttle import Throttle
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.views import APIView

from .base_view import BaseAPIView