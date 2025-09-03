#!/usr/bin/env python3
"""
Unit tests for sub-ADM evaluation with expected final cases
"""

import unittest
from MainClasses import *
from inventive_step_ADM import create_sub_adm_prior_art

class TestSubADMEvaluation(unittest.TestCase):
    """Unit tests for sub-ADM evaluation"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sub_adf = create_sub_adm_prior_art("test_feature")
    
    def evaluate_blf_combination(self, blf_list):
        """Helper method to evaluate a combination of BLFs using the tree evaluation algorithm"""
        # Start with base case
        self.sub_adf.case = ["DistinguishingFeatures"]
        
        # Add the BLFs to the case
        for blf in blf_list:
            if blf not in self.sub_adf.case:
                self.sub_adf.case.append(blf)
        
        # Use the existing tree evaluation algorithm
        self.sub_adf.evaluateTree(self.sub_adf.case)
        
        return self.sub_adf.case.copy()
    
    def assert_final_case(self, test_name, blf_list, expected_final_case):
        """Helper method to test and display final case results"""
        actual_final_case = self.evaluate_blf_combination(blf_list)
        
        # Only show output for failures
        try:
            self.assertEqual(
                set(actual_final_case), 
                set(expected_final_case),
                f"Expected: {expected_final_case}, Got: {actual_final_case}"
            )
        except AssertionError:
            # Show both cases for failures only
            print(f"\nTest: {test_name}")
            print(f"BLFs: {blf_list}")
            print(f"Expected: {sorted(expected_final_case)}")
            print(f"Actual:   {sorted(actual_final_case)}")
            raise
    
    def test_independent_contribution_only(self):
        """Test: Independent Contribution Only"""
        blf_list = ["IndependentContribution"]
        expected_final_case = [
            "DistinguishingFeatures", 
            "IndependentContribution", 
            "NonReproducible",
            "NormalTechnicalContribution", 
            "FeatureTechnicalContribution"
        ]
        
        self.assert_final_case("Independent Contribution Only", blf_list, expected_final_case)
    
    def test_combination_contribution_only(self):
        """Test: Combination Contribution Only"""
        blf_list = ["CombinationContribution"]
        expected_final_case = [
            "DistinguishingFeatures", 
            "CombinationContribution", 
            "NonReproducible",
            "NormalTechnicalContribution", 
            "FeatureTechnicalContribution"
        ]
        
        self.assert_final_case("Combination Contribution Only", blf_list, expected_final_case)
    
    def test_independent_with_circumvent_tech_problem(self):
        """Test: Independent Contribution + CircumventTechProblem (should be rejected)"""
        blf_list = ["IndependentContribution", "CircumventTechProblem"]
        expected_final_case = [
            "DistinguishingFeatures", 
            "IndependentContribution", 
            "NonReproducible",
            "CircumventTechProblem"
        ]
        
        self.assert_final_case("Independent + CircumventTechProblem (rejected)", blf_list, expected_final_case)
    
    def test_independent_with_excluded_field(self):
        """Test: Independent Contribution + Excluded Field (should be rejected)"""
        blf_list = ["IndependentContribution", "ComputerSimulation"]
        expected_final_case = [
            "ExcludedField",
            "NumOrComp",
            "DistinguishingFeatures", 
            "IndependentContribution", 
            "NonReproducible",
            "ComputerSimulation"
        ]
        
        self.assert_final_case("Independent + Excluded Field (rejected)", blf_list, expected_final_case)
    
    def test_computer_simulation_with_technical_adaptation(self):
        """Test: Computer Simulation + Technical Adaptation"""
        blf_list = ["ComputerSimulation", "TechnicalAdaptation"]
        expected_final_case = [
            "DistinguishingFeatures", 
            "NonReproducible",
            "ComputerSimulation", 
            "ExcludedField",
            "NumOrComp",
            "TechnicalAdaptation", 
            "ComputationalContribution", 
            "FeatureTechnicalContribution"
        ]
        
        self.assert_final_case("Computer Simulation + Technical Adaptation", blf_list, expected_final_case)
    
    def test_mathematical_method_with_specific_purpose(self):
        """Test: Mathematical Method + Specific Purpose + Functionally Limited"""
        blf_list = ["MathematicalMethod", "SpecificPurpose", "FunctionallyLimited"]
        expected_final_case = [
            "DistinguishingFeatures", 
            "NonReproducible",
            "MathematicalMethod", 
            "ExcludedField",
            "SpecificPurpose", 
            "FunctionallyLimited", 
            "AppliedInField", 
            "MathematicalContribution", 
            "FeatureTechnicalContribution"
        ]
        
        self.assert_final_case("Mathematical Method + Specific Purpose + Functionally Limited", blf_list, expected_final_case)
    
    def test_independent_with_unexpected_effect(self):
        """Test: Independent Contribution + Unexpected Effect + Precise Terms + One Way Street"""
        blf_list = ["IndependentContribution", "UnexpectedEffect", "PreciseTerms", "OneWayStreet"]
        expected_final_case = [
            "DistinguishingFeatures", 
            "IndependentContribution", 
            "NonReproducible",
            "NormalTechnicalContribution", 
            "FeatureTechnicalContribution", 
            "UnexpectedEffect", 
            "PreciseTerms", 
            "OneWayStreet", 
            "BonusEffect"
        ]
        
        self.assert_final_case("Independent + Unexpected Effect + Precise Terms + One Way Street", blf_list, expected_final_case)
    
    def test_independent_with_credible_reproducible(self):
        """Test: Independent Contribution + Credible + Reproducible"""
        blf_list = ["IndependentContribution", "Credible", "Reproducible"]
        expected_final_case = [
            "DistinguishingFeatures", 
            "IndependentContribution", 
            "NormalTechnicalContribution", 
            "FeatureTechnicalContribution", 
            "Credible", 
            "Reproducible", 
            "ReliableTechnicalEffect"
        ]
        
        self.assert_final_case("Independent + Credible + Reproducible", blf_list, expected_final_case)

    def test_independent_with_unexpected_effect(self):
        """Test: Independent Contribution + Unexpected Effect + Precise Terms + One Way Street"""
        blf_list = ["IndependentContribution", "UnexpectedEffect", "PreciseTerms", "OneWayStreet"]
        expected_final_case = [
            "DistinguishingFeatures", 
            "IndependentContribution", 
            "NonReproducible",
            "NormalTechnicalContribution", 
            "FeatureTechnicalContribution", 
            "UnexpectedEffect", 
            "PreciseTerms", 
            "OneWayStreet", 
            "BonusEffect"
        ]
        
        self.assert_final_case("Independent + Unexpected Effect + Precise Terms + One Way Street", blf_list, expected_final_case)
      
    
    def test_complex_all_positive(self):
        """Test: Complex scenario with all positive factors"""
        blf_list = ["IndependentContribution", "ComputerSimulation", "TechnicalAdaptation", "Credible", "Reproducible"]
        expected_final_case = [
            "DistinguishingFeatures", 
            "IndependentContribution", 
            "ExcludedField",
            "NumOrComp",
            "ComputerSimulation", 
            "TechnicalAdaptation", 
            "Credible", 
            "Reproducible", 
            "ComputationalContribution", 
            "FeatureTechnicalContribution", 
            "ReliableTechnicalEffect"
        ]
        
        self.assert_final_case("Complex All Positive Factors", blf_list, expected_final_case)
    
    def test_complex_mixed_with_reject(self):
        """Test: Complex scenario with reject conditions"""
        blf_list = ["IndependentContribution", "CircumventTechProblem", "Credible", "Reproducible"]
        expected_final_case = [
            "DistinguishingFeatures", 
            "IndependentContribution", 
            "CircumventTechProblem", 
            "Credible", 
            "Reproducible"
            # NormalTechnicalContribution should NOT be added due to CircumventTechProblem
        ]
        
        self.assert_final_case("Complex Mixed with Reject", blf_list, expected_final_case)
    
    def test_no_blfs(self):
        """Test: No BLFs (edge case)"""
        blf_list = ["DistinguishingFeatures"]
        expected_final_case = [
            "DistinguishingFeatures",
            "NonReproducible"
        ]
        
        self.assert_final_case("No BLFs (Base Case Only)", blf_list, expected_final_case)
    
    def test_only_excluded_field(self):
        """Test: Only Excluded Field"""
        blf_list = ["ExcludedField"]
        expected_final_case = [
            "DistinguishingFeatures", 
            "ExcludedField",
            "NonReproducible"
        ]
        
        self.assert_final_case("Only Excluded Field", blf_list, expected_final_case)
    
    def test_only_circumvent_tech_problem(self):
        """Test: Only CircumventTechProblem"""
        blf_list = ["CircumventTechProblem"]
        expected_final_case = [
            "DistinguishingFeatures", 
            "CircumventTechProblem",
            "NonReproducible"
        ]
        
        self.assert_final_case("Only Circumvent Tech Problem", blf_list, expected_final_case)

def run_tests():
    """Run the unit tests"""
    print("Running Sub-ADM Unit Tests...")
    print("="*60)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSubADMEvaluation)
    
    # Run tests with minimal verbosity
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFAILURES:")
        for test, traceback in result.failures:
            # Extract the detailed error message
            lines = traceback.split('\n')
            for line in lines:
                if 'Expected:' in line and 'Got:' in line:
                    print(f"  - {test}: {line}")
                    break
            else:
                # Fallback to original error message
                error_msg = traceback.split('AssertionError: ')[-1].split('\n')[0]
                print(f"  - {test}: {error_msg}")
    
    if result.errors:
        print(f"\nERRORS:")
        for test, traceback in result.errors:
            error_msg = traceback.split('\n')[-2]
            print(f"  - {test}: {error_msg}")
    
    return result

if __name__ == "__main__":
    run_tests()
