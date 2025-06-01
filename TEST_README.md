# Walver SDK Client Test Suite

This directory contains comprehensive tests for both the AsyncWalver (async) and Walver (sync) clients.

## 🧪 Test Files

- **`test_complete_async.py`** - Complete test suite for AsyncWalver (asynchronous client)
- **`test_complete_sync.py`** - Complete test suite for Walver (synchronous client)
- **`run_tests.py`** - Test runner script with options for both clients

## 🚀 Quick Start

### 1. Setup Environment

Create a `.env` file with your API key:

```bash
# Required: Your Walver API key
WALVER_API_KEY=your_api_key_here

# Optional: Base URL (default: https://walver.io/)
WALVER_BASE_URL=http://localhost:8000

# Optional: Request timeout in seconds (default: 10)
WALVER_TIMEOUT=30
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Tests

```bash
# Run all tests for both clients
python run_tests.py all

# Run tests for specific client type
python run_tests.py all --client-type async    # Async client only
python run_tests.py all --client-type sync     # Sync client only
python run_tests.py all --client-type both     # Both clients (default)

# Run specific test categories
python run_tests.py init         # Client initialization tests
python run_tests.py folders      # Folder operation tests (not implemented yet)
python run_tests.py api-keys     # API key tests (not implemented yet) 
python run_tests.py verifications # Verification tests (not implemented yet)

# Run individual test files directly
python test_complete.py          # Async tests only
python test_complete_sync.py     # Sync tests only
```

## 📋 Test Coverage

Both async and sync test suites provide identical coverage:

### 🔧 Client Initialization Tests
- ✅ Initialize client with API key from environment
- ✅ Initialize client with explicit API key
- ✅ Error handling for missing API key
- ✅ Custom base URL and timeout settings

### 📁 Folder Operations Tests
- ✅ **Create Folder** - With and without custom fields
- ✅ **Get All Folders** - Retrieve list of all folders
- ✅ **Get Specific Folder** - Retrieve folder by ID
- ✅ **Get Folder Verifications** - List verifications in a folder
- ✅ **Delete Folder** - Remove folder and cleanup

### 🔑 API Key Operations Tests
- ✅ **Create API Key** - With and without description
- ✅ **Get All API Keys** - Retrieve list of all API keys
- ✅ **Delete API Key** - Remove API key

### 🔗 Verification Operations Tests

#### Basic Verifications
- ✅ **Basic Verification** - Simple wallet verification
- ✅ **Folder Verification** - Verification with folder and custom fields
- ✅ **Webhook Integration** - With webhook URL and secret

#### Social Verifications
- ✅ **Email Verification** - Force email verification
- ✅ **Telephone Verification** - Force phone verification  
- ✅ **Telegram Verification** - Force Telegram verification
- ✅ **Twitter Verification** - Force Twitter verification
- ✅ **All Social Verifications** - Combined social verification

#### Token Gating
- ✅ **Token Gate** - Require specific token amount
- ✅ **NFT Gate** - Require NFT ownership
- ✅ **One-time Verification** - Single-use verification

#### Advanced Features
- ✅ **Custom Fields** - All field types (email, telephone, telegram, twitter, text)
- ✅ **Expiration Dates** - Time-limited verifications
- ✅ **Redirect URLs** - Post-verification redirects
- ✅ **Multiple Chains** - Solana, Ethereum, Polygon support

### 🚨 Error Handling Tests
- ✅ **Duplicate Verification ID** - Proper error for existing ID
- ✅ **Invalid Token Gate** - Missing token address/amount
- ✅ **Invalid Social Verification** - Missing required custom fields
- ✅ **Network Errors** - HTTP error handling
- ✅ **Validation Errors** - Parameter validation

### 🧹 Cleanup Tests
- ✅ **Resource Cleanup** - Automatic cleanup of test resources
- ✅ **Error Recovery** - Cleanup even if tests fail

## 📊 Test Output

The test suite provides colorful, detailed output showing:

- 🧪 **Test Progress** - Which test is currently running
- ✅ **Success Messages** - What succeeded
- ❌ **Error Messages** - What failed and why
- ℹ️ **Information** - Additional details about created resources
- ⚠️ **Warnings** - Non-critical issues during cleanup

Example output for both clients:
```
🧪 WALVER SDK ASYNC CLIENT COMPREHENSIVE TEST SUITE
======================================================================

🧪 🔧 Testing Client Initialization
✅ Correctly caught missing API key error: API key is required...
✅ Client initialized with explicit API key

==================================================
🔄 RUNNING SYNCHRONOUS CLIENT TESTS
==================================================

🧪 WALVER SDK SYNC CLIENT COMPREHENSIVE TEST SUITE
======================================================================

🧪 🔧 Testing Client Initialization (Synchronous)
✅ Correctly caught missing API key error: API key is required...
...
```

## 🔄 Test Resources

Each test suite creates and cleans up:

### Created Resources
- **2 Test Folders** (with different configurations)
- **2 Test API Keys** (with and without descriptions) 
- **7+ Test Verifications** (covering all verification types)

### Resource Separation
- **Async tests** create resources with standard names
- **Sync tests** create resources with "(Sync)" suffix and "sync" in IDs
- This prevents conflicts when running both test suites

### Automatic Cleanup
All created resources are automatically deleted at the end of each test, even if errors occur.

## 🔀 Client Differences

### AsyncWalver (Asynchronous Client)
- Uses `httpx` for HTTP requests
- All methods are `async` and require `await`
- Better for high-concurrency applications
- Requires `asyncio.run()` or async context

### Walver (Synchronous Client)  
- Uses `requests` for HTTP requests
- All methods are synchronous (blocking)
- Simpler to use in regular Python scripts
- Direct function calls (no `await` needed)

### Usage Examples

**Async Client:**
```python
import asyncio
from walver_sdk.async_client import AsyncWalver

async def main():
    walver = AsyncWalver(api_key="your-key")
    folders = await walver.get_folders()
    return folders

result = asyncio.run(main())
```

**Sync Client:**
```python
from walver_sdk.client import Walver

walver = Walver(api_key="your-key")
folders = walver.get_folders()
```

## 🐛 Troubleshooting

### Common Issues

1. **Missing API Key**
   ```
   ValueError: API key is required...
   ```
   Solution: Add `WALVER_API_KEY=your_key` to your `.env` file

2. **Connection Errors**
   ```
   httpx.ConnectError: [Errno 61] Connection refused (async)
   requests.ConnectionError: [Errno 61] Connection refused (sync)
   ```
   Solution: Make sure your Walver server is running on the specified URL

3. **Permission Errors**
   ```
   httpx.HTTPStatusError: 403 Forbidden (async)
   requests.HTTPError: 403 Forbidden (sync)
   ```
   Solution: Verify your API key has the required permissions

4. **Duplicate ID Errors**
   ```
   ValueError: ID for the verification already exists
   ```
   Solution: This is expected behavior for the duplicate ID test

### Client-Specific Issues

**Async Client:**
- Make sure to use `await` with all client methods
- Run tests with `asyncio.run()` or in async context
- Import from `walver_sdk.async_client`

**Sync Client:**
- No `await` needed - direct function calls
- Can run directly in regular Python scripts
- Import from `walver_sdk.client`

### Debug Mode

For more detailed debugging, you can modify the test files to add additional logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Extending Tests

To add new tests to both clients:

1. **Add test function** to both `test_complete.py` and `test_complete_sync.py`
2. **Follow naming convention** `test_XX_description` 
3. **Add to cleanup** if creating resources
4. **Update this README** with test description
5. **Keep async/sync versions identical** except for `async`/`await` keywords

Example:
```python
# Async version (test_complete.py)
async def test_new_feature():
    result = await walver.new_method()
    print_success(f"New feature works: {result}")

# Sync version (test_complete_sync.py)  
def test_new_feature():
    result = walver.new_method()
    print_success(f"New feature works: {result}")
```

## 📝 Test Data

The tests use realistic test data:

- **Folder Names**: "Test Folder 1", "Simple Test Folder" (+ "(Sync)" for sync tests)
- **Service Names**: "Test Service Basic", "Test Email Verification Service" (+ "(Sync)" for sync tests)
- **Verification IDs**: "test-basic-verification-001", "test-basic-verification-sync-001" 
- **Token Addresses**: Real format addresses for Solana/Ethereum
- **Webhooks**: "https://webhook.example.com/..." 

This ensures tests are realistic while being clearly identifiable as test data and prevents conflicts between async/sync test runs. 