#!/usr/bin/env python3
"""
Quick ADM Testing Script
For focused testing and debugging of specific issues
"""

import copy
from MainClasses import ADF

def quick_test_adm(adm_instance, test_cases=None):
    """
    Quick test of ADM with specific test cases
    
    Parameters:
    -----------
    adm_instance : ADF
        The ADM instance to test
    test_cases : list, optional
        List of test cases to run. If None, runs default test cases.
    """
    print(f"Quick Testing ADM: {adm_instance.name}")
    print("=" * 60)
    
    if test_cases is None:
        # Default test cases
        test_cases = [
            [],  # Empty case
            ["QUANTITATIVE"],  # Single BLF
            ["QUANTITATIVE", "QUALITATIVE"],  # Two BLFs
            ["QUANTITATIVE", "QUALITATIVE", "NOVELTY"],  # Three BLFs
            ["NON_EXISTENT"],  # Invalid BLF
        ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\n--- Test Case {i+1}: {test_case} ---")
        
        try:
            # Create a copy for testing
            test_adm = copy.deepcopy(adm_instance)
            
            # Show initial state
            print(f"  Initial case: {test_case}")
            print(f"  Non-leaf nodes: {list(test_adm.nonLeaf.keys()) if hasattr(test_adm, 'nonLeaf') else 'None'}")
            
            # Run evaluation
            statements = test_adm.evaluateTree(test_case)
            
            # Show results
            print(f"  Final case: {test_adm.case}")
            print(f"  Statements: {statements}")
            print(f"  ✓ SUCCESS")
            
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            import traceback
            traceback.print_exc()

def test_specific_scenario(adm_instance, scenario_name, blfs_to_accept):
    """
    Test a specific scenario and show detailed evaluation steps
    
    Parameters:
    -----------
    adm_instance : ADF
        The ADM instance to test
    scenario_name : str
        Name of the scenario being tested
    blfs_to_accept : list
        List of BLFs to accept in this scenario
    """
    print(f"\n{'='*80}")
    print(f"TESTING SCENARIO: {scenario_name}")
    print(f"BLFs to accept: {blfs_to_accept}")
    print(f"{'='*80}")
    
    try:
        # Create a copy for testing
        test_adm = copy.deepcopy(adm_instance)
        
        # Step 1: Show initial state
        print(f"\nStep 1: Initial State")
        print(f"  Case: {blfs_to_accept}")
        print(f"  Non-leaf nodes: {list(test_adm.nonLeaf.keys()) if hasattr(test_adm, 'nonLeaf') else 'None'}")
        
        # Step 2: Show acceptance conditions for abstract factors
        print(f"\nStep 2: Abstract Factor Analysis")
        for name, node in test_adm.nodes.items():
            if hasattr(node, 'children') and node.children:
                print(f"  {name}:")
                print(f"    Children: {node.children}")
                print(f"    Acceptance: {node.acceptance}")
                print(f"    Statements: {node.statement}")
        
        # Step 3: Run evaluation
        print(f"\nStep 3: Running Evaluation")
        statements = test_adm.evaluateTree(blfs_to_accept)
        
        # Step 4: Show results
        print(f"\nStep 4: Results")
        print(f"  Final case: {test_adm.case}")
        print(f"  Statements generated: {len(statements)}")
        for i, statement in enumerate(statements, 1):
            print(f"    {i}. {statement}")
        
        # Step 5: Analysis
        print(f"\nStep 5: Analysis")
        initial_count = len(blfs_to_accept)
        final_count = len(test_adm.case)
        added_count = final_count - initial_count
        
        print(f"  Initial BLFs: {initial_count}")
        print(f"  Final BLFs: {final_count}")
        print(f"  Added BLFs: {added_count}")
        
        if added_count > 0:
            added_blfs = [b for b in test_adm.case if b not in blfs_to_accept]
            print(f"  Newly added: {added_blfs}")
        
        print(f"  ✓ Scenario completed successfully")
        
    except Exception as e:
        print(f"  ✗ Scenario failed: {e}")
        import traceback
        traceback.print_exc()

def analyze_adm_structure(adm_instance):
    """Analyze the structure of the ADM"""
    print(f"\n{'='*80}")
    print(f"ADM STRUCTURE ANALYSIS")
    print(f"{'='*80}")
    
    print(f"\nADM Name: {adm_instance.name}")
    print(f"Total nodes: {len(adm_instance.nodes)}")
    
            # Categorize nodes
        blfs = []
        abstract_factors = []
        special_nodes = []
        
        for name, node in adm_instance.nodes.items():
            if hasattr(node, 'children') and node.children:
                abstract_factors.append(name)
            elif hasattr(node, 'checkDependency'):
                special_nodes.append((name, 'DependentBLF'))
            elif hasattr(node, 'evaluateResults'):
                special_nodes.append((name, 'EvaluationBLF'))
            elif hasattr(node, 'evaluateSubADMs'):
                special_nodes.append((name, 'SubADMBLF'))
            else:
                # Only include actual BLFs (not special nodes)
                if not hasattr(node, 'checkDependency') and \
                   not hasattr(node, 'evaluateResults') and \
                   not hasattr(node, 'evaluateSubADMs'):
                    blfs.append(name)
    
    print(f"\nBase-Level Factors (BLFs): {len(blfs)}")
    for blf in blfs:
        node = adm_instance.nodes[blf]
        question = getattr(node, 'question', 'No question')
        print(f"  {blf}: {question}")
    
    print(f"\nAbstract Factors: {len(abstract_factors)}")
    for af in abstract_factors:
        node = adm_instance.nodes[af]
        children = getattr(node, 'children', [])
        acceptance = getattr(node, 'acceptance', [])
        print(f"  {af}:")
        print(f"    Children: {children}")
        print(f"    Acceptance: {acceptance}")
    
    print(f"\nSpecial Nodes: {len(special_nodes)}")
    for name, node_type in special_nodes:
        print(f"  {name}: {node_type}")
    
    # Show question order
    if hasattr(adm_instance, 'questionOrder') and adm_instance.questionOrder:
        print(f"\nQuestion Order: {adm_instance.questionOrder}")
    
    # Show question instantiators
    if hasattr(adm_instance, 'question_instantiators') and adm_instance.question_instantiators:
        print(f"\nQuestion Instantiators: {len(adm_instance.question_instantiators)}")
        for name, instantiator in adm_instance.question_instantiators.items():
            print(f"  {name}: {instantiator['question']}")

def main():
    """Main function for quick testing"""
    print("Quick ADM Testing Script")
    print("=" * 50)
    
    try:
        # Import your ADM
        from academic_research_ADM import adf
        print(f"Loaded ADM: {adf.name}")
        
        # Analyze structure
        analyze_adm_structure(adf)
        
        # Quick tests
        quick_test_adm(adf)
        
        # Test specific scenarios
        test_specific_scenario(adf, "Quantitative Research", ["QUANTITATIVE"])
        test_specific_scenario(adf, "Mixed Methods Research", ["QUANTITATIVE", "QUALITATIVE"])
        test_specific_scenario(adf, "Complex Research", ["QUANTITATIVE", "QUALITATIVE", "NOVELTY"])
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Please ensure your ADM is properly defined and importable")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

