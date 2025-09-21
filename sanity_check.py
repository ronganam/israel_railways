#!/usr/bin/env python3
"""
Simple sanity check script for Israel Railways API
This script tests the basic functionality of the israel_railways_api module.
"""

import asyncio
import sys
from israel_railways_api import IsraelRailwaysAPI


async def test_station_names():
    """Test the get_station_name method with sample station IDs."""
    print("=" * 50)
    print("Testing station name lookup...")
    print("=" * 50)
    
    # Using Tel Aviv Central (station ID 3700) and Haifa Central (station ID 9000) as examples
    api = IsraelRailwaysAPI("3700", "9000")
    
    try:
        station_a_name, station_b_name = await api.get_station_name()
        print(f"Station A (ID: 3700): {station_a_name}")
        print(f"Station B (ID: 9000): {station_b_name}")
        
        if station_a_name and station_b_name:
            print("✅ Station name lookup successful!")
            return True
        else:
            print("❌ Station name lookup failed - no names returned")
            return False
            
    except Exception as e:
        print(f"❌ Error during station name lookup: {e}")
        return False


async def test_next_train():
    """Test the get_next_train method with sample stations."""
    print("\n" + "=" * 50)
    print("Testing next train lookup...")
    print("=" * 50)
    
    # Using Tel Aviv Central (station ID 3700) and Haifa Central (station ID 9000)
    api = IsraelRailwaysAPI("3700", "9000")
    
    try:
        next_train = await api.get_next_train()
        
        if next_train:
            print("✅ Next train found!")
            print(f"Train details: {next_train}")
            
            # Extract some key information if available
            if 'trainNumber' in next_train:
                print(f"Train Number: {next_train['trainNumber']}")
            if 'departureTime' in next_train:
                print(f"Departure Time: {next_train['departureTime']}")
            if 'arrivalTime' in next_train:
                print(f"Arrival Time: {next_train['arrivalTime']}")
                
            return True
        else:
            print("⚠️  No upcoming trains found (this might be normal depending on time)")
            return True  # This is not necessarily an error
            
    except Exception as e:
        print(f"❌ Error during next train lookup: {e}")
        return False


async def test_api_connection():
    """Test basic API connectivity."""
    print("\n" + "=" * 50)
    print("Testing API connectivity...")
    print("=" * 50)
    
    try:
        # Test with a simple station lookup first
        api = IsraelRailwaysAPI("3700", "9000")
        station_a_name, station_b_name = await api.get_station_name()
        
        if station_a_name or station_b_name:
            print("✅ API connection successful!")
            return True
        else:
            print("❌ API connection failed - no response")
            return False
            
    except Exception as e:
        print(f"❌ API connection error: {e}")
        return False


async def main():
    """Main function to run all sanity checks."""
    print("Israel Railways API - Sanity Check")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: API Connection
    if await test_api_connection():
        tests_passed += 1
    
    # Test 2: Station Names
    if await test_station_names():
        tests_passed += 1
    
    # Test 3: Next Train
    if await test_next_train():
        tests_passed += 1
    
    # Summary
    print("\n" + "=" * 50)
    print("SANITY CHECK SUMMARY")
    print("=" * 50)
    print(f"Tests passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! The Israel Railways API is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the error messages above.")
        return 1


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nSanity check interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error during sanity check: {e}")
        sys.exit(1)
