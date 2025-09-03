#!/usr/bin/env python3
"""
Unit tests for both sub-ADM and main ADM evaluation with expected final cases
"""

import unittest
from MainClasses import *
from inventive_step_ADM import create_sub_adm_prior_art, adf

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


class TestMainADMEvaluation(unittest.TestCase):
    """Unit tests for main ADM evaluation"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.main_adf = adf()
    
    def evaluate_blf_combination(self, blf_list, information_responses=None):
        """Helper method to evaluate a combination of BLFs using the tree evaluation algorithm"""
        # Start with empty case
        self.main_adf.case = []
        
        # Add information responses if provided
        if information_responses:
            for key, value in information_responses.items():
                self.main_adf.case.append(key)
                # Store the information in the ADF for placeholder resolution
                if not hasattr(self.main_adf, 'information'):
                    self.main_adf.information = {}
                self.main_adf.information[key] = value
        
        # Add the BLFs to the case
        for blf in blf_list:
            if blf not in self.main_adf.case:
                self.main_adf.case.append(blf)
        
        # Use the existing tree evaluation algorithm
        self.main_adf.evaluateTree(self.main_adf.case)
        
        return self.main_adf.case.copy()
    
    def assert_final_case(self, test_name, blf_list, expected_final_case, information_responses=None):
        """Helper method to test and display final case results"""
        actual_final_case = self.evaluate_blf_combination(blf_list, information_responses)
        
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
            if information_responses:
                print(f"Information: {information_responses}")
            print(f"Expected: {sorted(expected_final_case)}")
            print(f"Actual:   {sorted(actual_final_case)}")
            raise
    
    def test_basic_skilled_person_establishment(self):
        """Test: Basic skilled person establishment"""
        blf_list = ["Individual", "SkilledIn", "Average", "Aware", "Access"]
        information_responses = {
            "INVENTION_TITLE": "Test Invention",
            "INVENTION_DESCRIPTION": "A test invention for evaluation",
            "INVENTION_TECHNICAL_FIELD": "Computer Science",
            "REL_PRIOR_ART": "Prior art in computer science",
            "CGK": "Common knowledge in computer science"
        }
        expected_final_case = [
            "INVENTION_TITLE", "INVENTION_DESCRIPTION", "INVENTION_TECHNICAL_FIELD", 
            "REL_PRIOR_ART", "CGK", "Individual", "SkilledIn", "Average", 
            "Aware", "Access", "Person", "SkilledPerson"
        ]
        
        self.assert_final_case("Basic Skilled Person Establishment", blf_list, expected_final_case, information_responses)
    
    def test_relevant_prior_art_same_field(self):
        """Test: Relevant prior art from same field"""
        blf_list = ["SameField", "SimilarPurpose", "SimilarEffect"]
        information_responses = {
            "INVENTION_TITLE": "Test Invention",
            "INVENTION_DESCRIPTION": "A test invention",
            "INVENTION_TECHNICAL_FIELD": "Computer Science",
            "REL_PRIOR_ART": "Prior art in computer science"
        }
        expected_final_case = [
            "INVENTION_TITLE", "INVENTION_DESCRIPTION", "INVENTION_TECHNICAL_FIELD", 
            "REL_PRIOR_ART", "SameField", "SimilarPurpose", "SimilarEffect", 
            "RelevantPriorArt"
        ]
        
        self.assert_final_case("Relevant Prior Art Same Field", blf_list, expected_final_case, information_responses)
    
    def test_common_knowledge_with_textbook_evidence(self):
        """Test: Common knowledge with textbook evidence"""
        blf_list = ["Textbook"]
        information_responses = {
            "INVENTION_TITLE": "Test Invention",
            "INVENTION_DESCRIPTION": "A test invention",
            "INVENTION_TECHNICAL_FIELD": "Computer Science",
            "REL_PRIOR_ART": "Prior art in computer science",
            "CGK": "Common knowledge in computer science"
        }
        expected_final_case = [
            "INVENTION_TITLE", "INVENTION_DESCRIPTION", "INVENTION_TECHNICAL_FIELD", 
            "REL_PRIOR_ART", "CGK", "Textbook", "DocumentaryEvidence", 
            "CommonKnowledge"
        ]
        
        self.assert_final_case("Common Knowledge with Textbook Evidence", blf_list, expected_final_case, information_responses)
    
    def test_common_knowledge_contested(self):
        """Test: Common knowledge contested"""
        blf_list = ["Contested"]
        information_responses = {
            "INVENTION_TITLE": "Test Invention",
            "INVENTION_DESCRIPTION": "A test invention",
            "INVENTION_TECHNICAL_FIELD": "Computer Science",
            "REL_PRIOR_ART": "Prior art in computer science",
            "CGK": "Common knowledge in computer science"
        }
        expected_final_case = [
            "INVENTION_TITLE", "INVENTION_DESCRIPTION", "INVENTION_TECHNICAL_FIELD", 
            "REL_PRIOR_ART", "CGK", "Contested"
        ]
        
        self.assert_final_case("Common Knowledge Contested", blf_list, expected_final_case, information_responses)
    
    def test_closest_prior_art_single_reference(self):
        """Test: Closest prior art as single reference"""
        blf_list = ["SingleReference", "MinModifications", "AssessedBy"]
        information_responses = {
            "INVENTION_TITLE": "Test Invention",
            "INVENTION_DESCRIPTION": "A test invention",
            "INVENTION_TECHNICAL_FIELD": "Computer Science",
            "REL_PRIOR_ART": "Prior art in computer science",
            "CGK": "Common knowledge in computer science",
            "CPA": "Closest prior art document"
        }
        expected_final_case = [
            "INVENTION_TITLE", "INVENTION_DESCRIPTION", "INVENTION_TECHNICAL_FIELD", 
            "REL_PRIOR_ART", "CGK", "SingleReference", "MinModifications", 
            "AssessedBy"
        ]
        
        self.assert_final_case("Closest Prior Art Single Reference", blf_list, expected_final_case, information_responses)
    
    def test_combination_attempt_same_field(self):
        """Test: Combination attempt with same field documents"""
        blf_list = ["CombinationAttempt", "SameFieldCPA", "CombinationMotive", "BasisToAssociate"]
        information_responses = {
            "INVENTION_TITLE": "Test Invention",
            "INVENTION_DESCRIPTION": "A test invention",
            "INVENTION_TECHNICAL_FIELD": "Computer Science",
            "REL_PRIOR_ART": "Prior art in computer science",
            "CGK": "Common knowledge in computer science",
            "CPA": "Closest prior art document"
        }
        expected_final_case = [
            "INVENTION_TITLE", "INVENTION_DESCRIPTION", "INVENTION_TECHNICAL_FIELD", 
            "REL_PRIOR_ART", "CGK", "CombinationAttempt", "SameFieldCPA", 
            "CombinationMotive", "BasisToAssociate", "CombinationDocuments"
        ]
        
        self.assert_final_case("Combination Attempt Same Field", blf_list, expected_final_case, information_responses)
    
    def test_complex_scenario_with_all_factors(self):
        """Test: Complex scenario with all major factors"""
        blf_list = [
            "Individual", "SkilledIn", "Average", "Aware", "Access",
            "SameField", "SimilarPurpose", "SimilarEffect",
            "Textbook", "SingleReference", "MinModifications", "AssessedBy",
            "CombinationAttempt", "SameFieldCPA", "CombinationMotive", "BasisToAssociate"
        ]
        information_responses = {
            "INVENTION_TITLE": "Advanced Test Invention",
            "INVENTION_DESCRIPTION": "A complex test invention for comprehensive evaluation",
            "INVENTION_TECHNICAL_FIELD": "Computer Science",
            "REL_PRIOR_ART": "Prior art in computer science",
            "CGK": "Common knowledge in computer science",
            "CPA": "Closest prior art document"
        }
        expected_final_case = [
            "INVENTION_TITLE", "INVENTION_DESCRIPTION", "INVENTION_TECHNICAL_FIELD", 
            "REL_PRIOR_ART", "CGK", "Individual", "SkilledIn", "Average", 
            "Aware", "Access", "Person", "SkilledPerson", "SameField", 
            "SimilarPurpose", "SimilarEffect", "RelevantPriorArt", "Textbook", 
            "DocumentaryEvidence", "CommonKnowledge", "SingleReference", 
            "MinModifications", "AssessedBy", "ClosestPriorArt", "CombinationAttempt", 
            "SameFieldCPA", "CombinationMotive", "BasisToAssociate", 
            "CombinationDocuments", "ClosestPriorArtDocuments"
        ]
        
        self.assert_final_case("Complex Scenario with All Factors", blf_list, expected_final_case, information_responses)
    
    def test_research_team_skilled_person(self):
        """Test: Research team as skilled person"""
        blf_list = ["ResearchTeam", "SkilledIn", "Average", "Aware", "Access"]
        information_responses = {
            "INVENTION_TITLE": "Test Invention",
            "INVENTION_DESCRIPTION": "A test invention",
            "INVENTION_TECHNICAL_FIELD": "Computer Science",
            "REL_PRIOR_ART": "Prior art in computer science",
            "CGK": "Common knowledge in computer science"
        }
        expected_final_case = [
            "INVENTION_TITLE", "INVENTION_DESCRIPTION", "INVENTION_TECHNICAL_FIELD", 
            "REL_PRIOR_ART", "CGK", "ResearchTeam", "SkilledIn", "Average", 
            "Aware", "Access", "Person", "SkilledPerson"
        ]
        
        self.assert_final_case("Research Team Skilled Person", blf_list, expected_final_case, information_responses)
    
    def test_technical_survey_evidence(self):
        """Test: Technical survey as documentary evidence"""
        blf_list = ["TechnicalSurvey"]
        information_responses = {
            "INVENTION_TITLE": "Test Invention",
            "INVENTION_DESCRIPTION": "A test invention",
            "INVENTION_TECHNICAL_FIELD": "Computer Science",
            "REL_PRIOR_ART": "Prior art in computer science",
            "CGK": "Common knowledge in computer science"
        }
        expected_final_case = [
            "INVENTION_TITLE", "INVENTION_DESCRIPTION", "INVENTION_TECHNICAL_FIELD", 
            "REL_PRIOR_ART", "CGK", "TechnicalSurvey", "DocumentaryEvidence", 
            "CommonKnowledge"
        ]
        
        self.assert_final_case("Technical Survey Evidence", blf_list, expected_final_case, information_responses)
    
    def test_combination_attempt_similar_field(self):
        """Test: Combination attempt with similar field documents"""
        blf_list = ["CombinationAttempt", "SimilarFieldCPA", "CombinationMotive", "BasisToAssociate"]
        information_responses = {
            "INVENTION_TITLE": "Test Invention",
            "INVENTION_DESCRIPTION": "A test invention",
            "INVENTION_TECHNICAL_FIELD": "Computer Science",
            "REL_PRIOR_ART": "Prior art in computer science",
            "CGK": "Common knowledge in computer science",
            "CPA": "Closest prior art document"
        }
        expected_final_case = [
            "INVENTION_TITLE", "INVENTION_DESCRIPTION", "INVENTION_TECHNICAL_FIELD", 
            "REL_PRIOR_ART", "CGK", "CombinationAttempt", "SimilarFieldCPA", 
            "CombinationMotive", "BasisToAssociate", "CombinationDocuments"
        ]
        
        self.assert_final_case("Combination Attempt Similar Field", blf_list, expected_final_case, information_responses)
    
    def test_production_team_skilled_person(self):
        """Test: Production team as skilled person"""
        blf_list = ["ProductionTeam", "SkilledIn", "Average", "Aware", "Access"]
        information_responses = {
            "INVENTION_TITLE": "Test Invention",
            "INVENTION_DESCRIPTION": "A test invention",
            "INVENTION_TECHNICAL_FIELD": "Computer Science",
            "REL_PRIOR_ART": "Prior art in computer science",
            "CGK": "Common knowledge in computer science"
        }
        expected_final_case = [
            "INVENTION_TITLE", "INVENTION_DESCRIPTION", "INVENTION_TECHNICAL_FIELD", 
            "REL_PRIOR_ART", "CGK", "ProductionTeam", "SkilledIn", "Average", 
            "Aware", "Access", "Person", "SkilledPerson"
        ]
        
        self.assert_final_case("Production Team Skilled Person", blf_list, expected_final_case, information_responses)
    
    def test_publication_new_field_evidence(self):
        """Test: Publication in new field as documentary evidence"""
        blf_list = ["PublicationNewField"]
        information_responses = {
            "INVENTION_TITLE": "Test Invention",
            "INVENTION_DESCRIPTION": "A test invention",
            "INVENTION_TECHNICAL_FIELD": "Computer Science",
            "REL_PRIOR_ART": "Prior art in computer science",
            "CGK": "Common knowledge in computer science"
        }
        expected_final_case = [
            "INVENTION_TITLE", "INVENTION_DESCRIPTION", "INVENTION_TECHNICAL_FIELD", 
            "REL_PRIOR_ART", "CGK", "PublicationNewField", "DocumentaryEvidence", 
            "CommonKnowledge"
        ]
        
        self.assert_final_case("Publication New Field Evidence", blf_list, expected_final_case, information_responses)
    
    def test_minimal_case_information_only(self):
        """Test: Minimal case with only information questions"""
        blf_list = []
        information_responses = {
            "INVENTION_TITLE": "Test Invention",
            "INVENTION_DESCRIPTION": "A test invention",
            "INVENTION_TECHNICAL_FIELD": "Computer Science",
            "REL_PRIOR_ART": "Prior art in computer science",
            "CGK": "Common knowledge in computer science"
        }
        expected_final_case = [
            "INVENTION_TITLE", "INVENTION_DESCRIPTION", "INVENTION_TECHNICAL_FIELD", 
            "REL_PRIOR_ART", "CGK"
        ]
        
        self.assert_final_case("Minimal Case Information Only", blf_list, expected_final_case, information_responses)


def run_all_tests():
    """Run all unit tests (both sub-ADM and main ADM)"""
    print("Running All ADM Unit Tests...")
    print("="*60)
    
    # Create test suite for both test classes
    suite = unittest.TestSuite()
    
    # Add sub-ADM tests
    sub_adm_suite = unittest.TestLoader().loadTestsFromTestCase(TestSubADMEvaluation)
    suite.addTest(sub_adm_suite)
    
    # Add main ADM tests
    main_adm_suite = unittest.TestLoader().loadTestsFromTestCase(TestMainADMEvaluation)
    suite.addTest(main_adm_suite)
    
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


def run_sub_adm_tests():
    """Run only sub-ADM unit tests"""
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


def run_main_adm_tests():
    """Run only main ADM unit tests"""
    print("Running Main ADM Unit Tests...")
    print("="*60)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMainADMEvaluation)
    
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
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "sub":
            run_sub_adm_tests()
        elif sys.argv[1] == "main":
            run_main_adm_tests()
        else:
            print("Usage: python test_adm_unit.py [sub|main]")
            print("  sub  - Run only sub-ADM tests")
            print("  main - Run only main ADM tests")
            print("  (no args) - Run all tests")
    else:
        run_all_tests()
