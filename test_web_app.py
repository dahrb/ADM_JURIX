#!/usr/bin/env python3
"""
Simple test script for the web app
"""

import requests
import json

def test_web_app():
    """Test the web app endpoints"""
    base_url = "http://localhost:5000"
    
    print("Testing ADM Web App...")
    
    # Test 1: Load Wild Animals domain
    print("\n1. Testing domain loading...")
    response = requests.post(f"{base_url}/load_domain", data={'domain_type': 'wild_animals'})
    if response.status_code == 200:
        data = response.json()
        if data['success']:
            print(f"✓ Domain loaded: {data['domain_name']}")
        else:
            print(f"✗ Domain loading failed: {data['message']}")
            return
    else:
        print(f"✗ HTTP error: {response.status_code}")
        return
    
    # Test 2: Start query
    print("\n2. Testing query start...")
    response = requests.get(f"{base_url}/start_query")
    if response.status_code == 200:
        data = response.json()
        if data['success']:
            print(f"✓ Query started, first question: {data['question']['type']}")
            print(f"  Question: {data['question'].get('question', 'N/A')}")
        else:
            print(f"✗ Query start failed: {data['message']}")
            return
    else:
        print(f"✗ HTTP error: {response.status_code}")
        return
    
    # Test 3: Get case status
    print("\n3. Testing case status...")
    response = requests.get(f"{base_url}/get_case_status")
    if response.status_code == 200:
        data = response.json()
        if data['success']:
            print(f"✓ Case status retrieved")
            print(f"  Domain: {data['domain_name']}")
            print(f"  Case factors: {data['case']}")
        else:
            print(f"✗ Case status failed: {data['message']}")
    else:
        print(f"✗ HTTP error: {response.status_code}")
    
    print("\n✓ Basic web app functionality test completed!")

if __name__ == "__main__":
    test_web_app()

