#!/usr/bin/env python3

import asyncio
import sys
import argparse
from test_complete_async import run_all_tests as run_async_tests, test_client_initialization as test_async_init, test_walver_client as test_async_client
from test_complete_sync import run_all_tests as run_sync_tests, test_client_initialization as test_sync_init, test_walver_client as test_sync_client

async def run_specific_tests(test_type, client_type="both"):
    """Run specific test categories"""
    
    if client_type in ["async", "both"]:
        if test_type == "init":
            await test_async_init()
        elif test_type == "folders":
            # Run only folder-related tests (would need to extract from main test)
            print("Running folder tests only is not implemented yet. Use 'all' for complete test.")
        elif test_type == "api-keys": 
            # Run only API key tests (would need to extract from main test)
            print("Running API key tests only is not implemented yet. Use 'all' for complete test.")
        elif test_type == "verifications":
            # Run only verification tests (would need to extract from main test)
            print("Running verification tests only is not implemented yet. Use 'all' for complete test.")
        elif test_type == "all":
            await run_async_tests()
        else:
            print(f"Unknown test type: {test_type}")
            print("Available test types: init, folders, api-keys, verifications, all")
            return
    
    if client_type in ["sync", "both"] and client_type != "async":
        print("\n" + "="*50)
        print("🔄 RUNNING SYNCHRONOUS CLIENT TESTS")
        print("="*50)
        
        if test_type == "init":
            test_sync_init()
        elif test_type == "folders":
            # Run only folder-related tests (would need to extract from main test)
            print("Running folder tests only is not implemented yet. Use 'all' for complete test.")
        elif test_type == "api-keys": 
            # Run only API key tests (would need to extract from main test)
            print("Running API key tests only is not implemented yet. Use 'all' for complete test.")
        elif test_type == "verifications":
            # Run only verification tests (would need to extract from main test)
            print("Running verification tests only is not implemented yet. Use 'all' for complete test.")
        elif test_type == "all":
            run_sync_tests()
        else:
            print(f"Unknown test type: {test_type}")
            print("Available test types: init, folders, api-keys, verifications, all")

def main():
    parser = argparse.ArgumentParser(description="Run Walver SDK tests")
    parser.add_argument(
        "test_type", 
        nargs="?", 
        default="all",
        choices=["init", "folders", "api-keys", "verifications", "all"],
        help="Type of tests to run (default: all)"
    )
    parser.add_argument(
        "--client-type", 
        "-c",
        choices=["async", "sync", "both"],
        default="both",
        help="Which client type to test (default: both)"
    )
    parser.add_argument(
        "--verbose", 
        "-v", 
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    client_desc = {
        "async": "asynchronous",
        "sync": "synchronous", 
        "both": "both async and sync"
    }[args.client_type]
    
    print(f"Running {args.test_type} tests for {client_desc} client(s)...")
    
    try:
        asyncio.run(run_specific_tests(args.test_type, args.client_type))
    except KeyboardInterrupt:
        print("\n⚠️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Tests failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 