#!/usr/bin/env python3
"""
Test script for evaluating sub-ADMs directly without going through the main ADM
"""

from MainClasses import *
from inventive_step_ADM import create_sub_adm_prior_art
from UI import CLI

def test_sub_adm_evaluation():
    """
    Test function to evaluate a sub-ADM directly
    """
    print("=== Testing Sub-ADM Evaluation ===")
    
    # Create a test item name
    test_item = "test_feature"
    
    # Create key facts that would normally come from the main ADM
    key_facts = {
        'CPA': 'Test prior art document',
        'INVENTION_TITLE': 'Test invention',
        'INFORMATION': {
            'CPA': 'Test prior art document',
            'INVENTION_TITLE': 'Test invention'
        }
    }
    
    print(f"Creating sub-ADM for item: {test_item}")
    
    # Create the sub-ADM
    sub_adf = create_sub_adm_prior_art(test_item, key_facts)
    
    print(f"Sub-ADM created with {len(sub_adf.nodes)} nodes")
    print(f"Question order: {sub_adf.questionOrder}")
    
    # Create a UI instance for evaluation
    ui = CLI()
    ui.adf = sub_adf
    ui.case = sub_adf.case.copy()  # Start with the initial case
    ui.caseName = test_item
    
    print(f"Initial case: {ui.case}")
    
    # Evaluate the sub-ADM by asking questions
    print("\n=== Starting Sub-ADM Evaluation ===")
    ui.ask_questions()
    
    # Get the final case
    final_case = ui.case
    print(f"\nFinal case: {final_case}")
    
    # Determine the result based on whether the root node is accepted or rejected
    # The root node is the final node that gets evaluated (corresponds to final statement in explanation)
    root_node = None
    
    # Find the node that was evaluated last by looking at the evaluation order
    # The final node is typically the one that corresponds to the final statement
    if hasattr(ui.adf, 'statements') and ui.adf.statements:
        print(f"Statements generated: {ui.adf.statements}")
        # The final statement corresponds to the final evaluated node
        final_statement = ui.adf.statements[-1]
        print(f"Final statement: {final_statement}")
        
        # Find the node that has this statement
        for node_name, node in ui.adf.nodes.items():
            if hasattr(node, 'statement') and node.statement and final_statement in node.statement:
                root_node = node_name
                print(f"Found root node: {root_node}")
                break
    
    # Fallback: if we can't find the root node from statements, use the last node in question order
    if not root_node and sub_adf.questionOrder:
        root_node = sub_adf.questionOrder[-1]
        print(f"Using fallback root node: {root_node}")
    
    if not root_node:
        print(f"  → {test_item} classification: UNKNOWN (no root node found)")
        return 'UNKNOWN', final_case
    
    if root_node in final_case:
        # Root node was accepted
        print(f"  → {test_item} classified as {root_node} (ACCEPTED)")
        return 'ACCEPTED', final_case
    else:
        # Root node was rejected (not in final_case)
        print(f"  → {test_item} REJECTED (root node {root_node} rejected)")
        return 'REJECTED', final_case

def test_multiple_items():
    """
    Test function to evaluate multiple items with the same sub-ADM
    """
    print("\n=== Testing Multiple Items ===")
    
    test_items = ["feature_a", "feature_b", "feature_c"]
    results = {}
    
    for item in test_items:
        print(f"\n--- Testing item: {item} ---")
        result, case = test_sub_adm_evaluation()
        results[item] = (result, case)
    
    print(f"\n=== Summary ===")
    for item, (result, case) in results.items():
        print(f"{item}: {result} - {case}")

if __name__ == "__main__":
    # Test single item
    test_sub_adm_evaluation()
    
    # Uncomment to test multiple items
    # test_multiple_items()
