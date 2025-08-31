#!/usr/bin/env python3
"""
Test Script for Inventive Step ADM
"""

from inventive_step_ADM import adf
from test_adm import ADMTester

def main():
    """Test the inventive step ADM"""
    print("Testing Inventive Step ADM")
    print("=" * 50)
    
    # Create tester instance
    tester = ADMTester(adf)
    
    # Analyze acceptance conditions
    tester.analyze_acceptance_conditions()
    
    # Run edge case tests
    tester.run_edge_case_tests()
    
    # Run random tests
    tester.run_multiple_tests(num_tests=10, complexity_range=(2, 4))
    
    print(f"\n{'='*80}")
    print(f"INVENTIVE STEP ADM TESTING COMPLETED")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
