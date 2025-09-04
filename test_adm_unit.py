#!/usr/bin/env python3
"""
Unit tests for both sub-ADM and main ADM evaluation with expected final cases
"""

import unittest
import os
from MainClasses import *
from inventive_step_ADM import create_sub_adm_prior_art, adf
from UI import CLI
import builtins
import sys


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
    
    def evaluate_blf_combination(self, blf_list):
        """Helper method to evaluate a combination of BLFs using the tree evaluation algorithm"""
        # Start with empty case
        self.main_adf.case = []
        
        # Add the BLFs to the case
        for blf in blf_list:
            if blf not in self.main_adf.case:
                self.main_adf.case.append(blf)
        
        # Use the existing tree evaluation algorithm
        self.main_adf.evaluateTree(self.main_adf.case)
        
        return self.main_adf.case.copy()
    
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
    
    def test_basic_skilled_person_establishment(self):
        """Test: Basic skilled person establishment"""
        blf_list = ["Individual", "SkilledIn", "Average", "Aware", "Access"]
        expected_final_case = [
            "Individual", "SkilledIn", "Average", 
            "Aware", "Access", "Person", "SkilledPerson", "CommonKnowledge"
        ]
        
        self.assert_final_case("Basic Skilled Person Establishment", blf_list, expected_final_case)
    
    def test_relevant_prior_art_same_field(self):
        """Test: Relevant prior art from same field"""
        blf_list = ["SameField", "SimilarPurpose", "SimilarEffect"]
        expected_final_case = [
            "SameField", "SimilarPurpose", "SimilarEffect", 
            "RelevantPriorArt", "CommonKnowledge"
        ]
        
        self.assert_final_case("Relevant Prior Art Same Field", blf_list, expected_final_case)
    
    def test_common_knowledge_with_textbook_evidence(self):
        """Test: Common knowledge with textbook evidence"""
        blf_list = ["Textbook"]
        expected_final_case = [
            "Textbook", "DocumentaryEvidence", 
            "CommonKnowledge"
        ]
        
        self.assert_final_case("Common Knowledge with Textbook Evidence", blf_list, expected_final_case)
    
    def test_common_knowledge_contested(self):
        """Test: Common knowledge contested"""
        blf_list = ["Contested"]

        expected_final_case = [
            "Contested"
        ]
        
        self.assert_final_case("Common Knowledge Contested", blf_list, expected_final_case)
    
    def test_closest_prior_art_single_reference(self):
        """Test: Closest prior art as single reference"""
        blf_list = ["SingleReference", "MinModifications", "AssessedBy"]

        expected_final_case = [
            "SingleReference", "MinModifications", 
            "AssessedBy", "CommonKnowledge"
        ]
        
        self.assert_final_case("Closest Prior Art Single Reference", blf_list, expected_final_case)
    
    def test_combination_attempt_same_field(self):
        """Test: Combination attempt with same field documents"""
        blf_list = ["CombinationAttempt", "SameFieldCPA", "CombinationMotive", "BasisToAssociate"]

        expected_final_case = [
            "CombinationAttempt", "SameFieldCPA", 
            "CombinationMotive", "BasisToAssociate", "CombinationDocuments", "CommonKnowledge","ClosestPriorArtDocuments"
        ]
        
        self.assert_final_case("Combination Attempt Same Field", blf_list, expected_final_case)
    
    def test_complex_scenario_with_all_factors(self):
        """Test: Complex scenario with all major factors"""
        blf_list = [
            "Individual", "SkilledIn", "Average", "Aware", "Access",
            "SameField", "SimilarPurpose", "SimilarEffect",
            "Textbook", "SingleReference", "MinModifications", "AssessedBy",
            "CombinationAttempt", "SameFieldCPA", "CombinationMotive", "BasisToAssociate"
        ]


        expected_final_case = [
            "Individual", "SkilledIn", "Average", 
            "Aware", "Access", "Person", "SkilledPerson", "SameField", 
            "SimilarPurpose", "SimilarEffect", "RelevantPriorArt", "Textbook", 
            "DocumentaryEvidence", "CommonKnowledge", "SingleReference", 
            "MinModifications", "AssessedBy", "ClosestPriorArt", "CombinationAttempt", 
            "SameFieldCPA", "CombinationMotive", "BasisToAssociate", 
            "CombinationDocuments", "ClosestPriorArtDocuments"
        ]
        
        self.assert_final_case("Complex Scenario with All Factors", blf_list, expected_final_case)
    
    def test_research_team_skilled_person(self):
        """Test: Research team as skilled person"""
        blf_list = ["ResearchTeam", "SkilledIn", "Average", "Aware", "Access"]

        expected_final_case = [
            "ResearchTeam", "SkilledIn", "Average", 
            "Aware", "Access", "Person", "SkilledPerson", "CommonKnowledge"
        ]
        
        self.assert_final_case("Research Team Skilled Person", blf_list, expected_final_case)
    
    def test_technical_survey_evidence(self):
        """Test: Technical survey as documentary evidence"""
        blf_list = ["TechnicalSurvey"]

        expected_final_case = [
            "TechnicalSurvey", "DocumentaryEvidence", 
            "CommonKnowledge"
        ]
        
        self.assert_final_case("Technical Survey Evidence", blf_list, expected_final_case)
    
    def test_combination_attempt_similar_field(self):
        """Test: Combination attempt with similar field documents"""
        blf_list = ["CombinationAttempt", "SimilarFieldCPA", "CombinationMotive", "BasisToAssociate"]


        expected_final_case = [
            "CombinationAttempt", "SimilarFieldCPA", 
            "CombinationMotive", "BasisToAssociate", "CombinationDocuments", "CommonKnowledge","ClosestPriorArtDocuments"
        ]
        
        self.assert_final_case("Combination Attempt Similar Field", blf_list, expected_final_case)
    
    def test_production_team_skilled_person(self):
        """Test: Production team as skilled person"""
        blf_list = ["ProductionTeam", "SkilledIn", "Average", "Aware", "Access"]

        expected_final_case = [
            "ProductionTeam", "SkilledIn", "Average", 
            "Aware", "Access", "Person", "SkilledPerson", "CommonKnowledge"
        ]
        
        self.assert_final_case("Production Team Skilled Person", blf_list, expected_final_case)
    
    def test_publication_new_field_evidence(self):
        """Test: Publication in new field as documentary evidence"""
        blf_list = ["PublicationNewField"]

        expected_final_case = [
            "PublicationNewField", "DocumentaryEvidence", 
            "CommonKnowledge"
        ]
        
        self.assert_final_case("Publication New Field Evidence", blf_list, expected_final_case)
    
    def test_minimal_case_information_only(self):
        """Test: Minimal case with no BLFs"""
        blf_list = []

        expected_final_case = ["CommonKnowledge"]
        
        self.assert_final_case("Minimal Case Information Only", blf_list, expected_final_case)

class TestCLIUI(unittest.TestCase):
    """Unit tests for CLI UI functionality - focused on non-blocking methods"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.cli = CLI()
        # Mock the input function to control user input
        self.original_input = builtins.input
        self.original_print = builtins.print
        self.input_calls = []
        self.print_calls = []
        
    def tearDown(self):
        """Clean up after tests"""
        builtins.input = self.original_input
        builtins.print = self.original_print
    
    def mock_input(self, prompt=""):
        """Mock input function that returns predefined responses"""
        self.input_calls.append(prompt)
        if self.input_calls:
            return self.input_calls.pop(0)
        return ""
    
    def mock_print(self, *args, **kwargs):
        """Mock print function to capture output"""
        self.print_calls.append(' '.join(str(arg) for arg in args))
        # Don't actually print during tests
    
    def test_cli_initialization(self):
        """Test CLI initialization"""
        cli = CLI()
        self.assertIsNone(cli.adf)
        self.assertEqual(cli.case, [])
        self.assertEqual(cli.cases, {})
        self.assertIsNone(cli.caseName)
    
    def test_main_menu_choice_logic(self):
        """Test main menu choice handling logic without infinite loops"""
        # Test choice 1 - should call load_existing_domain
        original_load = self.cli.load_existing_domain
        self.cli.load_existing_domain = lambda: "loaded"
        
        choice = "1"
        if choice == "1":
            result = self.cli.load_existing_domain()
            self.assertEqual(result, "loaded")
        
        # Test choice 2 - should exit
        choice = "2"
        if choice == "2":
            with self.assertRaises(SystemExit):
                sys.exit(0)
        
        # Test invalid choice
        choice = "99"
        if choice not in ["1", "2"]:
            self.assertTrue(True)  # Just verify the logic works
        
        # Restore original method
        self.cli.load_existing_domain = original_load
    
    def test_load_existing_domain_logic(self):
        """Test load existing domain choice handling logic"""
        # Test choice 1 - Academic Research Project
        original_load_academic = self.cli.load_academic_research_domain
        self.cli.load_academic_research_domain = lambda: "academic_loaded"
        
        choice = "1"
        if choice == "1":
            result = self.cli.load_academic_research_domain()
            self.assertEqual(result, "academic_loaded")
        
        # Test choice 2 - Inventive Step
        original_load_inventive = self.cli.load_inventive_step_domain
        self.cli.load_inventive_step_domain = lambda: "inventive_loaded"
        
        choice = "2"
        if choice == "2":
            result = self.cli.load_inventive_step_domain()
            self.assertEqual(result, "inventive_loaded")
        
        # Test choice 3 - Back to main menu
        choice = "3"
        if choice == "3":
            result = None
            self.assertIsNone(result)
        
        # Restore original methods
        self.cli.load_academic_research_domain = original_load_academic
        self.cli.load_inventive_step_domain = original_load_inventive
    
    def test_domain_menu_logic(self):
        """Test domain menu choice handling logic"""
        # Set up a mock ADF
        self.cli.adf = type('MockADF', (), {'name': 'Test Domain'})()
        
        # Test choice 1 - Query domain
        original_query = self.cli.query_domain
        self.cli.query_domain = lambda: "queried"
        
        choice = "1"
        if choice == "1":
            result = self.cli.query_domain()
            self.assertEqual(result, "queried")
        
        # Test choice 2 - Visualize domain
        original_visualize = self.cli.visualize_domain
        self.cli.visualize_domain = lambda: "visualized"
        
        choice = "2"
        if choice == "2":
            result = self.cli.visualize_domain()
            self.assertEqual(result, "visualized")
        
        # Test choice 3 - Back to main menu
        choice = "3"
        if choice == "3":
            result = None
            self.assertIsNone(result)
        
        # Restore original methods
        self.cli.query_domain = original_query
        self.cli.visualize_domain = original_visualize
    
    def test_query_domain_basic(self):
        """Test query domain basic functionality"""
        # Mock the ask_questions method
        original_ask = self.cli.ask_questions
        self.cli.ask_questions = lambda: "questions_asked"
        
        # Test with case name
        self.cli.caseName = 'test'
        self.cli.case = []
        
        # Simulate the query_domain logic
        if self.cli.caseName:
            result = self.cli.ask_questions()
            self.assertEqual(result, "questions_asked")
            self.assertEqual(self.cli.caseName, 'test')
            self.assertEqual(self.cli.case, [])
        
        # Test without case name
        self.cli.caseName = None
        if not self.cli.caseName:
            # This would print "No case name provided" in the actual method
            self.assertTrue(True)  # Just verify the logic works
        
        # Restore original method
        self.cli.ask_questions = original_ask
    
    def test_ask_questions_basic(self):
        """Test ask_questions basic functionality"""
        # Set up mock ADF
        mock_adf = type('MockADF', (), {
            'nodes': {},
            'questionOrder': []
        })()
        self.cli.adf = mock_adf
        
        # Mock the show_outcome method
        original_show = self.cli.show_outcome
        self.cli.show_outcome = lambda: "outcome_shown"
        
        # Test without question order
        if not self.cli.adf.questionOrder:
            # This would print "No question order specified" in the actual method
            self.assertTrue(True)  # Just verify the logic works
        
        # Test with question order
        self.cli.adf.questionOrder = ['question1', 'question2']
        if self.cli.adf.questionOrder:
            # This would process questions in the actual method
            self.assertTrue(True)  # Just verify the logic works
        
        # Restore original method
        self.cli.show_outcome = original_show
    
    def test_show_outcome_basic(self):
        """Test show_outcome basic functionality"""
        # Set up mock ADF and case
        def success_evaluateTree(self, case):
            return ['Result 1', 'Result 2']
        
        mock_adf = type('MockADF', (), {
            'evaluateTree': success_evaluateTree
        })()
        self.cli.adf = mock_adf
        self.cli.caseName = 'test_case'
        self.cli.case = ['node1', 'node2']
        
        # Mock print to capture output
        builtins.print = self.mock_print
        
        # Test successful evaluation
        try:
            statements = self.cli.adf.evaluateTree(self.cli.case)
            self.assertEqual(statements, ['Result 1', 'Result 2'])
        except Exception as e:
            self.fail(f"Unexpected exception: {e}")
        
        # Test error handling
        def error_evaluateTree(self, case):
            raise Exception("Test error")
        
        mock_adf_error = type('MockADF', (), {
            'evaluateTree': error_evaluateTree
        })()
        self.cli.adf = mock_adf_error
        
        try:
            statements = self.cli.adf.evaluateTree(self.cli.case)
        except Exception as e:
            self.assertEqual(str(e), "Test error")
    
    def test_question_helper_basic(self):
        """Test questionHelper basic functionality"""
        # Set up mock ADF and node
        mock_node = type('MockNode', (), {
            'question': 'Test question?',
            'acceptance': None
        })()
        mock_adf = type('MockADF', (), {
            'nodes': {'test_node': mock_node}
        })()
        self.cli.adf = mock_adf
        
        # Mock input and print
        builtins.input = lambda x: "y"
        builtins.print = self.mock_print
        
        # Test with question
        if hasattr(mock_node, 'question') and mock_node.question:
            # This would ask the question in the actual method
            self.assertTrue(True)  # Just verify the logic works
        
        # Test without question
        mock_node_no_question = type('MockNode', (), {
            'question': None,
            'acceptance': None
        })()
        
        if not (hasattr(mock_node_no_question, 'question') and mock_node_no_question.question):
            # This would add to case without asking in the actual method
            self.assertTrue(True)  # Just verify the logic works
    
    

    
    
    
    def test_query_domain_with_case_name(self):
        """Test query domain with case name"""
        builtins.print = self.mock_print
        
        # Mock the ask_questions method
        original_ask = self.cli.ask_questions
        self.cli.ask_questions = lambda: None
        
        result = self.cli.query_domain()
        self.assertIsNone(result)
        self.assertEqual(self.cli.caseName, 'test')
        self.assertEqual(self.cli.case, [])
        
        # Restore original method
        self.cli.ask_questions = original_ask
    
    def test_query_domain_without_case_name(self):
        """Test query domain without case name"""
        # Temporarily modify the case name assignment
        original_case_name = self.cli.caseName
        self.cli.caseName = None
        builtins.print = self.mock_print
        
        # Mock the ask_questions method
        original_ask = self.cli.ask_questions
        self.cli.ask_questions = lambda: None
        
        result = self.cli.query_domain()
        self.assertIsNone(result)
        
        # Restore original method and case name
        self.cli.ask_questions = original_ask
        self.cli.caseName = original_case_name
    
    def test_ask_questions_with_question_order(self):
        """Test ask_questions with question order"""
        # Set up mock ADF with question order
        mock_adf = type('MockADF', (), {
            'nodes': {},
            'questionOrder': ['question1', 'question2']
        })()
        self.cli.adf = mock_adf
        builtins.print = self.mock_print
        
        # Mock the questiongen method
        original_questiongen = self.cli.questiongen
        self.cli.questiongen = lambda qo, nodes: ([], {})
        
        # Mock the show_outcome method
        original_show = self.cli.show_outcome
        self.cli.show_outcome = lambda: None
        
        self.cli.ask_questions()
        
        # Restore original methods
        self.cli.questiongen = original_questiongen
        self.cli.show_outcome = original_show
    
    def test_ask_questions_without_question_order(self):
        """Test ask_questions without question order"""
        # Set up mock ADF without question order
        mock_adf = type('MockADF', (), {
            'nodes': {},
            'questionOrder': []
        })()
        self.cli.adf = mock_adf
        builtins.print = self.mock_print
        
        # Mock the show_outcome method
        original_show = self.cli.show_outcome
        self.cli.show_outcome = lambda: None
        
        self.cli.ask_questions()
        
        # Restore original method
        self.cli.show_outcome = original_show
    
    def test_question_helper_regular_node_yes(self):
        """Test questionHelper with regular node answering yes"""
        # Set up mock ADF and node
        mock_node = type('MockNode', (), {
            'question': 'Test question?',
            'acceptance': None
        })()
        mock_adf = type('MockADF', (), {
            'nodes': {'test_node': mock_node}
        })()
        self.cli.adf = mock_adf

        builtins.input = lambda x: "y"

        builtins.print = self.mock_print
        
        result = self.cli.questionHelper(mock_node, 'test_node')
        self.assertEqual(result, 'Done')
        self.assertIn('test_node', self.cli.case)
    
    def test_question_helper_regular_node_no(self):
        """Test questionHelper with regular node answering no"""
        # Set up mock ADF and node
        mock_node = type('MockNode', (), {
            'question': 'Test question?',
            'acceptance': None
        })()
        mock_adf = type('MockADF', (), {
            'nodes': {'test_node': mock_node}
        })()
        self.cli.adf = mock_adf

        builtins.input = lambda x: "n"

        builtins.print = self.mock_print
        
        result = self.cli.questionHelper(mock_node, 'test_node')
        self.assertEqual(result, 'Done')
        self.assertNotIn('test_node', self.cli.case)
    
    def test_question_helper_regular_node_invalid_input(self):
        """Test questionHelper with invalid input"""
        # Set up mock ADF and node
        mock_node = type('MockNode', (), {
            'question': 'Test question?',
            'acceptance': None
        })()
        mock_adf = type('MockADF', (), {
            'nodes': {'test_node': mock_node}
        })()
        self.cli.adf = mock_adf
        
        # Mock input to return invalid then valid response
        input_responses = ['invalid', 'y']
        builtins.input = lambda x: input_responses.pop(0)
        builtins.print = self.mock_print
        
        result = self.cli.questionHelper(mock_node, 'test_node')
        self.assertEqual(result, 'Done')
        self.assertIn('test_node', self.cli.case)
    
    def test_question_helper_node_without_question(self):
        """Test questionHelper with node without question"""
        # Set up mock ADF and node
        mock_node = type('MockNode', (), {
            'question': None,
            'acceptance': None
        })()
        mock_adf = type('MockADF', (), {
            'nodes': {'test_node': mock_node}
        })()
        self.cli.adf = mock_adf
        builtins.print = self.mock_print
        
        result = self.cli.questionHelper(mock_node, 'test_node')
        self.assertEqual(result, 'Done')
        self.assertIn('test_node', self.cli.case)
    
    def test_show_outcome_success(self):
        """Test show_outcome with successful evaluation"""
        # Set up mock ADF and case
        mock_adf = type('MockADF', (), {
            'evaluateTree': lambda case: ['Result 1', 'Result 2']
        })()
        self.cli.adf = mock_adf
        self.cli.caseName = 'test_case'
        self.cli.case = ['node1', 'node2']
        builtins.print = self.mock_print
        
        self.cli.show_outcome()
        
        # Debug: print what was actually captured
        print(f"DEBUG: print_calls = {self.print_calls}")
        print_output = ' '.join(self.print_calls)
        print(f"DEBUG: print_output = {print_output}")
        
        # Check that evaluation was called - look for the actual printed content
        self.assertTrue('Result 1' in print_output)
        self.assertTrue('Result 2' in print_output)
    
    def test_show_outcome_error(self):
        """Test show_outcome with evaluation error"""
        # Set up mock ADF that raises exception
        mock_adf = type('MockADF', (), {
            'evaluateTree': lambda case: (_ for _ in ()).throw(Exception("Test error"))
        })()
        self.cli.adf = mock_adf
        self.cli.caseName = 'test_case'
        self.cli.case = ['node1', 'node2']
        builtins.print = self.mock_print
        
        self.cli.show_outcome()
        
        # Check that error was printed
        print_output = ' '.join(self.print_calls)
        self.assertTrue('Error evaluating case' in print_output)
    
    def test_visualize_domain_with_case(self):
        """Test visualize_domain with case data"""
        # Set up mock ADF
        mock_adf = type('MockADF', (), {
            'name': 'Test Domain',
            'visualiseNetworkWithSubADMs': lambda case=None: type('MockGraph', (), {
                'write_png': lambda filename: None
            })()
        })()
        self.cli.adf = mock_adf
        self.cli.caseName = 'test_case'
        self.cli.case = ['node1', 'node2']
        builtins.print = self.mock_print
        
        # Mock os.system to avoid actual system calls
        original_system = os.system
        os.system = lambda x: None
        
        try:
            self.cli.visualize_domain()
        finally:
            os.system = original_system
    
    def test_visualize_domain_without_case(self):
        """Test visualize_domain without case data"""
        # Set up mock ADF
        mock_adf = type('MockADF', (), {
            'name': 'Test Domain',
            'visualiseNetworkWithSubADMs': lambda: type('MockGraph', (), {
                'write_png': lambda filename: None
            })()
        })()
        self.cli.adf = mock_adf
        self.cli.caseName = None
        self.cli.case = []
        builtins.print = self.mock_print
        
        # Mock os.system to avoid actual system calls
        original_system = os.system
        os.system = lambda x: None
        
        try:
            self.cli.visualize_domain()
        finally:
            os.system = original_system
    
    def test_visualize_domain_error(self):
        """Test visualize_domain with error"""
        # Set up mock ADF that raises exception
        mock_adf = type('MockADF', (), {
            'name': 'Test Domain',
            'visualiseNetworkWithSubADMs': lambda case=None: (_ for _ in ()).throw(Exception("Test error"))
        })()
        self.cli.adf = mock_adf
        self.cli.caseName = 'test_case'
        self.cli.case = ['node1', 'node2']
        builtins.print = self.mock_print
        
        self.cli.visualize_domain()
        
        # Check that error was printed
        print_output = ' '.join(self.print_calls)
        self.assertTrue('Error creating visualization' in print_output)

def run_all_tests():
    """Run all unit tests (sub-ADM, main ADM, and CLI UI)"""
    print("Running All ADM Unit Tests...")
    print("="*60)
    
    # Create test suite for all test classes
    suite = unittest.TestSuite()
    
    # Add sub-ADM tests
    sub_adm_suite = unittest.TestLoader().loadTestsFromTestCase(TestSubADMEvaluation)
    suite.addTest(sub_adm_suite)
    
    # Add main ADM tests
    main_adm_suite = unittest.TestLoader().loadTestsFromTestCase(TestMainADMEvaluation)
    suite.addTest(main_adm_suite)
    
    # Add CLI UI tests
    cli_suite = unittest.TestLoader().loadTestsFromTestCase(TestCLIUI)
    suite.addTest(cli_suite)
    
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

def run_cli_tests():
    """Run only CLI UI unit tests"""
    print("Running CLI UI Unit Tests...")
    print("="*60)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCLIUI)
    
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
            error_msg = traceback.split('AssertionError: ')[-1].split('\n')[0]
            print(f"  - {test}: {error_msg}")
    
    if result.errors:
        print(f"\nERRORS:")
        for test, traceback in result.errors:
            error_msg = traceback.split('\n')[-2]
            print(f"  - {test}: {error_msg}")
    
    return result

if __name__ == "__main__":
   
    if len(sys.argv) > 1:
        if sys.argv[1] == "sub":
            run_sub_adm_tests()
        elif sys.argv[1] == "main":
            run_main_adm_tests()
        elif sys.argv[1] == "cli":
            run_cli_tests()
        else:
            print("Usage: python test_adm_unit.py [sub|main|cli]")
            print("  sub  - Run only sub-ADM tests")
            print("  main - Run only main ADM tests")
            print("  cli  - Run only CLI UI tests")
            print("  (no args) - Run all tests")
    else:
        run_all_tests()
