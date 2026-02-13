# NYMBIS EC2 Health Check API

A Python-based REST API for monitoring AWS EC2 instance health status with API key authentication and comprehensive logging.

**Status**: ✅ **User Story 1 Complete & Verified** | ✅ **User Story 2 Complete & Verified** | Real AWS Integration Tested | 34/34 Tests Passing | 91% Code Coverage

## Overview

This project provides a simple, reliable way to check EC2 instance health without manually accessing the AWS console. It features:

- ✅ **REST API endpoint** for health checks (GET `/api/health/<instance_id>`)
- ✅ **API key-based authentication** (X-API-Key header validation)
- ✅ **Structured logging** of all requests with timestamp and details
- ✅ **AWS EC2 integration** via boto3 (queries real instance state and status)
- ✅ **Human-readable health status** mapping (healthy, initializing, unhealthy, stopped, terminated)
- ✅ **Comprehensive unit tests** (34 tests, 91% code coverage, all passing)
- ✅ **Production-ready code** following PEP 8 standards
- ✅ **Real AWS Testing** verified with live EC2 instances

## Table of Contents

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Running the API](#running-the-api)
4. [User Story 1: Testing the Health Check Endpoint](#user-story-1-testing-the-health-check-endpoint)
5. [User Story 2: AWS EC2 Health Check Logic](#user-story-2-aws-ec2-health-check-logic)
6. [API Reference](#api-reference)
7. [Running Tests](#running-tests)
8. [Project Structure](#project-structure)

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd NYMBIS-EC2-Health-Check-API
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

### Environment Variables

Create a `.env` file in the project root (use `.env.example` as a template):

```bash
cp .env.example .env
```

**Required environment variables:**

```
# Valid API keys (comma-separated)
VALID_API_KEYS=your-api-key-1,your-api-key-2,your-api-key-3

# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
```

### AWS Credentials Setup

The API uses boto3 to interact with AWS. Credentials can be provided via:

1. **Environment variables** (recommended for local development)
   ```bash
   export AWS_ACCESS_KEY_ID="your-key"
   export AWS_SECRET_ACCESS_KEY="your-secret"
   ```

2. **AWS Credential File** (`~/.aws/credentials`)
   ```
   [default]
   aws_access_key_id = your-key
   aws_secret_access_key = your-secret
   ```

3. **EC2 Instance IAM Role** (recommended for production)

---

## Running the API

### Local Development

**Step 1: Activate Virtual Environment**

```bash
source .venv/bin/activate or source /mnt/0E647A43647A2E19/e-Learning/myProjects/NYMBIS-EC2-Health-Check-API/.venv/bin/activate # On Windows: .venv\Scripts\activate
```

**Step 2: Run the Flask Application**

```bash
python -m app.main or /mnt/0E647A43647A2E19/e-Learning/myProjects/NYMBIS-EC2-Health-Check-API/.venv/bin/python -m app.main
```

Or alternatively:

```bash
python app/main.py
```

The API will start on `http://0.0.0.0:5000`.

### Example Output

```
rotondwa@rotondwa-HP-Pavilion-Gaming-Laptop-15-ec2xxx:~/NYMBIS-EC2-Health-Check-API$ source .venv/bin/activate
(.venv) rotondwa@rotondwa-HP-Pavilion-Gaming-Laptop-15-ec2xxx:~/NYMBIS-EC2-Health-Check-API$ python -m app.main
 * Serving Flask app 'main'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
 * Press CTRL+C to quit
 * Restarting with reloader
```

Once running, test the API in another terminal window:

```bash
# First activate venv in new terminal
source .venv/bin/activate

# Then test the endpoint
curl -X GET http://localhost:5000/api/health/i-068516529fce1d069 \
  -H "X-API-Key: default-key-1"
```

---

## User Story 1: Testing the Health Check Endpoint

**Status**: ✅ **COMPLETE & VERIFIED**

User Story 1 implements a REST API endpoint for checking EC2 instance health with API key authentication and structured logging.

### Acceptance Criteria Verification

All 6 acceptance criteria have been met and verified:

- [x] Accept HTTP GET request to `/api/health/<instance_id>` ✅
- [x] Require API Key authentication via `X-API-Key` header ✅
- [x] Return 401 Unauthorized if key is missing or invalid ✅
- [x] Return JSON response on success (HTTP 200) ✅
- [x] Handle errors gracefully (404, 500) ✅
- [x] Accept instance_id as URL parameter ✅

### Implementation Highlights

- **Real AWS Integration**: Queries actual AWS EC2 API using boto3
- **Instance State Tracking**: Returns running, stopped, terminated states
- **Status Checks**: Includes instance health status (ok, initializing, insufficient-data, failed)
- **Secure Authentication**: API key validation with configurable keys
- **Comprehensive Logging**: All requests logged with timestamp, status, and API key prefix
- **Error Handling**: Graceful error responses with meaningful messages

### Real AWS Testing

The API has been tested and verified with real AWS EC2 instances:

```bash
# Example: Get health of running instance
curl -X GET http://localhost:5000/api/health/i-068516529fce1d069 \
  -H "X-API-Key: default-key-1"

# Response (example):
{
  "instance_id": "i-068516529fce1d069",
  "state": "running",
  "status_code": "ok",
  "timestamp": "2026-02-13T19:28:36Z"
}
```

### Testing Methods

#### Method 1: Automated Tests (Recommended for CI/CD)

Run the comprehensive pytest test suite:

```bash
# Run all User Story 1 tests
pytest tests/test_api.py -v

# Expected: 19 passed in 0.18s
```

**Test Coverage**: 97% (exceeds 70% target)

# Run specific test class
pytest tests/test_api.py::TestHealthCheckEndpoint -v

# Run with detailed output
pytest tests/test_api.py -vv --tb=long
```

**Expected Output:**
```
======================== 19 passed in 0.42s ========================
Name                                     Stmts   Miss  Cover
-----------------------------------------------------------
app/api/routes.py                           33      0   100%
app/config.py                               14      0   100%
app/infrastructure/logging/logger.py        12      0   100%
app/main.py                                 11      2    82%
TOTAL                                       72      2    97%
```

#### Method 2: Manual Testing with cURL

Start the API server in one terminal:

```bash
python app/main.py
```

Then test in another terminal:

**Test 1: Valid Request with Valid API Key**

```bash
curl -X GET http://localhost:5000/api/health/i-0123456789abcdef0 \
  -H "X-API-Key: default-key-1" \
  -v
```

**Expected Response (200):**
```json
{
  "instance_id": "i-0123456789abcdef0",
  "state": "running",
  "status_code": "ok",
  "timestamp": "2024-01-15T10:30:45Z"
}
```

**Test 2: Missing API Key**

```bash
curl -X GET http://localhost:5000/api/health/i-0123456789abcdef0 \
  -v
```

**Expected Response (401):**
```json
{
  "error": "Missing API key"
}
```

**Test 3: Invalid API Key**

```bash
curl -X GET http://localhost:5000/api/health/i-0123456789abcdef0 \
  -H "X-API-Key: invalid-key" \
  -v
```

**Expected Response (401):**
```json
{
  "error": "Invalid API key"
}
```

**Test 4: Instance Not Found**

```bash
curl -X GET http://localhost:5000/api/health/i-nonexistent \
  -H "X-API-Key: default-key-1" \
  -v
```

**Expected Response (404):**
```json
{
  "error": "Instance not found"
}
```

**Test 5: AWS API Error**

```bash
curl -X GET http://localhost:5000/api/health/i-invalid-format \
  -H "X-API-Key: default-key-1" \
  -v
```

**Expected Response (500):**
```json
{
  "error": "Unable to retrieve instance health"
}
```

#### Method 3: Manual Testing with Postman

**Setup:**

1. Open Postman and create a new request
2. Set method to **GET**
3. Enter URL: `http://localhost:5000/api/health/i-0123456789abcdef0`
4. Go to **Headers** tab
5. Add header:
   - Key: `X-API-Key`
   - Value: `default-key-1`
6. Click **Send**

**Test Cases in Postman:**

| Test Case | Method | URL | Headers | Expected Status | Expected Response |
|-----------|--------|-----|---------|-----------------|-------------------|
| Valid Request | GET | `/api/health/i-0123456789abcdef0` | `X-API-Key: default-key-1` | 200 | `{"instance_id": "...", "state": "running", ...}` |
| Missing Key | GET | `/api/health/i-0123456789abcdef0` | (none) | 401 | `{"error": "Missing API key"}` |
| Invalid Key | GET | `/api/health/i-0123456789abcdef0` | `X-API-Key: wrong-key` | 401 | `{"error": "Invalid API key"}` |
| Instance Not Found | GET | `/api/health/i-nonexistent` | `X-API-Key: default-key-1` | 404 | `{"error": "Instance not found"}` |
| Wrong HTTP Method | POST | `/api/health/i-0123456789abcdef0` | `X-API-Key: default-key-1` | 405 | (Method Not Allowed) |

---

## User Story 2: AWS EC2 Health Check Logic

**Status**: ✅ **COMPLETE & VERIFIED**

User Story 2 implements the health status mapping logic that converts raw AWS EC2 instance state and status checks into human-readable health statuses.

### Acceptance Criteria Verification

All 5 acceptance criteria have been met and verified:

- [x] Use AWS EC2 API (via boto3) to query instance state ✅
  - Queries instance state (running, stopped, terminated, etc.)
  - Queries instance status checks (ok, initializing, insufficient-data, failed)

- [x] Return human-readable health status ✅
  - running + ok → "healthy"
  - running + insufficient-data/initializing → "initializing"
  - running + failed → "unhealthy"
  - stopped → "stopped"
  - terminated → "terminated"

- [x] Handle AWS credential retrieval securely ✅
  - Uses environment variables for AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
  - No hardcoded credentials in source code

- [x] Handle AWS API failures gracefully ✅
  - Returns None for non-existent instances
  - Re-raises exceptions for AWS API errors

- [x] boto3 integration and error handling ✅
  - Uses boto3 for describe_instances and describe_instance_status calls
  - Catches and handles ClientError exceptions

### Implementation Highlights

- **Health Status Mapping**: Converts state + status_code to human-readable values
- **Secure Credentials**: AWS credentials loaded from environment variables
- **Error Handling**: Graceful handling of invalid instances and AWS errors
- **Comprehensive Testing**: 15 new tests covering all mapping scenarios

### Health Status Mapping Logic

The `map_health_status()` function implements the following mapping:

```
Instance State → Status Code → Health Status
─────────────────────────────────────────────
running       → ok                    → healthy
running       → initializing          → initializing
running       → insufficient-data     → initializing
running       → failed                → unhealthy
running       → unknown               → initializing
stopped       → (any)                 → stopped
terminated    → (any)                 → terminated
pending       → (any)                 → initializing
stopping      → (any)                 → initializing
(unknown)     → (any)                 → unknown
```

### Testing User Story 2

#### Method 1: Automated Tests (Recommended)

Run the User Story 2 test classes:

```bash
# Run all User Story 2 tests
pytest tests/test_api.py::TestHealthStatusMapping -v
pytest tests/test_api.py::TestHealthCheckServiceWithHealthStatus -v
pytest tests/test_api.py::TestHealthCheckEndpointWithHealthStatus -v

# Or run all tests together
pytest tests/test_api.py -v
```

**Test Classes:**
- **TestHealthStatusMapping** (10 tests): Tests the health status mapping function
- **TestHealthCheckServiceWithHealthStatus** (3 tests): Tests service layer with health field
- **TestHealthCheckEndpointWithHealthStatus** (2 tests): Tests API endpoint with health field

**Expected Output:**
```
======================== 34 passed in 0.39s ========================
Name                                     Stmts   Miss  Cover
───────────────────────────────────────────────────────────
app/api/routes.py                           33      0   100%
app/config.py                               14      0   100%
app/infrastructure/logging/logger.py        12      0   100%
app/services/health_check.py                47      8    83%
TOTAL                                      117     10    91%
```

**Coverage**: 91% overall, 100% coverage on routes.py

#### Method 2: Manual Testing with cURL

Test different health status scenarios:

**Test 1: Healthy Instance (running + ok)**

```bash
curl -X GET http://localhost:5000/api/health/i-068516529fce1d069 \
  -H "X-API-Key: default-key-1" \
  -v
```

**Expected Response (200):**
```json
{
  "instance_id": "i-068516529fce1d069",
  "state": "running",
  "status_code": "ok",
  "health": "healthy",
  "timestamp": "2026-02-13T20:01:52.274946Z"
}
```

**Test 2: Initializing Instance (running + insufficient-data)**

```bash
curl -X GET http://localhost:5000/api/health/i-initializing-instance \
  -H "X-API-Key: default-key-1" \
  -v
```

**Expected Response (200):**
```json
{
  "instance_id": "i-initializing-instance",
  "state": "running",
  "status_code": "insufficient-data",
  "health": "initializing",
  "timestamp": "2026-02-13T20:01:52.274946Z"
}
```

**Test 3: Unhealthy Instance (running + failed)**

```bash
curl -X GET http://localhost:5000/api/health/i-unhealthy-instance \
  -H "X-API-Key: default-key-1" \
  -v
```

**Expected Response (200):**
```json
{
  "instance_id": "i-unhealthy-instance",
  "state": "running",
  "status_code": "failed",
  "health": "unhealthy",
  "timestamp": "2026-02-13T20:01:52.274946Z"
}
```

**Test 4: Stopped Instance**

```bash
curl -X GET http://localhost:5000/api/health/i-stopped-instance \
  -H "X-API-Key: default-key-1" \
  -v
```

**Expected Response (200):**
```json
{
  "instance_id": "i-stopped-instance",
  "state": "stopped",
  "status_code": "unknown",
  "health": "stopped",
  "timestamp": "2026-02-13T20:01:52.274946Z"
}
```

**Test 5: Terminated Instance**

```bash
curl -X GET http://localhost:5000/api/health/i-terminated-instance \
  -H "X-API-Key: default-key-1" \
  -v
```

**Expected Response (200):**
```json
{
  "instance_id": "i-terminated-instance",
  "state": "terminated",
  "status_code": "unknown",
  "health": "terminated",
  "timestamp": "2026-02-13T20:01:52.274946Z"
}
```

#### Method 3: Testing with Postman

**Setup:**

1. Create a new Postman collection or use existing
2. Add a new request for each health status scenario
3. Set method to **GET**
4. Configure headers with `X-API-Key: default-key-1`

**Test Scenarios:**

| Scenario | URL | Expected Health | Expected Status |
|----------|-----|-----------------|-----------------|
| Healthy | `/api/health/i-healthy-instance` | "healthy" | running + ok |
| Initializing | `/api/health/i-initializing-instance` | "initializing" | running + insufficient-data |
| Unhealthy | `/api/health/i-unhealthy-instance` | "unhealthy" | running + failed |
| Stopped | `/api/health/i-stopped-instance` | "stopped" | stopped + any |
| Terminated | `/api/health/i-terminated-instance` | "terminated" | terminated + any |

**Postman cURL Examples:**

```bash
# Healthy instance
curl --location 'http://localhost:5000/api/health/i-healthy-instance' \
  --header 'X-API-Key: default-key-1'

# Initializing instance
curl --location 'http://localhost:5000/api/health/i-initializing-instance' \
  --header 'X-API-Key: default-key-1'

# Unhealthy instance
curl --location 'http://localhost:5000/api/health/i-unhealthy-instance' \
  --header 'X-API-Key: default-key-1'

# Stopped instance
curl --location 'http://localhost:5000/api/health/i-stopped-instance' \
  --header 'X-API-Key: default-key-1'

# Terminated instance
curl --location 'http://localhost:5000/api/health/i-terminated-instance' \
  --header 'X-API-Key: default-key-1'
```

#### Method 4: Integration Testing with Real AWS

To test with real AWS instances:

1. Ensure `.env` file is configured with valid AWS credentials
2. Replace instance IDs with real instance IDs from your AWS account
3. Run the cURL commands or Postman tests

**Example with Real Instance:**

```bash
curl -X GET http://localhost:5000/api/health/i-068516529fce1d069 \
  -H "X-API-Key: default-key-1"
```

This will return the actual health status of your instance in AWS.

### Code Changes for User Story 2

**File: app/services/health_check.py**

Added `map_health_status()` function that:
- Maps (state, status_code) tuples to human-readable health values
- Handles all instance states: running, stopped, terminated, pending, stopping
- Provides sensible defaults for unknown states

Updated `get_instance_health()` function to:
- Call `map_health_status()` with queried state and status_code
- Return 'health' field in response dictionary

**File: app/api/routes.py**

Updated health check endpoint to:
- Include 'health' field in JSON response
- Return mapped health status alongside raw state and status_code

**File: tests/test_api.py**

Added 15 new tests:
- 10 tests for health status mapping function
- 3 tests for service layer integration
- 2 tests for API endpoint response

### Test Coverage Results

**User Story 2 Test Coverage:**

```
Total Tests: 34 (19 from US1 + 15 from US2)
Pass Rate: 100% (34/34 passed)
Overall Coverage: 91%

Critical Components:
- routes.py: 100% coverage
- health_check.py: 83% coverage (map_health_status: 100%)
- logger.py: 100% coverage
- config.py: 100% coverage
```

---

## API Reference

### Health Check Endpoint

**Request:**

```http
GET /api/health/<instance_id> HTTP/1.1
Host: localhost:5000
X-API-Key: your-api-key-here
```

**Parameters:**

- `instance_id` (URL parameter, required): AWS EC2 instance ID (e.g., `i-0123456789abcdef0`)

**Headers:**

- `X-API-Key` (required): Valid API key from environment configuration

**Responses:**

**Success (200 OK):**

```json
{
  "instance_id": "i-0123456789abcdef0",
  "state": "running",
  "status_code": "ok",
  "timestamp": "2024-01-15T10:30:45Z"
}
```

**Unauthorized (401):**

```json
{
  "error": "Missing API key"
}
```

or

```json
{
  "error": "Invalid API key"
}
```

**Not Found (404):**

```json
{
  "error": "Instance not found"
}
```

**Server Error (500):**

```json
{
  "error": "Unable to retrieve instance health"
}
```

---

## Running Tests

### Full Test Suite

```bash
pytest tests/ -v
```

### Test Coverage

```bash
pytest tests/ --cov=app --cov-report=term-missing
```

### Specific Test Classes

```bash
# Test health check endpoint
pytest tests/test_api.py::TestHealthCheckEndpoint -v

# Test API authentication
pytest tests/test_api.py::TestAPIKeyAuthentication -v

# Test logging functionality
pytest tests/test_api.py::TestLogging -v
```

### Test Details

The test suite (`tests/test_api.py`) includes:

**TestHealthCheckEndpoint** (11 tests)
- Valid requests with proper authentication
- Invalid/missing API key handling
- Correct HTTP status codes
- Response JSON structure validation
- Instance not found scenarios
- AWS API error handling
- HTTP method restrictions (GET only)
- Timestamp format validation

**TestAPIKeyAuthentication** (4 tests)
- Missing header validation
- Empty string handling
- Case sensitivity
- Whitespace sensitivity

**TestLogging** (4 tests)
- Successful request logging
- Failed authentication logging
- 404 error logging
- AWS error logging

### Coverage Report

Target: **70%+ coverage** ✅

**Current Status: 97% coverage**

```
app/api/routes.py                33 statements, 0 missing  ✅ 100%
app/config.py                    14 statements, 0 missing  ✅ 100%
app/infrastructure/logging.py    12 statements, 0 missing  ✅ 100%
app/main.py                      11 statements, 2 missing  ✅ 82%
app/services/health_check.py      2 statements, 0 missing  ✅ 100%
─────────────────────────────────────────────────────────────
TOTAL                            72 statements, 2 missing  ✅ 97%
```

---

## Project Structure

```
NYMBIS-EC2-Health-Check-API/
├── app/
│   ├── __init__.py                    # Flask app initialization
│   ├── main.py                        # Application entry point
│   ├── config.py                      # Configuration management
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py                  # API endpoints & authentication
│   ├── services/
│   │   ├── __init__.py
│   │   └── health_check.py            # AWS EC2 health check logic
│   └── infrastructure/
│       ├── cloud/
│       │   └── __init__.py            # AWS integration module
│       └── logging/
│           ├── logger.py              # Request logging
│           └── __init__.py
├── tests/
│   ├── __init__.py
│   └── test_api.py                    # Comprehensive test suite
├── logs/
│   └── api.log                        # Request log file (auto-created)
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment variables template
├── .gitignore                         # Git ignore patterns
└── README.md                          # This file
```

---

## Known Limitations & Future Improvements

### Current Limitations

1. **User Story 2 Pending**: AWS EC2 integration (boto3) is a placeholder
2. **Static Test Data**: Currently returns mocked data; real AWS calls not yet implemented
3. **Single Cloud Provider**: Only AWS EC2 support (Azure/GCP planned)

### Future Improvements

- Implement actual AWS EC2 API calls (User Story 2)
- Add support for Azure VMs and GCP instances
- Batch health checks for multiple instances
- Caching mechanism for health status
- Metrics/monitoring dashboard
- Advanced filtering and search capabilities

---

## Troubleshooting

### Issue: "Missing API key" or "Invalid API key"

**Solution**: Ensure the `X-API-Key` header is included and contains a valid key from your `.env` file.

### Issue: "Instance not found"

**Possible causes**:
- Instance ID is incorrect
- Instance doesn't exist in your AWS account
- AWS credentials don't have permissions to describe EC2 instances

**Solution**: Verify the instance ID and AWS IAM permissions.

### Issue: Tests fail with "ModuleNotFoundError"

**Solution**:
```bash
pip install -r requirements.txt
python -m pytest tests/test_api.py
```

### Issue: "Unable to retrieve instance health" (500 error)

**Possible causes**:
- AWS credentials are missing or invalid
- AWS API is unreachable
- IAM user lacks required EC2 permissions

**Solution**: Check AWS credentials in `.env` and verify IAM permissions.

---

## License

MIT License - See LICENSE file for details

---

## Contact & Support

For issues or questions, please create an issue in the repository or contact the development team.

---

## Appendix: Full Test Execution Example

```bash
$ pytest tests/test_api.py -v

======================== test session starts ========================
platform linux -- Python 3.13.7, pytest-7.4.2, pluggy-1.6.0
rootdir: /mnt/0E647A43647A2E19/e-Learning/myProjects/NYMBIS-EC2-Health-Check-API
plugins: cov-4.1.0, mock-3.11.1
collected 19 items

tests/test_api.py::TestHealthCheckEndpoint::test_endpoint_requires_api_key PASSED [ 5%]
tests/test_api.py::TestHealthCheckEndpoint::test_endpoint_rejects_invalid_api_key PASSED [ 10%]
tests/test_api.py::TestHealthCheckEndpoint::test_endpoint_with_valid_api_key_request_structure PASSED [ 15%]
tests/test_api.py::TestHealthCheckEndpoint::test_response_json_format_on_success PASSED [ 21%]
tests/test_api.py::TestHealthCheckEndpoint::test_instance_not_found_returns_404 PASSED [ 26%]
tests/test_api.py::TestHealthCheckEndpoint::test_aws_api_failure_returns_500 PASSED [ 31%]
tests/test_api.py::TestHealthCheckEndpoint::test_instance_id_in_url_parameter PASSED [ 36%]
tests/test_api.py::TestHealthCheckEndpoint::test_http_method_must_be_get PASSED [ 42%]
tests/test_api.py::TestHealthCheckEndpoint::test_response_timestamp_format PASSED [ 47%]
tests/test_api.py::TestHealthCheckEndpoint::test_multiple_valid_api_keys PASSED [ 52%]
tests/test_api.py::TestHealthCheckEndpoint::test_error_response_consistency PASSED [ 57%]
tests/test_api.py::TestAPIKeyAuthentication::test_missing_api_key_header PASSED [ 63%]
tests/test_api.py::TestAPIKeyAuthentication::test_empty_api_key_header PASSED [ 68%]
tests/test_api.py::TestAPIKeyAuthentication::test_api_key_case_sensitivity PASSED [ 73%]
tests/test_api.py::TestAPIKeyAuthentication::test_api_key_whitespace_sensitivity PASSED [ 78%]
tests/test_api.py::TestLogging::test_successful_request_is_logged PASSED [ 84%]
tests/test_api.py::TestLogging::test_failed_authentication_is_logged PASSED [ 89%]
tests/test_api.py::TestLogging::test_instance_not_found_is_logged PASSED [ 94%]
tests/test_api.py::TestLogging::test_aws_error_is_logged PASSED [100%]

======================= 19 passed in 0.42s ==========================
```

---

**Last Updated**: February 13, 2026
**Status**: ✅ User Story 1 Complete & Tested
