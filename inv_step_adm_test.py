#!/usr/bin/env python3
"""
Simple Test Script for Inventive Step ADM
Just modify the case list and expected output below and run the script to evaluate the entire tree
"""

from inventive_step_ADM import adf

# =============================================================================
# MODIFY THESE LISTS TO TEST DIFFERENT SCENARIOS
# =============================================================================

# BLFs to include in the case (these will be used to evaluate the entire tree)
case_blfs = ['Contested']

# Only specify abstract factors and issues here - case_blfs will be added automatically
expected_output = []

# =============================================================================
# DON'T MODIFY BELOW THIS LINE
# =============================================================================

# Create ADM instance and set case
adm_instance = adf()
adm_instance.case = case_blfs.copy()  # Only case_blfs go into the case for evaluation

print(f"Input Case (for evaluation): {adm_instance.case}")
print(f"Expected Output (abstract factors only): {expected_output}")
print()

# Evaluate the entire tree
try:
    statements = adm_instance.evaluateTree(adm_instance.case)
    print("Evaluation Results:")
    for i, statement in enumerate(statements, 1):
        print(f"{i}. {statement}")
    
    print(f"\nFinal Case (after evaluation): {adm_instance.case}")
    
    # For comparison: combine case_blfs with expected_output
    full_expected = case_blfs + expected_output
    print(f"Expected Final Case (case_blfs + abstract factors): {full_expected}")
    
    # Compare final case with expected output
    missing = [item for item in full_expected if item not in adm_instance.case]
    extra = [item for item in adm_instance.case if item not in full_expected]
    
    if not missing and not extra:
        print("✅ Perfect match! Final case matches expected output exactly.")
    else:
        if missing:
            print(f"❌ Missing from final case: {missing}")
        if extra:
            print(f"❌ Extra in final case: {extra}")
            
except Exception as e:
    print(f"❌ Error evaluating tree: {e}")