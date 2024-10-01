from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from adrf.decorators import api_view


@api_view(["GET"])
async def health_check(request: Request) -> Response:
    """
    Checks the health of the API.

    Args:
        request (Request): The incoming HTTP request.

    Returns:
        Response: A JSON response containing the status of the API, with a status code of 200.
    """
    return Response({"status": "OK"}, status=status.HTTP_200_OK)
