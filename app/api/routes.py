"""API routes for health check endpoints."""
from flask import Blueprint, request, jsonify
from datetime import datetime
from app.services.health_check import get_instance_health
from app.infrastructure.logging.logger import log_request

health_bp = Blueprint("health", __name__, url_prefix="/api")


def check_api_key(f):
    """Decorator to validate API key in request header.

    Checks if the X-API-Key header is present and valid.
    Returns 401 Unauthorized if missing or invalid.
    """
    def decorated_function(*args, **kwargs):
        from flask import current_app

        api_key = request.headers.get("X-API-Key")

        if not api_key:
            log_request(
                method=request.method,
                path=request.path,
                api_key="",
                status_code=401,
                result="Missing API key",
            )
            return jsonify({"error": "Missing API key"}), 401

        if api_key not in current_app.config["VALID_API_KEYS"]:
            log_request(
                method=request.method,
                path=request.path,
                api_key=api_key,
                status_code=401,
                result="Invalid API key",
            )
            return jsonify({"error": "Invalid API key"}), 401

        return f(*args, **kwargs)

    decorated_function.__name__ = f.__name__
    return decorated_function


@health_bp.route("/health/<instance_id>", methods=["GET"])
@check_api_key
def health_check(instance_id):
    """Get health status of an EC2 instance.

    Args:
        instance_id (str): AWS EC2 instance ID (e.g., i-0123456789abcdef0)

    Returns:
        JSON response with instance health status

    Status Codes:
        200: Instance health retrieved successfully
        401: Missing or invalid API key
        404: Instance not found
        500: AWS API error
    """
    api_key = request.headers.get("X-API-Key")

    try:
        health_status = get_instance_health(instance_id)

        if health_status is None:
            log_request(
                method=request.method,
                path=request.path,
                api_key=api_key,
                status_code=404,
                result="Instance not found",
            )
            return jsonify({"error": "Instance not found"}), 404

        response = {
            "instance_id": instance_id,
            "state": health_status.get("state"),
            "status_code": health_status.get("status_code"),
            "health": health_status.get("health"),
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

        log_request(
            method=request.method,
            path=request.path,
            api_key=api_key,
            status_code=200,
            result=health_status.get("status_code"),
        )

        return jsonify(response), 200

    except Exception as e:
        log_request(
            method=request.method,
            path=request.path,
            api_key=api_key,
            status_code=500,
            result=f"AWS API error: {str(e)}",
        )
        return (
            jsonify({"error": "Unable to retrieve instance health"}),
            500,
        )
