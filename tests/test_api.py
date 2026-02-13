"""Test module for Health Check API endpoints."""
import pytest
import json
from app.main import create_app
from app.config import TestingConfig


@pytest.fixture
def app():
    """Create and configure a test Flask application."""
    app = create_app(TestingConfig)
    return app


@pytest.fixture
def client(app):
    """Create a test client for the Flask application."""
    return app.test_client()


@pytest.fixture
def valid_api_key():
    """Return a valid test API key."""
    return "test-key-1"


@pytest.fixture
def invalid_api_key():
    """Return an invalid test API key."""
    return "invalid-key-xyz"


@pytest.fixture
def valid_instance_id():
    """Return a valid test instance ID."""
    return "i-0123456789abcdef0"


class TestHealthCheckEndpoint:
    """Test suite for the /api/health/<instance_id> endpoint."""

    def test_endpoint_requires_api_key(self, client, valid_instance_id):
        """Test that the endpoint returns 401 when API key is missing."""
        response = client.get(f"/api/health/{valid_instance_id}")
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert "error" in data
        assert data["error"] == "Missing API key"

    def test_endpoint_rejects_invalid_api_key(
        self, client, valid_instance_id, invalid_api_key
    ):
        """Test that the endpoint returns 401 with an invalid API key."""
        headers = {"X-API-Key": invalid_api_key}
        response = client.get(f"/api/health/{valid_instance_id}", headers=headers)
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert "error" in data
        assert data["error"] == "Invalid API key"

    def test_endpoint_with_valid_api_key_request_structure(
        self, client, valid_instance_id, valid_api_key, mocker
    ):
        """Test that endpoint accepts request with valid API key and returns proper structure."""
        # Mock the health check to return None (instance not found)
        mocker.patch(
            "app.api.routes.get_instance_health",
            return_value=None
        )
        
        headers = {"X-API-Key": valid_api_key}
        response = client.get(f"/api/health/{valid_instance_id}", headers=headers)
        
        # When instance not found, should return 404
        assert response.status_code == 404
        data = json.loads(response.data)
        assert "error" in data

    def test_response_json_format_on_success(
        self, client, valid_api_key, mocker
    ):
        """Test that successful response has correct JSON structure."""
        mock_health = {
            "state": "running",
            "status_code": "ok"
        }
        mocker.patch(
            "app.api.routes.get_instance_health",
            return_value=mock_health
        )
        
        instance_id = "i-0123456789abcdef0"
        headers = {"X-API-Key": valid_api_key}
        response = client.get(f"/api/health/{instance_id}", headers=headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Verify response structure
        assert "instance_id" in data
        assert "state" in data
        assert "status_code" in data
        assert "timestamp" in data
        
        # Verify values
        assert data["instance_id"] == instance_id
        assert data["state"] == "running"
        assert data["status_code"] == "ok"

    def test_instance_not_found_returns_404(
        self, client, valid_api_key, mocker
    ):
        """Test that invalid instance ID returns 404."""
        mocker.patch(
            "app.api.routes.get_instance_health",
            return_value=None
        )
        
        invalid_id = "i-nonexistent"
        headers = {"X-API-Key": valid_api_key}
        response = client.get(f"/api/health/{invalid_id}", headers=headers)
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data["error"] == "Instance not found"

    def test_aws_api_failure_returns_500(
        self, client, valid_api_key, mocker
    ):
        """Test that AWS API errors return 500."""
        mocker.patch(
            "app.api.routes.get_instance_health",
            side_effect=Exception("AWS API Error: AccessDenied")
        )
        
        instance_id = "i-0123456789abcdef0"
        headers = {"X-API-Key": valid_api_key}
        response = client.get(f"/api/health/{instance_id}", headers=headers)
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert "error" in data
        assert data["error"] == "Unable to retrieve instance health"

    def test_instance_id_in_url_parameter(
        self, client, valid_api_key, mocker
    ):
        """Test that instance_id is accepted as URL parameter, not JSON body."""
        mock_health = {
            "state": "running",
            "status_code": "ok"
        }
        mocker.patch(
            "app.api.routes.get_instance_health",
            return_value=mock_health
        )
        
        # Test with URL parameter
        instance_id = "i-9876543210fedcba0"
        headers = {"X-API-Key": valid_api_key}
        response = client.get(f"/api/health/{instance_id}", headers=headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["instance_id"] == instance_id

    def test_http_method_must_be_get(
        self, client, valid_api_key, valid_instance_id
    ):
        """Test that only GET requests are allowed."""
        headers = {"X-API-Key": valid_api_key}
        
        # POST should not be allowed
        response = client.post(f"/api/health/{valid_instance_id}", headers=headers)
        assert response.status_code == 405  # Method Not Allowed

    def test_response_timestamp_format(
        self, client, valid_api_key, mocker
    ):
        """Test that timestamp in response is ISO 8601 format with Z suffix."""
        mock_health = {
            "state": "running",
            "status_code": "ok"
        }
        mocker.patch(
            "app.api.routes.get_instance_health",
            return_value=mock_health
        )
        
        instance_id = "i-0123456789abcdef0"
        headers = {"X-API-Key": valid_api_key}
        response = client.get(f"/api/health/{instance_id}", headers=headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Verify timestamp format (ISO 8601 with Z)
        timestamp = data["timestamp"]
        assert timestamp.endswith("Z")
        assert "T" in timestamp  # Should have ISO 8601 format
        # Verify it's parseable as ISO format
        assert len(timestamp) > 15  # At least YYYY-MM-DDTHH:MM:SSZ

    def test_multiple_valid_api_keys(
        self, client, valid_instance_id, mocker
    ):
        """Test that endpoint works with different valid API keys."""
        mock_health = {
            "state": "running",
            "status_code": "ok"
        }
        mocker.patch(
            "app.api.routes.get_instance_health",
            return_value=mock_health
        )
        
        # Test with first valid key
        headers = {"X-API-Key": "test-key-1"}
        response = client.get(f"/api/health/{valid_instance_id}", headers=headers)
        assert response.status_code == 200
        
        # Test with second valid key
        headers = {"X-API-Key": "test-key-2"}
        response = client.get(f"/api/health/{valid_instance_id}", headers=headers)
        assert response.status_code == 200

    def test_error_response_consistency(
        self, client, valid_instance_id, invalid_api_key
    ):
        """Test that error responses follow consistent structure."""
        headers = {"X-API-Key": invalid_api_key}
        response = client.get(f"/api/health/{valid_instance_id}", headers=headers)
        
        assert response.status_code == 401
        data = json.loads(response.data)
        
        # Should only have "error" key in error response
        assert len(data) == 1
        assert "error" in data


class TestAPIKeyAuthentication:
    """Test suite for API key authentication decorator."""

    def test_missing_api_key_header(self, client, valid_instance_id):
        """Test behavior when X-API-Key header is completely missing."""
        response = client.get(f"/api/health/{valid_instance_id}")
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data["error"] == "Missing API key"

    def test_empty_api_key_header(self, client, valid_instance_id):
        """Test behavior when X-API-Key header is empty string."""
        headers = {"X-API-Key": ""}
        response = client.get(f"/api/health/{valid_instance_id}", headers=headers)
        
        assert response.status_code == 401

    def test_api_key_case_sensitivity(
        self, client, valid_instance_id, mocker
    ):
        """Test that API key validation is case-sensitive."""
        mock_health = {
            "state": "running",
            "status_code": "ok"
        }
        mocker.patch(
            "app.api.routes.get_instance_health",
            return_value=mock_health
        )
        
        # Valid key in uppercase should fail
        headers = {"X-API-Key": "TEST-KEY-1"}
        response = client.get(f"/api/health/{valid_instance_id}", headers=headers)
        
        assert response.status_code == 401

    def test_api_key_whitespace_sensitivity(
        self, client, valid_instance_id
    ):
        """Test that API key with whitespace is rejected."""
        headers = {"X-API-Key": " test-key-1"}  # Extra space
        response = client.get(f"/api/health/{valid_instance_id}", headers=headers)
        
        assert response.status_code == 401


class TestLogging:
    """Test suite for request logging functionality."""

    def test_successful_request_is_logged(
        self, client, valid_api_key, mocker, tmp_path
    ):
        """Test that successful requests are logged."""
        # Mock the log_request function to verify it's called
        log_mock = mocker.patch("app.api.routes.log_request")
        
        mock_health = {
            "state": "running",
            "status_code": "ok"
        }
        mocker.patch(
            "app.api.routes.get_instance_health",
            return_value=mock_health
        )
        
        instance_id = "i-0123456789abcdef0"
        headers = {"X-API-Key": valid_api_key}
        response = client.get(f"/api/health/{instance_id}", headers=headers)
        
        assert response.status_code == 200
        
        # Verify log_request was called
        assert log_mock.called
        call_args = log_mock.call_args
        
        # Verify logged parameters
        assert call_args.kwargs["method"] == "GET"
        assert call_args.kwargs["path"] == f"/api/health/{instance_id}"
        assert call_args.kwargs["status_code"] == 200
        assert call_args.kwargs["api_key"] == valid_api_key

    def test_failed_authentication_is_logged(
        self, client, valid_instance_id, invalid_api_key, mocker
    ):
        """Test that failed authentication attempts are logged."""
        log_mock = mocker.patch("app.api.routes.log_request")
        
        headers = {"X-API-Key": invalid_api_key}
        response = client.get(f"/api/health/{valid_instance_id}", headers=headers)
        
        assert response.status_code == 401
        
        # Verify log_request was called
        assert log_mock.called
        call_args = log_mock.call_args
        
        assert call_args.kwargs["status_code"] == 401
        assert call_args.kwargs["result"] == "Invalid API key"

    def test_instance_not_found_is_logged(
        self, client, valid_api_key, mocker
    ):
        """Test that 404 errors are logged."""
        log_mock = mocker.patch("app.api.routes.log_request")
        
        mocker.patch(
            "app.api.routes.get_instance_health",
            return_value=None
        )
        
        instance_id = "i-nonexistent"
        headers = {"X-API-Key": valid_api_key}
        response = client.get(f"/api/health/{instance_id}", headers=headers)
        
        assert response.status_code == 404
        
        # Verify log_request was called with 404 status
        assert log_mock.called
        call_args = log_mock.call_args
        assert call_args.kwargs["status_code"] == 404
        assert "Instance not found" in call_args.kwargs["result"]

    def test_aws_error_is_logged(
        self, client, valid_api_key, mocker
    ):
        """Test that AWS API errors are logged."""
        log_mock = mocker.patch("app.api.routes.log_request")
        
        mocker.patch(
            "app.api.routes.get_instance_health",
            side_effect=Exception("AWS API Error")
        )
        
        instance_id = "i-0123456789abcdef0"
        headers = {"X-API-Key": valid_api_key}
        response = client.get(f"/api/health/{instance_id}", headers=headers)
        
        assert response.status_code == 500
        
        # Verify log_request was called with 500 status
        assert log_mock.called
        call_args = log_mock.call_args
        assert call_args.kwargs["status_code"] == 500
