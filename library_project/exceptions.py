from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    # Start from DRF default handler
    response = exception_handler(exc, context)

    # If DRF didn't handle it, return generic 500
    if response is None:
        return Response(
            {"status": "error", "message": "An unexpected error occurred."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    data = {"status": "error", "message": str(exc)}
    # Include original details if available
    if isinstance(response.data, dict):
        data["details"] = response.data

    return Response(data, status=response.status_code)