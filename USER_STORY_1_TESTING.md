# User Story 1: Testing Guide - Health Check API Endpoint

**Status**: ✅ COMPLETE & TESTED (97% Code Coverage)

---

## Executive Summary

User Story 1 implements a Flask REST API endpoint for checking EC2 instance health with API key authentication. All acceptance criteria are met and covered by 19 comprehensive automated tests.

### Key Metrics

| Metric | Value | Status |
|--------|-------|--------|
| Tests Passed | 19/19 | ✅ PASS |
| Code Coverage | 97% | ✅ EXCEED (Target: 70%) |
| API Key Authentication | Implemented | ✅ PASS |
| HTTP Status Codes | Correct (200, 401, 404, 500) | ✅ PASS |
| Error Handling | Graceful | ✅ PASS |
| Response Format | Valid JSON | ✅ PASS |

---

## Acceptance Criteria Verification

### ✅ Criterion 1: Accept HTTP GET Request to `/api/health/<instance_id>`

**Implementation**: [app/api/routes.py](app/api/routes.py#L50)

```python
@health_bp.route("/api/health/<instance_id>", methods=["GET"])
@check_api_key
def health_check(instance_id):
    """Get health status of an EC2 instance."""
```

**Test Coverage**:
- ✅ `test_endpoint_with_valid_api_key_request_structure`
- ✅ `test_instance_id_in_url_parameter`
- ✅ `test_http_method_must_be_get`

---

### ✅ Criterion 2: Require API Key Authentication

**Implementation**: [app/api/routes.py](app/api/routes.py#L10-L41) - `check_api_key` decorator

**Features**:
- Validates `X-API-Key` header
- Returns 401 if missing
- Returns 401 if invalid
- Logs authentication attempts

**Test Coverage**:
- ✅ `test_endpoint_requires_api_key` - Missing key
- ✅ `test_endpoint_rejects_invalid_api_key` - Invalid key
- ✅ `test_missing_api_key_header`
- ✅ `test_empty_api_key_header`
- ✅ `test_api_key_case_sensitivity`
- ✅ `test_api_key_whitespace_sensitivity`
- ✅ `test_multiple_valid_api_keys`

---

### ✅ Criterion 3: Return 401 Unauthorized if Key Missing/Invalid

**Implementation**: [app/api/routes.py](app/api/routes.py#L27-L41)

```python
if not api_key:
    return jsonify({"error": "Missing API key"}), 401

if api_key not in current_app.config["VALID_API_KEYS"]:
    return jsonify({"error": "Invalid API key"}), 401
```

**Test Results**:
```
tests/test_api.py::TestHealthCheckEndpoint::test_endpoint_requires_api_key PASSED
tests/test_api.py::TestHealthCheckEndpoint::test_endpoint_rejects_invalid_api_key PASSED
tests/test_api.py::TestAPIKeyAuthentication::test_missing_api_key_header PASSED
tests/test_api.py::TestAPIKeyAuthentication::test_empty_api_key_header PASSED
```

---

### ✅ Criterion 4: Return JSON Response on Success (HTTP 200)

**Implementation**: [app/api/routes.py](app/api/routes.py#L73-L85)

**Response Structure**:
```json
{
  "instance_id": "i-0123456789abcdef0",
  "state": "running",
  "status_code": "ok",
  "timestamp": "2024-01-15T10:30:45Z"
}
```

**Test Coverage**:
- ✅ `test_response_json_format_on_success` - All fields present
- ✅ `test_response_timestamp_format` - ISO 8601 format with Z

---

### ✅ Criterion 5: Handle Errors Gracefully

**Error Cases Implemented**:

| Error | Status Code | Response | Test |
|-------|-------------|----------|------|
| Missing API key | 401 | `{"error": "Missing API key"}` | ✅ test_endpoint_requires_api_key |
| Invalid API key | 401 | `{"error": "Invalid API key"}` | ✅ test_endpoint_rejects_invalid_api_key |
| Instance not found | 404 | `{"error": "Instance not found"}` | ✅ test_instance_not_found_returns_404 |
| AWS API failure | 500 | `{"error": "Unable to retrieve instance health"}` | ✅ test_aws_api_failure_returns_500 |

---

### ✅ Criterion 6: Accept instance_id as URL Parameter

**Implementation**: [app/api/routes.py](app/api/routes.py#L50)

```python
@health_bp.route("/api/health/<instance_id>", methods=["GET"])
def health_check(instance_id):
    # instance_id is automatically extracted from URL
```

**Test Evidence**:
```python
def test_instance_id_in_url_parameter(self, client, valid_api_key, mocker):
    instance_id = "i-9876543210fedcba0"
    response = client.get(f"/api/health/{instance_id}", headers=headers)
    assert data["instance_id"] == instance_id
```

✅ PASSED

---

## Test Suite Details

### Test Statistics

```
Total Tests:        19
Passed:            19
Failed:            0
Skipped:           0
Success Rate:      100%

Execution Time:    0.42 seconds
Coverage:          97%
```

### Test Organization

**Class 1: TestHealthCheckEndpoint (11 tests)**

Tests the main endpoint behavior:

1. `test_endpoint_requires_api_key` ✅
   - Verifies 401 status when key missing
   
2. `test_endpoint_rejects_invalid_api_key` ✅
   - Verifies 401 status with invalid key
   
3. `test_endpoint_with_valid_api_key_request_structure` ✅
   - Verifies endpoint accepts valid key
   
4. `test_response_json_format_on_success` ✅
   - Validates response contains: instance_id, state, status_code, timestamp
   
5. `test_instance_not_found_returns_404` ✅
   - Mocks service to return None, expects 404
   
6. `test_aws_api_failure_returns_500` ✅
   - Mocks service to raise exception, expects 500
   
7. `test_instance_id_in_url_parameter` ✅
   - Verifies instance_id correctly captured from URL
   
8. `test_http_method_must_be_get` ✅
   - Verifies POST returns 405 (Method Not Allowed)
   
9. `test_response_timestamp_format` ✅
   - Validates ISO 8601 format with Z suffix
   
10. `test_multiple_valid_api_keys` ✅
    - Tests with multiple valid keys from config
    
11. `test_error_response_consistency` ✅
    - Validates error response structure

**Class 2: TestAPIKeyAuthentication (4 tests)**

Tests authentication edge cases:

1. `test_missing_api_key_header` ✅
   - Missing header returns 401
   
2. `test_empty_api_key_header` ✅
   - Empty string key returns 401
   
3. `test_api_key_case_sensitivity` ✅
   - Uppercase key rejected (case-sensitive)
   
4. `test_api_key_whitespace_sensitivity` ✅
   - Key with whitespace rejected

**Class 3: TestLogging (4 tests)**

Tests logging functionality:

1. `test_successful_request_is_logged` ✅
   - Verifies log_request called on success
   
2. `test_failed_authentication_is_logged` ✅
   - Verifies log_request called on 401
   
3. `test_instance_not_found_is_logged` ✅
   - Verifies log_request called on 404
   
4. `test_aws_error_is_logged` ✅
   - Verifies log_request called on 500

---

## How to Run Tests

### Quick Test (All Tests)

```bash
cd /mnt/0E647A43647A2E19/e-Learning/myProjects/NYMBIS-EC2-Health-Check-API
pytest tests/test_api.py -v
```

**Expected Output**:
```
======================== 19 passed in 0.42s ========================
```

### Test with Coverage Report

```bash
pytest tests/test_api.py --cov=app --cov-report=term
```

**Expected Output**:
```
Name                                     Stmts   Miss  Cover
-----------------------------------------------------------
app/api/routes.py                           33      0   100%
app/config.py                               14      0   100%
app/infrastructure/logging/logger.py        12      0   100%
app/main.py                                 11      2    82%
app/services/health_check.py                 2      0   100%
-----------------------------------------------------------
TOTAL                                       72      2    97%
```

### Test Specific Class

```bash
# Health check endpoint tests
pytest tests/test_api.py::TestHealthCheckEndpoint -v

# Authentication tests
pytest tests/test_api.py::TestAPIKeyAuthentication -v

# Logging tests
pytest tests/test_api.py::TestLogging -v
```

### Test with Verbose Output

```bash
pytest tests/test_api.py -vv --tb=long
```

---

## Manual Testing Guide

### Prerequisites

1. Start the API server:
   ```bash
   python app/main.py
   ```

2. Prepare test tools (choose one):
   - **cURL** (command line)
   - **Postman** (GUI)
   - **HTTPie** (user-friendly CLI)

### Test Case 1: Valid Request

**cURL Command**:
```bash
curl -X GET http://localhost:5000/api/health/i-0123456789abcdef0 \
  -H "X-API-Key: default-key-1" \
  -H "Content-Type: application/json" \
  -v
```

**Expected Response**:
```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "instance_id": "i-0123456789abcdef0",
  "state": "running",
  "status_code": "ok",
  "timestamp": "2024-01-15T10:30:45Z"
}
```

**Postman Steps**:
1. Method: GET
2. URL: `http://localhost:5000/api/health/i-0123456789abcdef0`
3. Headers:
   - Key: `X-API-Key`
   - Value: `default-key-1`
4. Click Send
5. Verify Status: 200 OK
6. Verify Response contains all required fields

---

### Test Case 2: Missing API Key

**cURL Command**:
```bash
curl -X GET http://localhost:5000/api/health/i-0123456789abcdef0 \
  -v
```

**Expected Response**:
```
HTTP/1.1 401 UNAUTHORIZED
Content-Type: application/json

{
  "error": "Missing API key"
}
```

---

### Test Case 3: Invalid API Key

**cURL Command**:
```bash
curl -X GET http://localhost:5000/api/health/i-0123456789abcdef0 \
  -H "X-API-Key: wrong-key-12345" \
  -v
```

**Expected Response**:
```
HTTP/1.1 401 UNAUTHORIZED
Content-Type: application/json

{
  "error": "Invalid API key"
}
```

---

### Test Case 4: Instance Not Found

**cURL Command**:
```bash
curl -X GET http://localhost:5000/api/health/i-nonexistent \
  -H "X-API-Key: default-key-1" \
  -v
```

**Expected Response**:
```
HTTP/1.1 404 NOT FOUND
Content-Type: application/json

{
  "error": "Instance not found"
}
```

---

### Test Case 5: Wrong HTTP Method

**cURL Command** (using POST instead of GET):
```bash
curl -X POST http://localhost:5000/api/health/i-0123456789abcdef0 \
  -H "X-API-Key: default-key-1" \
  -H "Content-Type: application/json" \
  -v
```

**Expected Response**:
```
HTTP/1.1 405 METHOD NOT ALLOWED
```

---

## Postman Collection Setup

### Create Request in Postman

**1. New Request**
- Click "+" or "New" → Request
- Name: "Get EC2 Health"
- Save to a collection

**2. Request Details**
- Method: **GET**
- URL: `{{base_url}}/api/health/i-0123456789abcdef0`
- Headers:
  - Key: `X-API-Key`
  - Value: `{{api_key}}`

**3. Environment Variables** (Postman)
- Click environment dropdown (top right)
- Add new environment "Development"
- Variables:
  ```
  base_url = http://localhost:5000
  api_key = default-key-1
  ```

**4. Run Tests**
- Send request
- Check response in "Response" tab
- Verify status code and JSON

---

## Code Coverage Analysis

### Coverage by Module

| Module | Statements | Covered | Missing | Coverage |
|--------|------------|---------|---------|----------|
| routes.py | 33 | 33 | 0 | **100%** ✅ |
| config.py | 14 | 14 | 0 | **100%** ✅ |
| logger.py | 12 | 12 | 0 | **100%** ✅ |
| health_check.py | 2 | 2 | 0 | **100%** ✅ |
| main.py | 11 | 9 | 2 | **82%** ✅ |
| **TOTAL** | **72** | **70** | **2** | **97%** ✅ |

### What's Covered

✅ All authentication paths (missing, invalid, valid)
✅ All HTTP status codes (200, 401, 404, 500)
✅ Response JSON structure validation
✅ Error message formatting
✅ Logging function calls
✅ URL parameter extraction
✅ HTTP method validation

### What's Not Covered (2 statements)

The 2 uncovered statements in `main.py` are the Flask development server initialization, which is not critical for testing the API logic itself.

---

## Potential Issues & Solutions

### Issue: Test Fails with Import Error

**Cause**: Dependencies not installed

**Solution**:
```bash
pip install -r requirements.txt
pytest tests/test_api.py
```

---

### Issue: API Key Test Fails

**Cause**: Invalid API keys in `.env` or test config

**Solution**:
```bash
# Verify config
grep VALID_API_KEYS .env

# Ensure test config has valid keys
cat app/config.py  # Check TestingConfig.VALID_API_KEYS
```

---

### Issue: Timestamp Format Test Fails

**Cause**: UTC datetime format incorrect

**Solution**: Ensure timestamp ends with "Z" and contains "T":
```python
timestamp = "2024-01-15T10:30:45Z"  # ✅ Correct
timestamp = "2024-01-15 10:30:45"    # ❌ Wrong
```

---

## Compliance Checklist

### Requirements Met

- [x] Endpoint: `/api/health/<instance_id>`
- [x] Method: HTTP GET
- [x] Authentication: X-API-Key header required
- [x] Response: Valid JSON with instance_id, state, status_code, timestamp
- [x] Status 200: Success with full response
- [x] Status 401: Missing or invalid API key
- [x] Status 404: Instance not found
- [x] Status 500: AWS API error
- [x] Error Messages: Meaningful and consistent
- [x] URL Parameters: instance_id extracted from path
- [x] No JSON Body: Only URL parameters and headers

### Testing Requirements Met

- [x] Unit tests written: 19 tests
- [x] Framework: pytest ✅
- [x] Mocking: unittest.mock ✅
- [x] Coverage: 97% (Target: 70%+) ✅
- [x] All tests passing: 19/19 ✅
- [x] Descriptive test names: All tests have clear names ✅
- [x] No real AWS calls: All mocked ✅

---

## Next Steps

### For Development

1. ✅ User Story 1 Complete - API Endpoint & Authentication
2. ⏳ User Story 2 - AWS EC2 Integration (boto3)
3. ⏳ User Story 3 - API Key Management (already done in US1)
4. ⏳ User Story 4 - Structured Logging (already done in US1)
5. ⏳ User Story 5 - Unit Tests (already done in US1)
6. ⏳ User Story 6 - Code Quality & Documentation

### For Production

- [ ] Deploy to AWS Lambda or EC2
- [ ] Set up CI/CD pipeline
- [ ] Configure CloudWatch logging
- [ ] Set up monitoring/alerting
- [ ] Security review and penetration testing

---

## References

- **Flask Documentation**: https://flask.palletsprojects.com/
- **pytest Documentation**: https://docs.pytest.org/
- **AWS boto3**: https://boto3.amazonaws.com/
- **PEP 8 Style Guide**: https://www.python.org/dev/peps/pep-0008/

---

**Document Created**: February 13, 2026
**Last Updated**: February 13, 2026
**Status**: ✅ User Story 1 Complete
