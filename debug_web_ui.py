#!/usr/bin/env python3
"""
Debug script to test the web UI API directly
"""

import requests
import json

def test_web_ui():
    base_url = "http://localhost:5000"
    
    print("Testing Web UI API...")
    
    # Test 1: Start session
    print("\n1. Starting session...")
    response = requests.post(f"{base_url}/start_session")
    if response.status_code == 200:
        data = response.json()
        session_id = data['session_id']
        print(f"✅ Session started: {session_id}")
    else:
        print(f"❌ Failed to start session: {response.status_code}")
        return
    
    # Test 2: Get first question
    print("\n2. Getting first question...")
    response = requests.get(f"{base_url}/api/question", params={'session_id': session_id})
    if response.status_code == 200:
        data = response.json()
        print(f"✅ First question: {json.dumps(data, indent=2)}")
        
        if data.get('type') == 'instantiator':
            # Answer the first question
            print("\n3. Answering first question...")
            answer_data = {
                'session_id': session_id,
                'question_name': data['name'],
                'answer': 'quantitative'
            }
            response = requests.post(f"{base_url}/api/answer", json=answer_data)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Answer submitted: {json.dumps(result, indent=2)}")
                
                if result.get('status') == 'next_question':
                    # Get the next question
                    print("\n4. Getting next question...")
                    response = requests.get(f"{base_url}/api/question", params={'session_id': session_id})
                    if response.status_code == 200:
                        data = response.json()
                        print(f"✅ Second question: {json.dumps(data, indent=2)}")
                        
                        if data.get('type') == 'simple':
                            # Answer the simple question
                            print("\n5. Answering simple question...")
                            answer_data = {
                                'session_id': session_id,
                                'question_name': data['name'],
                                'answer': 'Yes'
                            }
                            response = requests.post(f"{base_url}/api/answer", json=answer_data)
                            if response.status_code == 200:
                                result = response.json()
                                print(f"✅ Answer submitted: {json.dumps(result, indent=2)}")
                                
                                if result.get('status') == 'next_question':
                                    # Get the next question (should be SOURCES)
                                    print("\n6. Getting SOURCES question...")
                                    response = requests.get(f"{base_url}/api/question", params={'session_id': session_id})
                                    if response.status_code == 200:
                                        data = response.json()
                                        print(f"✅ SOURCES question: {json.dumps(data, indent=2)}")
                                        
                                        if data.get('type') == 'algorithmic':
                                            print("🎉 SUCCESS! Algorithmic question detected correctly!")
                                        else:
                                            print(f"❌ Expected algorithmic question, got: {data.get('type')}")
                                    else:
                                        print(f"❌ Failed to get SOURCES question: {response.status_code}")
                                else:
                                    print(f"❌ Unexpected result: {result}")
                            else:
                                print(f"❌ Failed to submit answer: {response.status_code}")
                        else:
                            print(f"❌ Expected simple question, got: {data.get('type')}")
                    else:
                        print(f"❌ Failed to get second question: {response.status_code}")
                else:
                    print(f"❌ Unexpected result: {result}")
            else:
                print(f"❌ Failed to submit answer: {response.status_code}")
        else:
            print(f"❌ Expected instantiator question, got: {data.get('type')}")
    else:
        print(f"❌ Failed to get first question: {response.status_code}")

if __name__ == "__main__":
    test_web_ui()
