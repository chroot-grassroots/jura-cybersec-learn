from django.http import JsonResponse
from .models import JuraUser
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit
import json


@csrf_exempt  #  Required for PyScript JSON requests
@ratelimit(
    key="ip", rate="5/m", method="POST", block=True
)  # 5  attempts per minute per IP
@require_http_methods(["POST"])
def login_endpoint(request):
    """
    Authenticate user with zero-knowledge auth hash.

    Expects JSON: {"auth_hash": "64-char-hex-string"}
    Returns: {"status": "success|invalid|invalid_request"}
    Rate limited: 5 attempts per minute per IP.
    """

    # Validate content type
    if request.content_type != "application/json":
        return JsonResponse({"status": "invalid_request"})

    try:
        # Parse JSON data
        data = json.loads(request.body)
        auth_hash = data.get("auth_hash")
    except json.JSONDecodeError:
        return JsonResponse({"status": "invalid_request"})

    # Validate hash format before database query
    if (
        not auth_hash
        or len(auth_hash) != 64
        or not all(c in "0123456789abcdefABCDEF" for c in auth_hash)
    ):
        return JsonResponse({"status": "invalid"})  # Same response as "user not found"

    # Look up user
    user = JuraUser.objects.filter(auth_hash=auth_hash).first()

    if user:
        request.session["auth_hash"] = auth_hash  # Store user identifier
        request.session["authenticated"] = True  # Mark as authenticated
        return JsonResponse({"status": "success"})
    else:
        return JsonResponse(
            {"status": "invalid"}
        )  # Covers "not found", "none", and "malformed"
