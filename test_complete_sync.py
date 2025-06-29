from walver_sdk.client import Walver
from walver_sdk.models import CustomField
import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

test_id = int(time.time())

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_test(message, color=Colors.CYAN):
    print(f"{color}{Colors.BOLD}🧪 {message}{Colors.RESET}")

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.RESET}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.RESET}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.RESET}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.RESET}")

def test_walver_client():
    """Comprehensive test of the Walver client"""
    
    print_test("🚀 Starting Walver Client Comprehensive Test (Synchronous)")
    print_info(f"Base URL: https://walver.io")
    
    # Initialize client
    try:
        walver = Walver(
            api_key=os.getenv("WALVER_API_KEY"),
            base_url="https://walver.io"
        )
        print_success("Walver client initialized successfully")
    except Exception as e:
        print_error(f"Failed to initialize client: {e}")
        return
    
    # Variables to store created resources for cleanup
    created_folder_ids = []
    created_api_key_ids = []
    created_verification_ids = []
    
    try:
        # =================================================================
        # FOLDER OPERATIONS TESTS
        # =================================================================
        print_test("📁 Testing Folder Operations")
        
        # Test 1: Create folders
        print_test("1️⃣ Creating test folders")
        
        # Create folder with custom fields
        custom_fields = [
            CustomField(
                id="field_1745675962846_279",
                name="Email Address",
                type="email",
                required=True,
                placeholder="Enter Email Address"
            ),
            CustomField(
                id="field_1745675979014_280",
                name="Phone Number", 
                type="telephone",
                required=True,
                placeholder="Enter Phone Number"
            ),
            CustomField(
                id="field_1745675995182_281",
                name="Telegram Username",
                type="telegram", 
                required=True,
                placeholder="Enter Telegram Username"
            ),
            CustomField(
                id="field_1745675995182_284",
                name="Discord Username",
                type="discord", 
                required=True,
                placeholder="Enter Discord Username"
            ),
            CustomField(
                id="field_1745676011350_282",
                name="Twitter Handle",
                type="twitter",
                required=True, 
                placeholder="Enter Twitter Handle"
            ),
            CustomField(
                id="field_1745676027518_283",
                name="Full Name",
                type="text",
                required=True,
                placeholder="Enter Full Name"
            )
        ]
        
        folder1 = walver.create_folder(
            name="Test Folder 1 (Sync)",
            description="A comprehensive test folder with all field types (sync)",
            custom_fields=custom_fields
        )
        created_folder_ids.append(folder1.id)
        print_success(f"Created folder 1: {folder1.name} (ID: {folder1.id})")
        
        # Create simple folder
        folder2 = walver.create_folder(
            name="Simple Test Folder (Sync)",
            description="A simple test folder (sync)"
        )
        created_folder_ids.append(folder2.id)
        print_success(f"Created folder 2: {folder2.name} (ID: {folder2.id})")
        
        # Test 2: Get all folders
        print_test("2️⃣ Getting all folders")
        folders = walver.get_folders()
        print_success(f"Retrieved {len(folders)} folders")
        for folder in folders[-2:]:  # Show last 2 folders (our test folders)
            print_info(f"  - {folder.name}: {folder.description}")
        
        # Test 3: Get specific folder
        print_test("3️⃣ Getting specific folder")
        retrieved_folder = walver.get_folder(folder1.id)
        print_success(f"Retrieved folder: {retrieved_folder.name}")
        print_info(f"  Custom fields: {len(retrieved_folder.custom_fields)}")
        for field in retrieved_folder.custom_fields:
            print_info(f"    - {field.name} ({field.type}) - Required: {field.required}")
        
        # Test 4: Get folder verifications (should be empty)
        print_test("4️⃣ Getting folder verifications")
        verifications = walver.get_folder_verifications(folder1.id)
        print_success(f"Retrieved {len(verifications)} verifications for folder")
        
        # =================================================================
        # API KEY OPERATIONS TESTS
        # =================================================================
        print_test("🔑 Testing API Key Operations")
        
        # Test 5: Create API keys
        print_test("5️⃣ Creating test API keys")
        
        api_key1 = walver.create_api_key(
            name="Test API Key 1 (Sync)",
            description="A test API key for comprehensive testing (sync)"
        )
        created_api_key_ids.append(api_key1.id)
        print_success(f"Created API key 1: {api_key1.name} (ID: {api_key1.id})")
        
        api_key2 = walver.create_api_key(
            name="Test API Key 2 (Sync)"
        )
        created_api_key_ids.append(api_key2.id) 
        print_success(f"Created API key 2: {api_key2.name} (ID: {api_key2.id})")
        
        # Test 6: Get all API keys
        print_test("6️⃣ Getting all API keys")
        api_keys = walver.get_api_keys()
        print_success(f"Retrieved {len(api_keys)} API keys")
        for key in api_keys[-2:]:  # Show last 2 keys (our test keys)
            print_info(f"  - {key.name}: {key.description or 'No description'}")
        
        # =================================================================
        # VERIFICATION OPERATIONS TESTS
        # =================================================================
        print_test("🔗 Testing Verification Operations")
        
        # Test 7: Create basic verification
        print_test("7️⃣ Creating basic verification")
        
        basic_verification = walver.create_verification(
            id=f"test-basic-verification-sync-{test_id}",
            service_name="Test Service Basic (Sync)",
            chain="solana",
            webhook="https://webhook.example.com/verify",
        )
        created_verification_ids.append(f"test-basic-verification-sync-{test_id}")
        print_success(f"Created basic verification: {basic_verification.verification_url}")
        
        # Test 8: Create verification with folder and custom fields
        print_test("8️⃣ Creating verification with folder and custom fields")
        
        folder_verification = walver.create_verification(
            id=f"test-folder-verification-sync-{test_id}",
            service_name="Test Service with Folder (Sync)",
            chain="ethereum",
            folder_id=folder1.id,
            custom_fields=custom_fields[:2],  # Just email and phone
            webhook="https://webhook.example.com/verify",
            secret="super-secret-key-123",
            redirect_url="https://example.com/success",
            expiration=(datetime.now() + timedelta(days=7)).isoformat()
        )
        created_verification_ids.append(f"test-folder-verification-sync-{test_id}")
        print_success(f"Created folder verification: {folder_verification.verification_url}")
        
        # Test 9: Create verification with email verification
        print_test("9️⃣ Creating verification with email verification")
        
        email_verification = walver.create_verification(
            id=f"test-email-verification-sync-{test_id}", 
            service_name="Test Email Verification Service (Sync)",
            chain="solana",
            custom_fields=[custom_fields[0]],  # Email field
            force_email_verification=True,
            webhook="https://webhook.example.com/email-verify"
        )
        created_verification_ids.append(f"test-email-verification-sync-{test_id}")
        print_success(f"Created email verification: {email_verification.verification_url}")
        
        # Test 10: Create verification with telephone verification
        print_test("🔟 Creating verification with telephone verification")
        
        telephone_verification = walver.create_verification(
            id=f"test-telephone-verification-sync-{test_id}",
            service_name="Test Telephone Verification Service (Sync)", 
            chain="polygon",
            custom_fields=[custom_fields[1]],  # Phone field
            force_telephone_verification=True,
            webhook="https://webhook.example.com/telephone-verify"
        )
        created_verification_ids.append(f"test-telephone-verification-sync-{test_id}")
        print_success(f"Created telephone verification: {telephone_verification.verification_url}")
        
        # Test 11: Create verification with all social verifications
        print_test("1️⃣ 1️⃣ Creating verification with all social verifications")
        
        social_verification = walver.create_verification(
            id=f"test-social-verification-sync-{test_id}",
            service_name="Test All Social Verifications (Sync)",
            chain="solana", 
            custom_fields=custom_fields,  # All fields
            force_email_verification=True,
            force_telephone_verification=True,
            force_telegram_verification=True,
            force_twitter_verification=True,
            force_discord_verification=True,
            webhook="https://webhook.example.com/social-verify",
            secret="social-secret-456"
        )
        created_verification_ids.append(f"test-social-verification-sync-{test_id}")
        print_success(f"Created social verification: {social_verification.verification_url}")
        
        # Test 12: Create verification with token gate
        print_test("1️⃣ 2️⃣ Creating verification with token gate")
        
        token_verification = walver.create_verification(
            id=f"test-token-verification-sync-{test_id}",
            service_name="Test Token Gate Service (Sync)",
            chain="solana",
            token_gate=True,
            token_address="So11111111111111111111111111111111111111112",  # SOL token
            token_amount=1.5,
            is_nft=False,
            webhook="https://webhook.example.com/token-verify"
        )
        created_verification_ids.append(f"test-token-verification-sync-{test_id}")
        print_success(f"Created token verification: {token_verification.verification_url}")
        
        # Test 13: Create verification with NFT gate
        print_test("1️⃣3️⃣ Creating verification with NFT gate")
        
        nft_verification = walver.create_verification(
            id=f"test-nft-verification-sync-{test_id}", 
            service_name="Test NFT Gate Service (Sync)",
            chain="ethereum",
            token_gate=True,
            token_address="0x1234567890123456789012345678901234567890",
            token_amount=1,
            is_nft=True,
            one_time=True,
            webhook="https://webhook.example.com/nft-verify"
        )
        created_verification_ids.append(f"test-nft-verification-sync-{test_id}")
        print_success(f"Created NFT verification: {nft_verification.verification_url}")
        
        # Test 14: Get folder verifications (should now have some)
        print_test("1️⃣4️⃣ Getting folder verifications after creation")
        verifications = walver.get_folder_verifications(folder1.id)
        print_success(f"Retrieved {len(verifications)} verifications for folder")
        for verification in verifications:
            print_info(f"  - {verification.service_name} (ID: {verification.id})")
        
        # =================================================================
        # ERROR HANDLING TESTS
        # =================================================================
        print_test("🚨 Testing Error Handling")
        
        # Test 15: Try to create duplicate verification
        print_test("1️⃣5️⃣ Testing duplicate verification ID error")
        try:
            walver.create_verification(
                id=f"test-basic-verification-sync-{test_id}",  # Same ID as before
                service_name="Duplicate Test (Sync)",
                chain="solana"
            )
            print_error("Should have failed with duplicate ID")
        except ValueError as e:
            print_success(f"Correctly caught duplicate ID error: {e}")
        except Exception as e:
            print_warning(f"Unexpected error type: {e}")
        
        # Test 16: Try invalid token gate (missing token_address)
        print_test("1️⃣6️⃣ Testing invalid token gate error")
        try:
            walver.create_verification(
                id=f"test-invalid-token-sync-{test_id}",
                service_name="Invalid Token Gate (Sync)",
                chain="solana",
                token_gate=True,
                # Missing token_address and token_amount
            )
            print_error("Should have failed with missing token_address")
        except ValueError as e:
            print_success(f"Correctly caught token gate error: {e}")
        
        # Test 17: Try email verification without email field
        print_test("1️⃣7️⃣ Testing email verification without email field error")
        try:
            walver.create_verification(
                id=f"test-invalid-email-sync-{test_id}",
                service_name="Invalid Email Verification (Sync)",
                chain="solana",
                force_email_verification=True,
                custom_fields=[custom_fields[4]]  # Text field, not email
            )
            print_error("Should have failed with missing email field")
        except ValueError as e:
            print_success(f"Correctly caught email verification error: {e}")
        
        print_test("✅ All tests completed successfully!")
        
    except Exception as e:
        print_error(f"Test failed with error: {e}")
        raise
    
    finally:
        # =================================================================
        # CLEANUP
        # =================================================================
        print_test("🧹 Cleaning up test resources")
        
        # Delete created API keys
        for api_key_id in created_api_key_ids:
            try:
                result = walver.delete_api_key(api_key_id)
                print_success(f"Deleted API key: {api_key_id}")
            except Exception as e:
                print_warning(f"Failed to delete API key {api_key_id}: {e}")
        
        # Delete created folders (this should also clean up verifications in folders)
        for folder_id in created_folder_ids:
            try:
                result = walver.delete_folder(folder_id)
                print_success(f"Deleted folder: {folder_id}")
            except Exception as e:
                print_warning(f"Failed to delete folder {folder_id}: {e}")
        
        print_test("🎉 Test cleanup completed!")

# =================================================================
# ERROR HANDLING TESTS (without cleanup needed)
# =================================================================
def test_client_initialization():
    """Test client initialization scenarios"""
    print_test("🔧 Testing Client Initialization (Synchronous)")
    
    # Test without API key
    try:
        # Temporarily remove API key
        original_api_key = os.getenv("WALVER_API_KEY")
        os.environ.pop("WALVER_API_KEY", None)
        
        walver = Walver(base_url="https://walver.io")
        print_error("Should have failed without API key")
    except ValueError as e:
        print_success(f"Correctly caught missing API key error: {e}")
    finally:
        # Restore API key
        if original_api_key:
            os.environ["WALVER_API_KEY"] = original_api_key
    
    # Test with explicit API key
    try:
        walver = Walver(
            api_key="test-key",
            base_url="https://walver.io",
            timeout=30
        )
        print_success("Client initialized with explicit API key")
    except Exception as e:
        print_error(f"Failed to initialize with explicit API key: {e}")

def run_all_tests():
    """Run all tests"""
    print(f"{Colors.MAGENTA}{Colors.BOLD}")
    print("=" * 70)
    print("🧪 WALVER SDK SYNC CLIENT COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    print(f"{Colors.RESET}")
    
    # Test client initialization
    test_client_initialization()
    
    print()
    
    # Run main test suite
    test_walver_client()
    
    print(f"{Colors.GREEN}{Colors.BOLD}")
    print("=" * 70)
    print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print(f"{Colors.RESET}")

if __name__ == "__main__":
    run_all_tests() 