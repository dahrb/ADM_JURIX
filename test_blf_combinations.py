#!/usr/bin/env python3
"""
Simple test to show final case results for different BLF combinations in sub-ADM
"""

from MainClasses import *
from inventive_step_ADM import create_sub_adm_prior_art

def test_blf_combination(combination_name, blf_list):
    """Test a specific combination of BLFs"""
    print(f"\n{'='*60}")
    print(f"Testing: {combination_name}")
    print(f"BLFs: {blf_list}")
    
    # Create sub-ADM
    sub_adf = create_sub_adm_prior_art("test_feature")
    
    # Start with base case
    sub_adf.case = ["DistinguishingFeatures"]
    
    # Add the BLFs to the case
    for blf in blf_list:
        if blf not in sub_adf.case:
            sub_adf.case.append(blf)
    
    print(f"Initial case: {sub_adf.case}")
    
    # Find abstract factors (nodes with children)
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
            print(f"\nEvaluating {factor} (children: {node.children})")
            
            # Check if all children are in case
            if all(child in sub_adf.case for child in node.children):
                print(f"  All children present, evaluating...")
                result = sub_adf.evaluateNode(node)
                print(f"  Result: {result}, Reject: {sub_adf.reject}")
                
                if result and not sub_adf.reject:
                    sub_adf.case.append(factor)
                    print(f"  ✅ Added {factor} to case")
                else:
                    print(f"  ❌ Did not add {factor} to case")
            else:
                missing = [child for child in node.children if child not in sub_adf.case]
                print(f"  ⚠️  Cannot evaluate - missing children: {missing}")
    
    print(f"\nFINAL CASE: {sub_adf.case}")
    
    # Determine result
    accepted_abstract = [f for f in abstract_factors if f in sub_adf.case]
    if accepted_abstract:
        root_node = accepted_abstract[-1]
        result = "ACCEPTED"
    else:
        root_node = None
        result = "REJECTED"
    
    print(f"Root node: {root_node}")
    print(f"Result: {result}")
    
    return sub_adf.case, result

def main():
    """Test different BLF combinations"""
    print("Testing Different BLF Combinations in Sub-ADM")
    
    # Define test combinations
    combinations = [
        ("Independent Contribution Only", ["IndependentContribution"]),
        ("Combination Contribution Only", ["CombinationContribution"]),
        ("Independent + CircumventTechProblem", ["IndependentContribution", "CircumventTechProblem"]),
        ("Independent + ExcludedField", ["IndependentContribution", "ComputerSimulation"]),
        ("Computer Simulation + Technical Adaptation", ["ComputerSimulation", "TechnicalAdaptation"]),
        ("Mathematical Method + Specific Purpose", ["MathematicalMethod", "SpecificPurpose", "FunctionallyLimited"]),
        ("Independent + Unexpected Effect", ["IndependentContribution", "UnexpectedEffect", "PreciseTerms", "OneWayStreet"]),
        ("Independent + Credible + Reproducible", ["IndependentContribution", "Credible", "Reproducible"]),
        ("Complex: All Positive", ["IndependentContribution", "ComputerSimulation", "TechnicalAdaptation", "Credible", "Reproducible"]),
        ("Complex: Mixed with Reject", ["IndependentContribution", "CircumventTechProblem", "Credible", "Reproducible"]),
        ("No BLFs", []),
        ("Only Excluded Field", ["OtherExclusions"]),
        ("Only CircumventTechProblem", ["CircumventTechProblem"])
    ]
    
    results = []
    
    for combo_name, blf_list in combinations:
        final_case, result = test_blf_combination(combo_name, blf_list)
        results.append((combo_name, blf_list, final_case, result))
    
    # Summary
    print(f"\n{'='*80}")
    print("SUMMARY OF ALL COMBINATIONS")
    print(f"{'='*80}")
    print(f"{'Combination':<40} {'Result':<10} {'Final Case'}")
    print(f"{'-'*80}")
    
    for combo_name, blf_list, final_case, result in results:
        case_str = str(final_case)[:30] + "..." if len(str(final_case)) > 30 else str(final_case)
        print(f"{combo_name:<40} {result:<10} {case_str}")

if __name__ == "__main__":
    main()
