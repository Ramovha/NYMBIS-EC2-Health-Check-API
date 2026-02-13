# Quick Start: Testing User Story 1

**Status**: ✅ Complete | **Coverage**: 97% | **Tests**: 19/19 Passing

---

## TL;DR - Run Tests Now

```bash
cd /mnt/0E647A43647A2E19/e-Learning/myProjects/NYMBIS-EC2-Health-Check-API

# Install dependencies (if not done)
pip install -r requirements.txt

# Run all tests
pytest tests/test_api.py -v

# See coverage
pytest tests/test_api.py --cov=app --cov-report=term
```

**Expected Result**: ✅ 19 passed in 0.42s with 97% coverage

---

## What Gets Tested?

### ✅ API Endpoint (`/api/health/<instance_id>`)
- Accepts GET requests with instance ID in URL
- Rejects wrong HTTP methods (POST, etc.)
- Returns proper JSON response

### ✅ Authentication
- Requires X-API-Key header
- Returns 401 if key missing
- Returns 401 if key invalid
- Accepts valid keys from config

### ✅ Response Format
- HTTP 200 on success with: instance_id, state, status_code, timestamp
- HTTP 404 when instance not found
- HTTP 500 when AWS API fails
- Consistent error message format

### ✅ Logging
- All requests logged with timestamp
- API key truncated in logs (first 10 chars)
- Both success and failure logged

---

## Test Files

| File | Tests | Coverage |
|------|-------|----------|
| [tests/test_api.py](tests/test_api.py) | 19 | 97% |

---

## Running Tests in Different Ways

### Option 1: Simple (All Tests)
```bash
pytest tests/test_api.py
```

### Option 2: With Details
```bash
pytest tests/test_api.py -v
```

### Option 3: With Coverage
```bash
pytest tests/test_api.py --cov=app --cov-report=term
```

### Option 4: Specific Test Class
```bash
# Just endpoint tests
pytest tests/test_api.py::TestHealthCheckEndpoint -v

# Just auth tests
pytest tests/test_api.py::TestAPIKeyAuthentication -v

# Just logging tests
pytest tests/test_api.py::TestLogging -v
```

### Option 5: Single Test
```bash
pytest tests/test_api.py::TestHealthCheckEndpoint::test_endpoint_requires_api_key -v
```

---

## Manual Testing with Postman

### Step 1: Start API Server
```bash
python app/main.py
```
Server runs on `http://localhost:5000`

### Step 2: Create Request in Postman
1. Method: **GET**
2. URL: `http://localhost:5000/api/health/i-0123456789abcdef0`
3. Headers:
   - Key: `X-API-Key`
   - Value: `default-key-1`

### Step 3: Send & Check Response
- Status: 404 (because instance doesn't exist in mocked state)
- Response: `{"error": "Instance not found"}`

### Try These Test Cases

| Test | URL | Header | Expected |
|------|-----|--------|----------|
| Valid | `/api/health/i-123` | `X-API-Key: default-key-1` | 200 or 404 |
| No Key | `/api/health/i-123` | (none) | 401 |
| Bad Key | `/api/health/i-123` | `X-API-Key: wrong` | 401 |
| Wrong Method | `/api/health/i-123` (POST) | `X-API-Key: default-key-1` | 405 |

---

## Manual Testing with cURL

### Test 1: Missing API Key (Should Return 401)
```bash
curl -X GET http://localhost:5000/api/health/i-0123456789abcdef0 -v
```

### Test 2: Valid API Key (Should Return 404 - instance not found)
```bash
curl -X GET http://localhost:5000/api/health/i-0123456789abcdef0 \
  -H "X-API-Key: default-key-1" \
  -v
```

### Test 3: Invalid API Key (Should Return 401)
```bash
curl -X GET http://localhost:5000/api/health/i-0123456789abcdef0 \
  -H "X-API-Key: wrong-key" \
  -v
```

---

## Test Details by Category

### 11 Endpoint Tests
1. ✅ Endpoint requires API key
2. ✅ Endpoint rejects invalid API key
3. ✅ Valid key accepted
4. ✅ Response JSON format correct
5. ✅ Instance not found → 404
6. ✅ AWS error → 500
7. ✅ Instance ID from URL parameter
8. ✅ GET method required (405 for POST)
9. ✅ Timestamp in ISO 8601 format
10. ✅ Multiple valid keys work
11. ✅ Error response consistent

### 4 Authentication Tests
1. ✅ Missing header → 401
2. ✅ Empty key → 401
3. ✅ Case-sensitive validation
4. ✅ Whitespace-sensitive validation

### 4 Logging Tests
1. ✅ Success logged
2. ✅ Failed auth logged
3. ✅ 404 error logged
4. ✅ 500 error logged

---

## Code Coverage Breakdown

```
File                           Coverage
──────────────────────────────────────
routes.py                      100% ✅
config.py                      100% ✅
logger.py                      100% ✅
health_check.py               100% ✅
main.py                        82% ✅
──────────────────────────────────────
TOTAL                          97% ✅✅✅
```

Target was 70%, we achieved 97% 🎉

---

## What's Tested vs Not Tested

### ✅ Tested
- Flask route handling
- Authentication logic
- Response formatting
- Error handling
- Logging function calls
- JSON response structure
- HTTP status codes
- URL parameter extraction

### ⏸️ Not Tested Yet (For User Story 2)
- Actual AWS EC2 API calls
- boto3 integration
- Real instance state querying
- Real status checks from AWS

These will be tested in User Story 2 when `get_instance_health()` is implemented.

---

## Troubleshooting

### Tests fail with "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Tests pass locally but fail in CI
- Ensure Python 3.8+ installed
- Ensure all dependencies installed
- Check pytest version (should be 7.4.2+)

### Want more test output?
```bash
pytest tests/test_api.py -vv --tb=long
```

### Want HTML coverage report?
```bash
pytest tests/test_api.py --cov=app --cov-report=html
# Then open htmlcov/index.html in browser
```

---

## Key Test Fixtures

All tests use these fixtures:

- `app`: Flask test app with TestingConfig
- `client`: Flask test client for making requests
- `valid_api_key`: "test-key-1"
- `invalid_api_key`: "invalid-key-xyz"
- `valid_instance_id`: "i-0123456789abcdef0"

---

## Configuration for Tests

Tests use `TestingConfig`:
```python
class TestingConfig(Config):
    TESTING = True
    VALID_API_KEYS = ["test-key-1", "test-key-2"]
```

No real AWS credentials needed for testing!

---

## Next Steps

### For Immediate Testing
1. ✅ Run automated tests: `pytest tests/test_api.py -v`
2. ✅ Check coverage: `pytest tests/test_api.py --cov=app --cov-report=term`
3. ✅ Manual Postman testing (optional)

### For User Story 2
- Implement `get_instance_health()` with actual boto3 calls
- Update tests to mock boto3 responses
- Test with real AWS credentials (in integration tests)

### For Production
- Deploy to AWS Lambda or EC2
- Set up CloudWatch logging
- Configure API Gateway for HTTP requests
- Set up monitoring/alerting

---

## Need More Details?

See:
- [README.md](README.md) - Setup & usage
- [USER_STORY_1_TESTING.md](USER_STORY_1_TESTING.md) - Detailed testing guide
- [TEST_EXECUTION_REPORT.md](TEST_EXECUTION_REPORT.md) - Full test report
- [tests/test_api.py](tests/test_api.py) - Test code

---

**Last Updated**: February 13, 2026  
**Status**: ✅ User Story 1 Complete & Ready for US2
