#!/usr/bin/env python3
"""
Test script for sub-ADM tree evaluation
Tests the complete evaluation process that happens in the sub-ADM
"""

from MainClasses import *
from inventive_step_ADM import create_sub_adm_prior_art

def evaluate_sub_adm_tree(sub_adf, initial_responses):
    """
    Evaluate the complete sub-ADM tree with given responses
    
    Parameters:
    -----------
    sub_adf : SubADM
        The sub-ADM to evaluate
    initial_responses : dict
        Dictionary mapping node names to their responses (True/False)
    
    Returns:
    --------
    tuple: (final_case, root_node, result)
    """
    # Start with base case
    sub_adf.case = ["DistinguishingFeatures"]
    
    # Add nodes based on responses
    for node_name, response in initial_responses.items():
        if response and node_name not in sub_adf.case:
            sub_adf.case.append(node_name)
    
    print(f"Initial case after responses: {sub_adf.case}")
    
    # Evaluate abstract factors (nodes with children) in dependency order
    # We need to evaluate them in the correct order based on dependencies
    abstract_factors = []
    for factor in sub_adf.nodes:
        if (hasattr(sub_adf.nodes[factor], 'children') and 
            sub_adf.nodes[factor].children):
            abstract_factors.append(factor)
    
    print(f"Abstract factors to evaluate: {abstract_factors}")
    
    # Evaluate abstract factors
    for factor in abstract_factors:
        if factor not in sub_adf.case:
            node = sub_adf.nodes[factor]
            print(f"\nEvaluating {factor} with children: {node.children}")
            
            # Check if all children are in case
            if all(child in sub_adf.case for child in node.children):
                print(f"All children of {factor} are in case, evaluating...")
                
                # Evaluate the node
                result = sub_adf.evaluateNode(node)
                print(f"Evaluation result for {factor}: {result}, reject: {sub_adf.reject}")
                
                if result and not sub_adf.reject:
                    sub_adf.case.append(factor)
                    print(f"Added {factor} to case")
                else:
                    print(f"Did not add {factor} to case (rejected or failed)")
            else:
                missing_children = [child for child in node.children if child not in sub_adf.case]
                print(f"Cannot evaluate {factor} - missing children: {missing_children}")
    
    print(f"Final case: {sub_adf.case}")
    
    # Find the root node (final evaluated node)
    root_node = None
    
    # The root node is typically the last abstract factor that was evaluated
    accepted_abstract_factors = [factor for factor in abstract_factors if factor in sub_adf.case]
    if accepted_abstract_factors:
        root_node = accepted_abstract_factors[-1]
    
    # Determine final result
    if not root_node:
        result = 'UNKNOWN'
    elif root_node in sub_adf.case:
        result = 'ACCEPTED'
    else:
        result = 'REJECTED'
    
    return sub_adf.case, root_node, result

def test_scenarios():
    """Test various scenarios"""
    print("=== Sub-ADM Tree Evaluation Testing ===")
    
    scenarios = {
        "Independent Contribution Only": {
            "responses": {
                "IndependentContribution": True,
                "CombinationContribution": False,
                "CircumventTechProblem": False,
                "TechnicalAdaptation": False,
                "Credible": False,
                "Reproducible": False
            },
            "expected": "ACCEPTED",
            "description": "Feature makes independent technical contribution"
        },
        
        "Combination Contribution Only": {
            "responses": {
                "IndependentContribution": False,
                "CombinationContribution": True,
                "CircumventTechProblem": False,
                "TechnicalAdaptation": False,
                "Credible": False,
                "Reproducible": False
            },
            "expected": "ACCEPTED",
            "description": "Feature makes combination contribution"
        },
        
        "Computer Simulation with Technical Adaptation": {
            "responses": {
                "IndependentContribution": False,
                "CombinationContribution": False,
                "ComputerSimulation": True,
                "TechnicalAdaptation": True,
                "CircumventTechProblem": False,
                "Credible": False,
                "Reproducible": False
            },
            "expected": "ACCEPTED",
            "description": "Computer simulation with technical adaptation"
        },
        
        "Mathematical Method with Specific Purpose": {
            "responses": {
                "IndependentContribution": False,
                "CombinationContribution": False,
                "MathematicalMethod": True,
                "SpecificPurpose": True,
                "FunctionallyLimited": True,
                "CircumventTechProblem": False,
                "TechnicalAdaptation": False,
                "Credible": False,
                "Reproducible": False
            },
            "expected": "ACCEPTED",
            "description": "Mathematical method with specific technical purpose"
        },
        
        "Rejected by CircumventTechProblem": {
            "responses": {
                "IndependentContribution": True,
                "CombinationContribution": False,
                "CircumventTechProblem": True,  # This should cause rejection
                "TechnicalAdaptation": False,
                "Credible": False,
                "Reproducible": False
            },
            "expected": "REJECTED",
            "description": "Feature circumvents technical problem - should be rejected"
        },
        
        "Rejected by Excluded Field": {
            "responses": {
                "IndependentContribution": False,
                "CombinationContribution": False,
                "OtherExclusions": True,  # This should cause rejection
                "CircumventTechProblem": False,
                "TechnicalAdaptation": False,
                "Credible": False,
                "Reproducible": False
            },
            "expected": "REJECTED",
            "description": "Feature is in excluded field - should be rejected"
        },
        
        "Complex: Independent + Unexpected Effect": {
            "responses": {
                "IndependentContribution": True,
                "CombinationContribution": False,
                "UnexpectedEffect": True,
                "PreciseTerms": True,
                "OneWayStreet": True,
                "Credible": True,
                "Reproducible": True,
                "CircumventTechProblem": False,
                "TechnicalAdaptation": False
            },
            "expected": "ACCEPTED",
            "description": "Independent contribution with unexpected technical effect"
        },
        
        "Edge Case: No Technical Contribution": {
            "responses": {
                "IndependentContribution": False,
                "CombinationContribution": False,
                "CircumventTechProblem": False,
                "TechnicalAdaptation": False,
                "Credible": False,
                "Reproducible": False
            },
            "expected": "REJECTED",
            "description": "No technical contribution factors met"
        }
    }
    
    results = []
    
    for scenario_name, scenario_data in scenarios.items():
        print(f"\n{'='*80}")
        print(f"TESTING: {scenario_name}")
        print(f"{'='*80}")
        print(f"Description: {scenario_data['description']}")
        print(f"Expected: {scenario_data['expected']}")
        print(f"Responses: {scenario_data['responses']}")
        
        # Create sub-ADM
        sub_adf = create_sub_adm_prior_art("test_feature")
        
        # Evaluate the tree
        final_case, root_node, actual_result = evaluate_sub_adm_tree(sub_adf, scenario_data['responses'])
        
        # Check if result matches expectation
        success = actual_result == scenario_data['expected']
        
        print(f"\n--- Results ---")
        print(f"Root Node: {root_node}")
        print(f"Actual Result: {actual_result}")
        print(f"Expected Result: {scenario_data['expected']}")
        print(f"Status: {'✅ PASS' if success else '❌ FAIL'}")
        
        results.append({
            'scenario': scenario_name,
            'expected': scenario_data['expected'],
            'actual': actual_result,
            'success': success,
            'final_case': final_case,
            'root_node': root_node
        })
    
    return results

def generate_report(results):
    """Generate a test report"""
    print(f"\n{'='*80}")
    print(f"SUB-ADM TREE EVALUATION TEST REPORT")
    print(f"{'='*80}")
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r['success'])
    failed_tests = total_tests - passed_tests
    
    print(f"\nSUMMARY:")
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests} ✅")
    print(f"Failed: {failed_tests} ❌")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    print(f"\nDETAILED RESULTS:")
    print(f"{'Scenario':<50} {'Expected':<10} {'Actual':<10} {'Status':<8}")
    print(f"{'-'*80}")
    
    for result in results:
        status = "✅ PASS" if result['success'] else "❌ FAIL"
        print(f"{result['scenario']:<50} {result['expected']:<10} {result['actual']:<10} {status:<8}")
    
    if failed_tests > 0:
        print(f"\nFAILED TESTS ANALYSIS:")
        for result in results:
            if not result['success']:
                print(f"\n❌ {result['scenario']}")
                print(f"   Expected: {result['expected']}")
                print(f"   Actual: {result['actual']}")
                print(f"   Final Case: {result['final_case']}")
                print(f"   Root Node: {result['root_node']}")
    
    # Check reject condition scenarios specifically
    reject_scenarios = [r for r in results if 'Rejected' in r['scenario']]
    print(f"\n{'='*80}")
    print(f"REJECT CONDITION VERIFICATION")
    print(f"{'='*80}")
    print(f"Reject Condition Tests: {len(reject_scenarios)}")
    for scenario in reject_scenarios:
        status = "✅ PASS" if scenario['success'] else "❌ FAIL"
        print(f"  {scenario['scenario']}: {status}")
    
    return {
        'total': total_tests,
        'passed': passed_tests,
        'failed': failed_tests,
        'success_rate': (passed_tests/total_tests)*100
    }

def main():
    """Main test function"""
    print("Starting Sub-ADM Tree Evaluation Testing...")
    
    # Test scenarios
    results = test_scenarios()
    
    # Generate report
    report = generate_report(results)
    
    print(f"\nTesting completed!")
    return report

if __name__ == "__main__":
    main()
