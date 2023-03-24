from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    if isinstance(exc, ValidationError):
        return Response({'error': exc.message}, status=400)
    return exception_handler(exc, context)
