#!/usr/bin/env python3
"""
Demo script for the ADM Web UI
This script demonstrates how to use the web interface programmatically
"""

import requests
import json
import time
import base64
from pathlib import Path

class ADMWebUIDemo:
    """Demo class for the ADM Web UI"""
    
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session_id = None
        self.session = requests.Session()
    
    def start_session(self):
        """Start a new ADM session"""
        print("🚀 Starting new ADM session...")
        
        response = self.session.post(f"{self.base_url}/start_session")
        if response.status_code == 200:
            data = response.json()
            self.session_id = data['session_id']
            print(f"✅ Session started: {self.session_id}")
            return True
        else:
            print(f"❌ Failed to start session: {response.status_code}")
            return False
    
    def get_current_question(self):
        """Get the current question for the session"""
        if not self.session_id:
            print("❌ No active session")
            return None
        
        response = self.session.get(f"{self.base_url}/api/question", 
                                  params={'session_id': self.session_id})
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'complete':
                print("✅ Evaluation complete!")
                return None
            return data
        else:
            print(f"❌ Failed to get question: {response.status_code}")
            return None
    
    def submit_answer(self, question_name, answer):
        """Submit an answer for a question"""
        if not self.session_id:
            print("❌ No active session")
            return False
        
        data = {
            'session_id': self.session_id,
            'question_name': question_name,
            'answer': answer
        }
        
        response = self.session.post(f"{self.base_url}/api/answer", 
                                   json=data)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('status') == 'complete':
                print("✅ Evaluation complete!")
                return result
            elif result.get('status') == 'next_question':
                print("➡️ Moving to next question...")
                return result
            else:
                print(f"❌ Unexpected response: {result}")
                return False
        else:
            print(f"❌ Failed to submit answer: {response.status_code}")
            return False
    
    def get_session_info(self):
        """Get session information and progress"""
        if not self.session_id:
            print("❌ No active session")
            return None
        
        response = self.session.get(f"{self.base_url}/api/session_info", 
                                  params={'session_id': self.session_id})
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Failed to get session info: {response.status_code}")
            return None
    
    def run_demo(self):
        """Run a complete demo of the ADM evaluation process"""
        print("🎯 ADM Web UI Demo")
        print("=" * 50)
        
        # Start session
        if not self.start_session():
            return
        
        question_count = 0
        max_questions = 10  # Prevent infinite loops
        
        while question_count < max_questions:
            # Get current question
            question = self.get_current_question()
            if not question:
                break
            
            question_count += 1
            print(f"\n📝 Question {question_count}: {question.get('name', 'Unknown')}")
            print(f"   Type: {question.get('type', 'Unknown')}")
            print(f"   Text: {question.get('question', 'No question text')}")
            
            # Get session progress
            session_info = self.get_session_info()
            if session_info:
                progress = session_info.get('progress', 0)
                current = session_info.get('current_question', 0)
                total = session_info.get('total_questions', 0)
                print(f"   Progress: {progress:.1f}% ({current}/{total})")
            
            # Handle different question types
            if question.get('type') == 'instantiator':
                choices = question.get('choices', [])
                print(f"   Choices: {', '.join(choices)}")
                
                # Auto-select first choice for demo
                answer = choices[0] if choices else 'default'
                print(f"   Auto-selecting: {answer}")
                
            elif question.get('type') == 'simple':
                choices = question.get('choices', ['Yes', 'No'])
                print(f"   Choices: {', '.join(choices)}")
                
                # Auto-select 'Yes' for demo
                answer = 'Yes'
                print(f"   Auto-selecting: {answer}")
                
            elif question.get('type') == 'algorithmic':
                questions = question.get('questions', [])
                print(f"   Input questions: {len(questions)}")
                
                # Auto-fill with demo data
                answer = ['demo_data'] * len(questions)
                print(f"   Auto-filling: {answer}")
                
            elif question.get('type') == 'sub_adm':
                print("   Sub-ADM evaluation - auto-processing")
                answer = 'auto'
                
            else:
                print(f"   Unknown question type: {question.get('type')}")
                answer = 'default'
            
            # Submit answer
            print(f"   Submitting answer: {answer}")
            result = self.submit_answer(question['name'], answer)
            
            if result and result.get('status') == 'complete':
                print("\n🎉 Evaluation completed!")
                if 'case' in result:
                    print(f"   Case factors: {', '.join(result['case'])}")
                if 'results' in result:
                    print(f"   Results: {len(result['results'])} statements")
                break
            
            # Small delay for demo purposes
            time.sleep(0.5)
        
        if question_count >= max_questions:
            print(f"\n⚠️ Demo stopped after {max_questions} questions")
        
        print("\n🏁 Demo completed!")
        print(f"Session ID: {self.session_id}")
        print(f"Questions processed: {question_count}")

def main():
    """Main function"""
    print("ADM Web UI Demo Script")
    print("This script demonstrates the web interface functionality")
    print()
    
    # Check if the web UI is running
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        if response.status_code == 200:
            print("✅ Web UI is running at http://localhost:5000")
        else:
            print("⚠️ Web UI responded with unexpected status code")
    except requests.exceptions.RequestException:
        print("❌ Web UI is not running")
        print("Please start the web UI first:")
        print("  python run_web_ui.py")
        return
    
    print()
    
    # Run the demo
    demo = ADMWebUIDemo()
    demo.run_demo()

if __name__ == "__main__":
    main()
