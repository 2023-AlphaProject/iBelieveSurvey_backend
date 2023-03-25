from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler


def validate_multiple(*validation_methods):
    exceptions = []
    for validation_method in validation_methods:
        try:
            validation_method()
        except ValidationError as e:
            exceptions.append(e)
    if len(exceptions) > 0:
        raise ValidationError(exceptions)


def custom_exception_handler(exc, context):
    if isinstance(exc, ValidationError):
        if exc.error_list is not None:
            return Response({'error': exc.error_list}, status=400)
        if exc.error_dict is not None:
            return Response({'error': exc.error_dict}, status=400)
        if exc.message is not None:
            return Response({'error': exc.message}, status=400)
    return exception_handler(exc, context)
