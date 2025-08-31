#!/usr/bin/env python3
"""
Simple ADM Test Script
Tests core functionality without visualization
"""

import copy
from MainClasses import ADF

def test_adm_core_functionality():
    """Test the core ADM functionality"""
    print("Testing ADM Core Functionality")
    print("=" * 50)
    
    try:
        # Import your ADM
        from academic_research_ADM import adf
        print(f"✓ Loaded ADM: {adf.name}")
        
        # Test basic structure
        print(f"\nADM Structure:")
        print(f"  Total nodes: {len(adf.nodes)}")
        print(f"  Question order: {adf.questionOrder}")
        
        # Categorize nodes
        blfs = []
        abstract_factors = []
        special_nodes = []
        
        for name, node in adf.nodes.items():
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
        
        print(f"  Base-Level Factors: {len(blfs)}")
        print(f"  Abstract Factors: {len(abstract_factors)}")
        print(f"  Special Nodes: {len(special_nodes)}")
        
        # Test basic evaluation
        print(f"\nTesting Basic Evaluation:")
        
        # Test case 1: Empty case
        print(f"\nTest 1: Empty case")
        try:
            test_adm = copy.deepcopy(adf)
            statements = test_adm.evaluateTree([])
            print(f"  ✓ Success: {len(statements)} statements generated")
            print(f"  Final case: {test_adm.case}")
        except Exception as e:
            print(f"  ✗ Error: {e}")
        
        # Test case 2: Single BLF
        if blfs:
            print(f"\nTest 2: Single BLF - {blfs[0]}")
            try:
                test_adm = copy.deepcopy(adf)
                statements = test_adm.evaluateTree([blfs[0]])
                print(f"  ✓ Success: {len(statements)} statements generated")
                print(f"  Final case: {test_adm.case}")
            except Exception as e:
                print(f"  ✗ Error: {e}")
        
        # Test case 3: Multiple BLFs
        if len(blfs) >= 2:
            print(f"\nTest 3: Multiple BLFs - {blfs[:2]}")
            try:
                test_adm = copy.deepcopy(adf)
                statements = test_adm.evaluateTree(blfs[:2])
                print(f"  ✓ Success: {len(statements)} statements generated")
                print(f"  Final case: {test_adm.case}")
            except Exception as e:
                print(f"  ✗ Error: {e}")
        
        # Test case 4: Invalid BLF
        print(f"\nTest 4: Invalid BLF")
        try:
            test_adm = copy.deepcopy(adf)
            statements = test_adm.evaluateTree(["NON_EXISTENT"])
            print(f"  ✓ Success: {len(statements)} statements generated")
            print(f"  Final case: {test_adm.case}")
        except Exception as e:
            print(f"  ✗ Error: {e}")
        
        print(f"\n{'='*50}")
        print("Core functionality testing completed!")
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("Please ensure your ADM is properly defined and importable")
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_adm_core_functionality()

