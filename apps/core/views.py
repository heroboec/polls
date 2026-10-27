from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class FooBar(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return JsonResponse({"FooBar": 1})

