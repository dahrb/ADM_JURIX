#!/usr/bin/env python3
"""
Test ADM to debug reject condition logic
"""

from MainClasses import *
from UI import CLI

def create_test_adm():
    """Creates a simple test ADM to debug reject conditions"""
    adf = ADF("Test Reject ADM")
    
    # Add some basic nodes
    adf.addNodes("NodeA", question="Is NodeA true?")
    adf.addNodes("NodeB", question="Is NodeB true?")
    
    # Add a node with reject conditions
    # This should be rejected if NodeA is in the case
    adf.addNodes("TestReject", 
                 ["reject NodeA", "NodeB"], 
                 ["TestReject is rejected because NodeA is present", 
                  "TestReject is accepted because NodeB is true"])
    
    # Set question order
    adf.questionOrder = ["NodeA", "NodeB", "TestReject"]
    
    return adf

def test_reject_logic():
    """Test the reject logic with different scenarios"""
    print("=== Testing Reject Logic ===")
    
    # Create test ADM
    adf = create_test_adm()
    
    # Create UI instance
    ui = CLI()
    ui.adf = adf
    ui.case = []
    ui.caseName = "test"
    
    print(f"Test ADM created with nodes: {list(adf.nodes.keys())}")
    print(f"TestReject acceptance conditions: {adf.nodes['TestReject'].acceptance}")
    print(f"TestReject statements: {adf.nodes['TestReject'].statement}")
    
    # Test scenario 1: NodeA = True, NodeB = False
    print("\n--- Scenario 1: NodeA=True, NodeB=False ---")
    ui.case = ["NodeA"]  # Manually set case
    adf.case = ["NodeA"]  # Also set case on ADF
    print(f"Case: {ui.case}")
    
    # Manually evaluate TestReject
    result = adf.evaluateNode(adf.nodes['TestReject'])
    print(f"TestReject evaluation result: {result}")
    print(f"Reject flag: {adf.reject}")
    
    if result and not adf.reject:
        print("✅ TestReject should be ACCEPTED")
        if "TestReject" not in ui.case:
            ui.case.append("TestReject")
    else:
        print("❌ TestReject should be REJECTED")
    
    print(f"Final case: {ui.case}")
    
    # Test scenario 2: NodeA = False, NodeB = True
    print("\n--- Scenario 2: NodeA=False, NodeB=True ---")
    ui.case = ["NodeB"]  # Manually set case
    adf.case = ["NodeB"]  # Also set case on ADF
    print(f"Case: {ui.case}")
    
    # Manually evaluate TestReject
    result = adf.evaluateNode(adf.nodes['TestReject'])
    print(f"TestReject evaluation result: {result}")
    print(f"Reject flag: {adf.reject}")
    
    if result and not adf.reject:
        print("✅ TestReject should be ACCEPTED")
        if "TestReject" not in ui.case:
            ui.case.append("TestReject")
    else:
        print("❌ TestReject should be REJECTED")
    
    print(f"Final case: {ui.case}")
    
    # Test scenario 3: NodeA = True, NodeB = True
    print("\n--- Scenario 3: NodeA=True, NodeB=True ---")
    ui.case = ["NodeA", "NodeB"]  # Manually set case
    adf.case = ["NodeA", "NodeB"]  # Also set case on ADF
    print(f"Case: {ui.case}")
    
    # Manually evaluate TestReject
    result = adf.evaluateNode(adf.nodes['TestReject'])
    print(f"TestReject evaluation result: {result}")
    print(f"Reject flag: {adf.reject}")
    
    if result and not adf.reject:
        print("✅ TestReject should be ACCEPTED")
        if "TestReject" not in ui.case:
            ui.case.append("TestReject")
    else:
        print("❌ TestReject should be REJECTED")
    
    print(f"Final case: {ui.case}")
    
    # Test scenario 4: NodeA = False, NodeB = False
    print("\n--- Scenario 4: NodeA=False, NodeB=False ---")
    ui.case = []  # Manually set case
    adf.case = []  # Also set case on ADF
    print(f"Case: {ui.case}")
    
    # Manually evaluate TestReject
    result = adf.evaluateNode(adf.nodes['TestReject'])
    print(f"TestReject evaluation result: {result}")
    print(f"Reject flag: {adf.reject}")
    
    if result and not adf.reject:
        print("✅ TestReject should be ACCEPTED")
        if "TestReject" not in ui.case:
            ui.case.append("TestReject")
    else:
        print("❌ TestReject should be REJECTED")
    
    print(f"Final case: {ui.case}")

def test_postfix_evaluation():
    """Test the postfix evaluation directly"""
    print("\n=== Testing Postfix Evaluation Directly ===")
    
    adf = create_test_adm()
    
    # Test the reject condition directly
    print("Testing 'reject NodeA' condition:")
    adf.case = ["NodeA"]
    print(f"Case: {adf.case}")
    
    # Reset reject flag
    adf.reject = False
    
    # Evaluate the reject condition
    result = adf.postfixEvaluation("reject NodeA")
    print(f"Postfix evaluation result: {result}")
    print(f"Reject flag after evaluation: {adf.reject}")
    
    print("\nTesting 'reject NodeA' condition with NodeA not in case:")
    adf.case = []
    print(f"Case: {adf.case}")
    
    # Reset reject flag
    adf.reject = False
    
    # Evaluate the reject condition
    result = adf.postfixEvaluation("reject NodeA")
    print(f"Postfix evaluation result: {result}")
    print(f"Reject flag after evaluation: {adf.reject}")

if __name__ == "__main__":
    test_reject_logic()
    test_postfix_evaluation()
