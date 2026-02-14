# User Story 5: Unit Tests

**Status**: ✅ **COMPLETE & VERIFIED**

## Overview

User Story 5 implements comprehensive unit tests for all API functionality, authentication, logging, and AWS integration using pytest and mocking to ensure code quality without hitting real AWS infrastructure.

## Acceptance Criteria Verification

All 6 acceptance criteria have been met and verified:

- [x] Test Flask endpoint scenarios ✅
  - Valid request with API key returns 200
  - Missing API key returns 401
  - Invalid API key returns 401
  - Invalid instance_id returns 404

- [x] Test AWS health check logic (using mocks) ✅
  - Mock boto3 running state → "healthy"
  - Mock boto3 stopped state → "stopped"
  - Mock boto3 exception → 500

- [x] Test authentication ✅
  - Valid key accepted
  - Invalid key rejected
  - Missing key rejected

- [x] Test logging ✅
  - Successful requests logged
  - Failed requests logged

- [x] All tests use pytest + mocking ✅
  - Framework: pytest 7.4.2
  - Mocking: unittest.mock + pytest-mock
  - No real AWS calls during testing

- [x] Coverage >= 70% ✅
  - **Current: 91% coverage** (exceeds target)
  - routes.py: 100%
  - logger.py: 100%
  - config.py: 100%
  - health_check.py: 83%

## Test Suite Overview

### Test Structure

```
tests/test_api.py (660+ lines)
├── TestHealthCheckEndpoint (11 tests)
├── TestAPIKeyAuthentication (4 tests)
├── TestLogging (4 tests)
├── TestHealthStatusMapping (10 tests)
├── TestHealthCheckServiceWithHealthStatus (3 tests)
└── TestHealthCheckEndpointWithHealthStatus (2 tests)

Total: 34 tests | 100% pass rate | 91% coverage
```

## Test Details

### 1. TestHealthCheckEndpoint (11 tests)

Tests the Flask endpoint behavior and response formats.

| Test | Scenario | Expected | Status |
|------|----------|----------|--------|
| test_endpoint_requires_api_key | No API key | 401 | ✅ |
| test_endpoint_rejects_invalid_api_key | Invalid key | 401 | ✅ |
| test_endpoint_with_valid_api_key_request_structure | Valid key | 404 (mocked None) | ✅ |
| test_response_json_format_on_success | Valid request | 200 with JSON | ✅ |
| test_instance_not_found_returns_404 | Instance not found | 404 | ✅ |
| test_aws_api_failure_returns_500 | AWS error | 500 | ✅ |
| test_instance_id_in_url_parameter | URL parameter | Accepted | ✅ |
| test_http_method_must_be_get | POST request | 405 | ✅ |
| test_response_timestamp_format | ISO 8601 timestamp | Valid format | ✅ |
| test_multiple_valid_api_keys | Multiple keys | All accepted | ✅ |
| test_error_response_consistency | Error format | Consistent JSON | ✅ |

### 2. TestAPIKeyAuthentication (4 tests)

Tests API key validation and edge cases.

| Test | Scenario | Expected | Status |
|------|----------|----------|--------|
| test_missing_api_key_header | No header | 401 | ✅ |
| test_empty_api_key_header | Empty string | 401 | ✅ |
| test_api_key_case_sensitivity | Uppercase key | 401 (case-sensitive) | ✅ |
| test_api_key_whitespace_sensitivity | Whitespace in key | 401 (exact match) | ✅ |

### 3. TestLogging (4 tests)

Tests request logging functionality.

| Test | Scenario | Expected | Status |
|------|----------|----------|--------|
| test_successful_request_is_logged | 200 response | Logged | ✅ |
| test_failed_authentication_is_logged | 401 response | Logged | ✅ |
| test_instance_not_found_is_logged | 404 response | Logged | ✅ |
| test_aws_error_is_logged | 500 response | Logged | ✅ |

### 4. TestHealthStatusMapping (10 tests)

Tests health status mapping logic from AWS state/status.

| Test | Input | Output | Status |
|------|-------|--------|--------|
| test_healthy_status_running_with_ok | running + ok | healthy | ✅ |
| test_initializing_status_running_with_insufficient_data | running + insufficient-data | initializing | ✅ |
| test_initializing_status_running_with_initializing | running + initializing | initializing | ✅ |
| test_unhealthy_status_running_with_failed | running + failed | unhealthy | ✅ |
| test_stopped_status_when_stopped | stopped + any | stopped | ✅ |
| test_terminated_status_when_terminated | terminated + any | terminated | ✅ |
| test_initializing_status_when_pending | pending + any | initializing | ✅ |
| test_initializing_status_when_stopping | stopping + any | initializing | ✅ |
| test_initializing_status_running_with_unknown | running + unknown | initializing | ✅ |
| test_unknown_status_for_unknown_state | unknown state + any | unknown | ✅ |

### 5. TestHealthCheckServiceWithHealthStatus (3 tests)

Tests health check service with mocked boto3.

| Test | Scenario | Expected | Status |
|------|----------|----------|--------|
| test_get_instance_health_returns_health_field | Mocked boto3 | health field included | ✅ |
| test_get_instance_health_unhealthy_mapping | Failed status | unhealthy | ✅ |
| test_get_instance_health_stopped_mapping | Stopped instance | stopped | ✅ |

### 6. TestHealthCheckEndpointWithHealthStatus (2 tests)

Tests API endpoint health field in response.

| Test | Scenario | Expected | Status |
|------|----------|----------|--------|
| test_endpoint_returns_health_field | Valid request | health field in response | ✅ |
| test_endpoint_returns_unhealthy_status | Unhealthy instance | health: unhealthy | ✅ |

## Running the Tests

### Method 1: Run All Tests

```bash
# Activate virtual environment
source .venv/bin/activate

# Run all tests
pytest tests/test_api.py -v

# Expected output:
# ====================== 34 passed in 0.61s ======================
```

### Method 2: Run Specific Test Class

```bash
# Run endpoint tests only
pytest tests/test_api.py::TestHealthCheckEndpoint -v

# Run authentication tests only
pytest tests/test_api.py::TestAPIKeyAuthentication -v

# Run logging tests only
pytest tests/test_api.py::TestLogging -v

# Run health status mapping tests only
pytest tests/test_api.py::TestHealthStatusMapping -v
```

### Method 3: Run with Coverage Report

```bash
# Full coverage report
pytest tests/test_api.py --cov=app --cov-report=term-missing

# Coverage for specific module
pytest tests/test_api.py --cov=app.api --cov-report=term-missing

# HTML coverage report
pytest tests/test_api.py --cov=app --cov-report=html
# Then open htmlcov/index.html in browser
```

### Method 4: Run with Verbose Output

```bash
# Very verbose output
pytest tests/test_api.py -vv

# Show print statements
pytest tests/test_api.py -v -s

# Show locals on failure
pytest tests/test_api.py -v -l
```

### Method 5: Run Single Test

```bash
# Run one specific test
pytest tests/test_api.py::TestHealthCheckEndpoint::test_endpoint_requires_api_key -v
```

## Test Configuration

### Fixtures

**app fixture** - Creates test Flask application with TestingConfig:
```python
@pytest.fixture
def app():
    app = create_app(TestingConfig)
    return app
```

**client fixture** - Flask test client:
```python
@pytest.fixture
def client(app):
    return app.test_client()
```

**valid_instance_id fixture** - Valid test instance ID:
```python
@pytest.fixture
def valid_instance_id():
    return 'i-0123456789abcdef0'
```

**valid_api_key fixture** - Valid test API key:
```python
@pytest.fixture
def valid_api_key():
    return 'test-key-1'
```

### Mocking Strategy

**Mock boto3 calls** - Prevents real AWS API calls:
```python
mocker.patch('app.services.health_check.boto3.client')
```

**Mock health check function** - Test endpoint behavior:
```python
mocker.patch('app.api.routes.get_instance_health', return_value={...})
```

**Mock logging** - Verify logging calls:
```python
mocker.patch('app.infrastructure.logging.logger.log_request')
```

## Coverage Report

### Overall Coverage

```
Total: 91% coverage (exceeds 70% target)

app/api/routes.py                33 statements, 0 missing  ✅ 100%
app/config.py                    14 statements, 0 missing  ✅ 100%
app/infrastructure/logging/      12 statements, 0 missing  ✅ 100%
app/services/health_check.py     47 statements, 8 missing  ✅ 83%
app/main.py                      11 statements, 2 missing  ✅ 82%
────────────────────────────────────────────────────────────
TOTAL                           117 statements, 10 missing ✅ 91%
```

### Missing Coverage

The 10 missing statements are in:
- `app/services/health_check.py` (8 lines): Exception handling branches for ConnectionError
- `app/main.py` (2 lines): Reloader subprocess initialization

These are low-risk infrastructure code not essential for endpoint testing.

## Test Execution Example

```bash
$ pytest tests/test_api.py -v --cov=app

collected 34 items

tests/test_api.py::TestHealthCheckEndpoint::test_endpoint_requires_api_key PASSED [  2%]
tests/test_api.py::TestHealthCheckEndpoint::test_endpoint_rejects_invalid_api_key PASSED [  5%]
tests/test_api.py::TestHealthCheckEndpoint::test_endpoint_with_valid_api_key_request_structure PASSED [  8%]
tests/test_api.py::TestHealthCheckEndpoint::test_response_json_format_on_success PASSED [ 11%]
tests/test_api.py::TestHealthCheckEndpoint::test_instance_not_found_returns_404 PASSED [ 14%]
tests/test_api.py::TestHealthCheckEndpoint::test_aws_api_failure_returns_500 PASSED [ 17%]
tests/test_api.py::TestHealthCheckEndpoint::test_instance_id_in_url_parameter PASSED [ 20%]
tests/test_api.py::TestHealthCheckEndpoint::test_http_method_must_be_get PASSED [ 23%]
tests/test_api.py::TestHealthCheckEndpoint::test_response_timestamp_format PASSED [ 26%]
tests/test_api.py::TestHealthCheckEndpoint::test_multiple_valid_api_keys PASSED [ 29%]
tests/test_api.py::TestHealthCheckEndpoint::test_error_response_consistency PASSED [ 32%]
tests/test_api.py::TestAPIKeyAuthentication::test_missing_api_key_header PASSED [ 35%]
tests/test_api.py::TestAPIKeyAuthentication::test_empty_api_key_header PASSED [ 38%]
tests/test_api.py::TestAPIKeyAuthentication::test_api_key_case_sensitivity PASSED [ 41%]
tests/test_api.py::TestAPIKeyAuthentication::test_api_key_whitespace_sensitivity PASSED [ 44%]
tests/test_api.py::TestLogging::test_successful_request_is_logged PASSED [ 47%]
tests/test_api.py::TestLogging::test_failed_authentication_is_logged PASSED [ 50%]
tests/test_api.py::TestLogging::test_instance_not_found_is_logged PASSED [ 52%]
tests/test_api.py::TestLogging::test_aws_error_is_logged PASSED [ 55%]
tests/test_api.py::TestHealthStatusMapping::test_healthy_status_running_with_ok PASSED [ 58%]
... (remaining 14 tests) ...

====================== 34 passed, 25 warnings in 0.61s ======================

---------- coverage: platform linux, python 3.13.7-final-0 -----------
Name                                     Stmts   Miss  Cover
----------------------------------------------------------------------
app/api/routes.py                           33      0   100%
app/config.py                               14      0   100%
app/infrastructure/logging/logger.py        12      0   100%
app/main.py                                 11      2    82%
app/services/health_check.py                47      8    83%
----------------------------------------------------------------------
TOTAL                                      117     10    91%
```

## Troubleshooting Tests

### Tests hang or timeout

```bash
# Run with timeout
pytest tests/test_api.py --timeout=10 -v
```

### Import errors

```bash
# Ensure virtual environment activated
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Missing pytest plugins

```bash
# Install test dependencies
pip install pytest pytest-cov pytest-mock
```

### Test collection errors

```bash
# Debug test collection
pytest tests/test_api.py --collect-only
```

## Best Practices Implemented

✅ **Descriptive test names** - Each test name explains what it tests
✅ **Isolated tests** - No test depends on another
✅ **Mocked external calls** - No real AWS calls during testing
✅ **Fixtures for reuse** - DRY principle applied
✅ **Clear assertions** - Easy to understand what's being tested
✅ **Coverage measurement** - Automated with pytest-cov
✅ **Fast execution** - All 34 tests run in ~0.6 seconds

## Related Documentation

- [Main README](README.md) - Project overview
- [User Story 4: Logging](USER_STORY_4_LOGGING.md) - Logging documentation
- [tests/test_api.py](tests/test_api.py) - Complete test implementation

## Summary

User Story 5 provides comprehensive test coverage:
- ✅ 34 unit tests covering all scenarios
- ✅ 100% pass rate
- ✅ 91% code coverage (exceeds 70% target)
- ✅ Uses pytest + pytest-mock for mocking
- ✅ No real AWS calls during testing
- ✅ Fast execution (~0.6 seconds)
- ✅ Clear, descriptive test names
- ✅ Isolated, reusable test fixtures
