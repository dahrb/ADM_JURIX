#!/usr/bin/env python3
"""
Direct test script for sub-ADM evaluation logic
Tests the evaluation logic directly without going through the UI
"""

from MainClasses import *
from inventive_step_ADM import create_sub_adm_prior_art

def test_direct_evaluation():
    """Test sub-ADM evaluation logic directly"""
    print("=== Direct Sub-ADM Evaluation Testing ===")
    
    # Create test scenarios
    scenarios = {
        "Independent Contribution Only": {
            "case": ["DistinguishingFeatures", "IndependentContribution"],
            "expected": "ACCEPTED",
            "description": "Feature makes independent technical contribution"
        },
        
        "Combination Contribution Only": {
            "case": ["DistinguishingFeatures", "CombinationContribution"],
            "expected": "ACCEPTED", 
            "description": "Feature makes combination contribution"
        },
        
        "Computer Simulation with Technical Adaptation": {
            "case": ["DistinguishingFeatures", "ComputerSimulation", "TechnicalAdaptation"],
            "expected": "ACCEPTED",
            "description": "Computer simulation with technical adaptation"
        },
        
        "Mathematical Method with Specific Purpose": {
            "case": ["DistinguishingFeatures", "MathematicalMethod", "SpecificPurpose", "FunctionallyLimited"],
            "expected": "ACCEPTED",
            "description": "Mathematical method with specific technical purpose"
        },
        
        "Rejected by CircumventTechProblem": {
            "case": ["DistinguishingFeatures", "IndependentContribution", "CircumventTechProblem"],
            "expected": "REJECTED",
            "description": "Feature circumvents technical problem - should be rejected"
        },
        
        "Rejected by Excluded Field": {
            "case": ["DistinguishingFeatures", "OtherExclusions"],
            "expected": "REJECTED",
            "description": "Feature is in excluded field - should be rejected"
        },
        
        "Complex: Independent + Unexpected Effect": {
            "case": ["DistinguishingFeatures", "IndependentContribution", "UnexpectedEffect", "PreciseTerms", "OneWayStreet", "Credible", "Reproducible"],
            "expected": "ACCEPTED",
            "description": "Independent contribution with unexpected technical effect"
        },
        
        "Edge Case: No Technical Contribution": {
            "case": ["DistinguishingFeatures"],
            "expected": "REJECTED",
            "description": "No technical contribution factors met"
        }
    }
    
    results = []
    
    for scenario_name, scenario_data in scenarios.items():
        print(f"\n{'='*60}")
        print(f"Testing: {scenario_name}")
        print(f"Description: {scenario_data['description']}")
        print(f"Expected: {scenario_data['expected']}")
        print(f"Test Case: {scenario_data['case']}")
        
        # Create sub-ADM
        sub_adf = create_sub_adm_prior_art("test_feature")
        
        # Set the case directly
        sub_adf.case = scenario_data['case'].copy()
        
        # Find the root node (final evaluated node)
        root_node = None
        
        # Try to find from statements first
        if hasattr(sub_adf, 'statements') and sub_adf.statements:
            final_statement = sub_adf.statements[-1]
            for node_name, node in sub_adf.nodes.items():
                if hasattr(node, 'statement') and node.statement and final_statement in node.statement:
                    root_node = node_name
                    break
        
        # Fallback to last node in question order
        if not root_node and sub_adf.questionOrder:
            root_node = sub_adf.questionOrder[-1]
        
        # Determine result
        if not root_node:
            actual_result = 'UNKNOWN'
        elif root_node in sub_adf.case:
            actual_result = 'ACCEPTED'
        else:
            actual_result = 'REJECTED'
        
        # Check if result matches expectation
        success = actual_result == scenario_data['expected']
        
        print(f"Root Node: {root_node}")
        print(f"Actual Result: {actual_result}")
        print(f"Status: {'✅ PASS' if success else '❌ FAIL'}")
        
        results.append({
            'scenario': scenario_name,
            'expected': scenario_data['expected'],
            'actual': actual_result,
            'success': success,
            'case': scenario_data['case'],
            'root_node': root_node
        })
    
    return results

def test_reject_conditions():
    """Test reject conditions specifically"""
    print(f"\n{'='*60}")
    print("TESTING REJECT CONDITIONS")
    print(f"{'='*60}")
    
    # Create sub-ADM
    sub_adf = create_sub_adm_prior_art("test_feature")
    
    # Test NormalTechnicalContribution with different cases
    test_cases = [
        {
            "name": "NormalTechnicalContribution - IndependentContribution only",
            "case": ["DistinguishingFeatures", "IndependentContribution"],
            "expected": "ACCEPTED"
        },
        {
            "name": "NormalTechnicalContribution - with CircumventTechProblem",
            "case": ["DistinguishingFeatures", "IndependentContribution", "CircumventTechProblem"],
            "expected": "REJECTED"
        },
        {
            "name": "NormalTechnicalContribution - with ExcludedField",
            "case": ["DistinguishingFeatures", "IndependentContribution", "ComputerSimulation"],
            "expected": "REJECTED"
        }
    ]
    
    for test_case in test_cases:
        print(f"\n--- {test_case['name']} ---")
        print(f"Case: {test_case['case']}")
        
        # Set case and evaluate NormalTechnicalContribution
        sub_adf.case = test_case['case'].copy()
        node = sub_adf.nodes['NormalTechnicalContribution']
        
        # Evaluate the node
        result = sub_adf.evaluateNode(node)
        print(f"Evaluation result: {result}")
        print(f"Reject flag: {sub_adf.reject}")
        
        # Determine if node should be in case
        if result and not sub_adf.reject:
            actual = "ACCEPTED"
        else:
            actual = "REJECTED"
        
        success = actual == test_case['expected']
        print(f"Expected: {test_case['expected']}")
        print(f"Actual: {actual}")
        print(f"Status: {'✅ PASS' if success else '❌ FAIL'}")

def generate_report(results):
    """Generate a test report"""
    print(f"\n{'='*60}")
    print("TEST REPORT")
    print(f"{'='*60}")
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r['success'])
    failed_tests = total_tests - passed_tests
    
    print(f"\nSUMMARY:")
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests} ✅")
    print(f"Failed: {failed_tests} ❌")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    print(f"\nDETAILED RESULTS:")
    print(f"{'Scenario':<40} {'Expected':<10} {'Actual':<10} {'Status':<8}")
    print(f"{'-'*70}")
    
    for result in results:
        status = "✅ PASS" if result['success'] else "❌ FAIL"
        print(f"{result['scenario']:<40} {result['expected']:<10} {result['actual']:<10} {status:<8}")
    
    if failed_tests > 0:
        print(f"\nFAILED TESTS:")
        for result in results:
            if not result['success']:
                print(f"\n❌ {result['scenario']}")
                print(f"   Expected: {result['expected']}")
                print(f"   Actual: {result['actual']}")
                print(f"   Case: {result['case']}")
                print(f"   Root Node: {result['root_node']}")
    
    return {
        'total': total_tests,
        'passed': passed_tests,
        'failed': failed_tests,
        'success_rate': (passed_tests/total_tests)*100
    }

def main():
    """Main test function"""
    print("Starting Direct Sub-ADM Testing...")
    
    # Test direct evaluation
    results = test_direct_evaluation()
    
    # Test reject conditions specifically
    test_reject_conditions()
    
    # Generate report
    report = generate_report(results)
    
    print(f"\nTesting completed!")
    return report

if __name__ == "__main__":
    main()
