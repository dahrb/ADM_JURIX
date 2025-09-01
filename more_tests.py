#!/usr/bin/env python3
"""
Comprehensive Test Script for Inventive Step ADM
Tests various combinations of BLFs and reports outcomes for inspection
"""

from inventive_step_ADM import adf
import itertools

def test_combination(adm_instance, case_blfs, test_num):
    """Test a specific combination of BLFs and report results"""
    print(f"\n{'='*80}")
    print(f"TEST {test_num}: {case_blfs}")
    print(f"{'='*80}")
    
    # Reset case and evaluate
    adm_instance.case = case_blfs.copy()
    
    try:
        statements = adm_instance.evaluateTree(adm_instance.case)
        
        print(f"Input BLFs: {case_blfs}")
        print(f"Final Case: {adm_instance.case}")
        print(f"Statements Generated: {len(statements)}")
        
        if statements:
            print("\nStatements:")
            for i, statement in enumerate(statements, 1):
                print(f"  {i}. {statement}")
        
        # Report what was added/removed
        added = [item for item in adm_instance.case if item not in case_blfs]
        if added:
            print(f"\nAdded to case: {added}")
        else:
            print(f"\nNothing added to case")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print(f"Input BLFs: {case_blfs}")
        print(f"Final Case: {adm_instance.case}")

def main():
    """Run comprehensive tests with different BLF combinations"""
    print("INVENTIVE STEP ADM - COMPREHENSIVE TESTING")
    print("Testing various BLF combinations to verify logic")
    
    # Create ADM instance
    adm_instance = adf()
    
    # Define all possible BLFs from the ADM
    all_blfs = [
        # Information questions (these get facts but don't affect logic)
        'INVENTION_TITLE', 'INVENTION_DESCRIPTION', 'INVENTION_TECHNICAL_FIELD', 'REL_PRIOR_ART', 'CGK',
        
        # Field-related BLFs
        'SimilarPurpose', 'SimilarEffect', 'SameField', 'SimilarField',
        
        # Documentary evidence BLFs
        'Textbook', 'TechnicalSurvey', 'PublicationNewField', 'SinglePublication',
        
        # Practitioner-related BLFs
        'Individual', 'ResearchTeam', 'ProductionTeam',
        
        # Skilled person requirements
        'SkilledIn', 'Average', 'Aware', 'Access',
        
        # Control BLFs
        'Contested'
    ]
    
    # Test 1: Empty case
    test_combination(adm_instance, [], 1)
    
    # Test 2-5: Single BLFs
    for i, blf in enumerate(['SimilarPurpose', 'SameField', 'Contested', 'Individual'], 2):
        test_combination(adm_instance, [blf], i)
    
    # Test 6-10: Pairs of related BLFs
    pairs = [
        ['SimilarPurpose', 'SameField'],
        ['Contested', 'SinglePublication'],
        ['Individual', 'SkilledIn'],
        ['SimilarPurpose', 'Contested'],
        ['SameField', 'Individual']
    ]
    
    for i, pair in enumerate(pairs, 6):
        test_combination(adm_instance, pair, i)
    
    # Test 11-15: Triplets
    triplets = [
        ['SimilarPurpose', 'SameField', 'Contested'],
        ['Individual', 'SkilledIn', 'Average'],
        ['Contested', 'SinglePublication', 'Textbook'],
        ['SimilarPurpose', 'Individual', 'Contested'],
        ['SameField', 'Contested', 'Individual']
    ]
    
    for i, triplet in enumerate(triplets, 11):
        test_combination(adm_instance, triplet, i)
    
    # Test 16-20: Complex combinations
    complex_combos = [
        ['SimilarPurpose', 'SameField', 'Contested', 'SinglePublication'],
        ['Individual', 'SkilledIn', 'Average', 'Aware', 'Access'],
        ['SimilarPurpose', 'SameField', 'Individual', 'Contested'],
        ['Contested', 'SinglePublication', 'Textbook', 'Individual'],
        ['SimilarPurpose', 'SameField', 'Contested', 'Individual', 'SkilledIn', 'Average']
    ]
    
    for i, combo in enumerate(complex_combos, 16):
        test_combination(adm_instance, combo, i)
    
    # Test 21-25: Edge cases and potential issues
    edge_cases = [
        ['SimilarPurpose', 'SimilarEffect', 'SameField', 'SimilarField'],  # All field BLFs
        ['Textbook', 'TechnicalSurvey', 'PublicationNewField', 'SinglePublication'],  # All evidence BLFs
        ['Individual', 'ResearchTeam', 'ProductionTeam'],  # All practitioner types
        ['SkilledIn', 'Average', 'Aware', 'Access'],  # All skilled person requirements
        ['Contested', 'SimilarPurpose', 'SameField', 'Individual', 'SkilledIn', 'Average', 'Aware', 'Access']  # Everything
    ]
    
    for i, edge_case in enumerate(edge_cases, 21):
        test_combination(adm_instance, edge_case, i)
    
    print(f"\n{'='*80}")
    print("TESTING COMPLETE")
    print(f"{'='*80}")
    print(f"Total tests run: 25")
    print("Check the outputs above for any unexpected behavior, errors, or logic issues")

if __name__ == "__main__":
    main()