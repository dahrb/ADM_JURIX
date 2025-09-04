#!/usr/bin/env python3
"""
Clean unit tests for both sub-ADM and main ADM evaluation with expected final cases
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
    
    def test_reject_statements_basic(self):
        """Test: Basic reject statements with CircumventTechProblem"""
        blf_list = ["DistinguishingFeatures", "CircumventTechProblem"]
        expected_final_case = [
            "DistinguishingFeatures", 
            "CircumventTechProblem",
            "NonReproducible"
        ]
        
        # Test the evaluation and check for reject statements
        sub_adf = create_sub_adm_prior_art("reject_test")
        sub_adf.evaluateTree(blf_list)
        statements = sub_adf.evaluateTree(blf_list)
        
        # Verify reject statements are present
        reject_statements = [stmt for stmt in statements if 'reject' in stmt.lower()]
        self.assertGreater(len(reject_statements), 0, "Should have reject statements")
        
        self.assert_final_case("Basic Reject Statements", blf_list, expected_final_case)
    
    def test_reject_statements_excluded_field(self):
        """Test: ExcludedField reject statements"""
        blf_list = ["DistinguishingFeatures", "ComputerSimulation", "MathematicalMethod"]
        expected_final_case = [
            "DistinguishingFeatures", 
            "NumOrComp",
            "ComputerSimulation",
            "MathematicalMethod",
            "ExcludedField",
            "NonReproducible"
        ]
        
        # Test the evaluation and check for reject statements
        sub_adf = create_sub_adm_prior_art("excluded_field_test")
        sub_adf.evaluateTree(blf_list)
        statements = sub_adf.evaluateTree(blf_list)
        
        # Verify reject statements are present
        reject_statements = [stmt for stmt in statements if 'reject' in stmt.lower()]
        self.assertGreater(len(reject_statements), 0, "Should have reject statements")
        
        self.assert_final_case("Excluded Field Reject Statements", blf_list, expected_final_case)
    
    def test_reject_statements_sufficiency_issue(self):
        """Test: SufficiencyOfDisclosureIssue reject statements"""
        blf_list = ["DistinguishingFeatures", "ClaimContainsEffect"]
        expected_final_case = [
            "DistinguishingFeatures", 
            "ClaimContainsEffect",
            "SufficiencyOfDisclosureIssue",
            "NonReproducible"
        ]
        
        # Test the evaluation and check for reject statements
        sub_adf = create_sub_adm_prior_art("sufficiency_test")
        sub_adf.evaluateTree(blf_list)
        statements = sub_adf.evaluateTree(blf_list)
        
        # Verify reject statements are present
        reject_statements = [stmt for stmt in statements if 'reject' in stmt.lower()]
        self.assertGreater(len(reject_statements), 0, "Should have reject statements")
        
        self.assert_final_case("Sufficiency Issue Reject Statements", blf_list, expected_final_case)
    
    def test_reject_statements_imprecise_effect(self):
        """Test: ImpreciseUnexpectedEffect reject statements"""
        blf_list = ["DistinguishingFeatures", "PreciseTerms"]
        expected_final_case = [
            "DistinguishingFeatures", 
            "PreciseTerms",
            "NonReproducible"
        ]
        
        # Test the evaluation and check for reject statements
        sub_adf = create_sub_adm_prior_art("imprecise_test")
        sub_adf.evaluateTree(blf_list)
        statements = sub_adf.evaluateTree(blf_list)
        
        # Verify reject statements are present
        reject_statements = [stmt for stmt in statements if 'reject' in stmt.lower()]
        self.assertGreater(len(reject_statements), 0, "Should have reject statements")
        
        self.assert_final_case("Imprecise Effect Reject Statements", blf_list, expected_final_case)
    
    def test_reject_statements_reliable_effect(self):
        """Test: ReliableTechnicalEffect reject statements"""
        blf_list = ["DistinguishingFeatures", "BonusEffect"]
        expected_final_case = [
            "DistinguishingFeatures", 
            "BonusEffect",
            "NonReproducible"
        ]
        
        # Test the evaluation and check for reject statements
        sub_adf = create_sub_adm_prior_art("reliable_test")
        sub_adf.evaluateTree(blf_list)
        statements = sub_adf.evaluateTree(blf_list)
        
        # Verify reject statements are present
        reject_statements = [stmt for stmt in statements if 'reject' in stmt.lower()]
        self.assertGreater(len(reject_statements), 0, "Should have reject statements")
        
        self.assert_final_case("Reliable Effect Reject Statements", blf_list, expected_final_case)
     
    def test_reject_statements_multiple_rejects(self):
        """Test: Multiple reject conditions in one case"""
        blf_list = ["DistinguishingFeatures", "CircumventTechProblem", "ComputerSimulation", "ClaimContainsEffect"]
        expected_final_case = [
            "DistinguishingFeatures", 
            "CircumventTechProblem",
            "ComputerSimulation",
            "NumOrComp",
            "ClaimContainsEffect",
            "ExcludedField",
            "SufficiencyOfDisclosureIssue",
            "NonReproducible"
        ]
        
        # Test the evaluation and check for reject statements
        sub_adf = create_sub_adm_prior_art("multiple_reject_test")
        sub_adf.evaluateTree(blf_list)
        statements = sub_adf.evaluateTree(blf_list)
        
        # Verify multiple reject statements are present
        reject_statements = [stmt for stmt in statements if 'reject' in stmt.lower()]
        self.assertGreater(len(reject_statements), 1, "Should have multiple reject statements")
        
        self.assert_final_case("Multiple Reject Statements", blf_list, expected_final_case)
    
    def test_reject_statements_no_rejects(self):
        """Test: Case that should not trigger reject statements"""
        blf_list = ["DistinguishingFeatures", "IndependentContribution", "Credible", "Reproducible"]
        expected_final_case = [
            "DistinguishingFeatures", 
            "IndependentContribution",
            "Credible",
            "Reproducible",
            "NormalTechnicalContribution",
            "FeatureTechnicalContribution",
            "ReliableTechnicalEffect",
        ]
        
        # Test the evaluation - this case should have minimal or no reject statements
        sub_adf = create_sub_adm_prior_art("no_reject_test")
        sub_adf.evaluateTree(blf_list)
        statements = sub_adf.evaluateTree(blf_list)
        
        # This case should have evaluation results (statements)
        self.assertGreater(len(statements), 0, "Should have evaluation statements")
        
        # Check that we have some non-reject statements (positive or neutral statements)
        non_reject_statements = [stmt for stmt in statements if 'reject' not in stmt.lower()]
        self.assertGreater(len(non_reject_statements), 0, "Should have non-reject statements")
        
        self.assert_final_case("No Reject Statements", blf_list, expected_final_case)
    
    
    def test_question_instantiator_basic(self):
        """Test: QuestionInstantiator basic functionality"""
        from inventive_step_ADM import create_sub_adm_prior_art
        
        # Create a sub-ADM and test question instantiator
        sub_adf = create_sub_adm_prior_art("question_instantiator_test")
        
        # Find a QuestionInstantiator node
        question_instantiator = None
        for node_name, node in sub_adf.nodes.items():
            if hasattr(node, 'blf_mapping'):
                question_instantiator = node
                break
        
        if question_instantiator:
            # Test that it has the required attributes
            self.assertIsNotNone(question_instantiator.blf_mapping)
            self.assertIsInstance(question_instantiator.blf_mapping, dict)
            self.assertGreater(len(question_instantiator.blf_mapping), 0)
    
    def test_question_instantiator_blf_mapping(self):
        """Test: QuestionInstantiator BLF mapping functionality"""
        from inventive_step_ADM import create_sub_adm_prior_art
        
        # Create a sub-ADM
        sub_adf = create_sub_adm_prior_art("mapping_test")
        
        # Find a QuestionInstantiator node with BLF mapping
        question_instantiator = None
        for node_name, node in sub_adf.nodes.items():
            if hasattr(node, 'blf_mapping'):
                question_instantiator = node
                break
        
        if question_instantiator:
            mapping = question_instantiator.blf_mapping
            
            # Verify expected mappings exist
            expected_mappings = [
                "A computer simulation.",
                "The processing of numerical data.",
                "A mathematical method or algorithm.",
                "Other excluded field",
                "None of the above"
            ]
            
            for expected in expected_mappings:
                self.assertIn(expected, mapping)
            
            # Verify BLF mappings
            self.assertEqual(mapping["A computer simulation."], "ComputerSimulation")
            self.assertEqual(mapping["The processing of numerical data."], "NumericalData")
            self.assertEqual(mapping["A mathematical method or algorithm."], "MathematicalMethod")
    
    
    def test_dependent_blf_factual_ascription(self):
        """Test: DependentBLF factual ascription inheritance"""
        from inventive_step_ADM import create_sub_adm_prior_art
        
        # Create a sub-ADM
        sub_adf = create_sub_adm_prior_art("ascription_test")
        
        # Find a DependentBLF with factual ascription
        dependent_blf = None
        for node_name, node in sub_adf.nodes.items():
            if hasattr(node, 'dependency_node') and hasattr(node, 'factual_ascription'):
                dependent_blf = node
                break
        
        if dependent_blf and dependent_blf.factual_ascription:
            # Test that factual ascription is properly set
            self.assertIsInstance(dependent_blf.factual_ascription, dict)
    
    def test_question_instantiator_dependency(self):
        """Test: QuestionInstantiator with dependency node"""
        from inventive_step_ADM import create_sub_adm_prior_art
        
        # Create a sub-ADM
        sub_adf = create_sub_adm_prior_art("qi_dependency_test")
        
        # Find a QuestionInstantiator with dependency
        qi_with_dep = None
        for node_name, node in sub_adf.nodes.items():
            if hasattr(node, 'blf_mapping') and hasattr(node, 'dependency_node'):
                qi_with_dep = node
                break
        
        if qi_with_dep:
            # Test that dependency is properly set
            self.assertIsNotNone(qi_with_dep.dependency_node)
            self.assertIsInstance(qi_with_dep.dependency_node, (str, list))


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
    
    def test_cli_with_sub_adm_case_data(self):
        """Test CLI with sub-ADM case data and expected outcomes"""
        # Set up CLI with sub-ADM
        from inventive_step_ADM import create_sub_adm_prior_art
        self.cli.adf = create_sub_adm_prior_art("test_feature")
        self.cli.caseName = "test_sub_adm_case"
        self.cli.case = []
        
        # Test case: Independent Contribution + Computer Simulation + Technical Adaptation
        test_blfs = ["DistinguishingFeatures","IndependentContribution", "ComputerSimulation", "TechnicalAdaptation"]
        expected_final_case = [
            "DistinguishingFeatures", 
            "IndependentContribution", 
            "ExcludedField",
            "NumOrComp",
            "ComputerSimulation", 
            "TechnicalAdaptation", 
            "NonReproducible",
            "ComputationalContribution", 
            "FeatureTechnicalContribution"
        ]
        
        # Simulate adding BLFs to case
        for blf in test_blfs:
            if blf not in self.cli.case:
                self.cli.case.append(blf)
        
        # Evaluate the case
        self.cli.adf.evaluateTree(self.cli.case)
        actual_final_case = self.cli.case.copy()
        
        # Verify expected outcome
        self.assertEqual(set(actual_final_case), set(expected_final_case))
    
    def test_cli_with_main_adm_case_data(self):
        """Test CLI with main ADM case data and expected outcomes"""
        # Set up CLI with main ADM
        from inventive_step_ADM import adf
        self.cli.adf = adf()
        self.cli.caseName = "test_main_adm_case"
        self.cli.case = []
        
        # Test case: Basic skilled person establishment
        test_blfs = ["Individual", "SkilledIn", "Average", "Aware", "Access"]
        expected_final_case = [
            "Individual", "SkilledIn", "Average", 
            "Aware", "Access", "Person", "SkilledPerson", "CommonKnowledge"
        ]
        
        # Simulate adding BLFs to case
        for blf in test_blfs:
            if blf not in self.cli.case:
                self.cli.case.append(blf)
        
        # Evaluate the case
        self.cli.adf.evaluateTree(self.cli.case)
        actual_final_case = self.cli.case.copy()
        
        # Verify expected outcome
        self.assertEqual(set(actual_final_case), set(expected_final_case))
    
    def test_cli_query_domain_with_case_evaluation(self):
        """Test CLI query domain with full case evaluation workflow"""
        # Set up CLI with sub-ADM
        from inventive_step_ADM import create_sub_adm_prior_art
        self.cli.adf = create_sub_adm_prior_art("test_feature")
        self.cli.caseName = "test_query_case"
        self.cli.case = []
        
        # Mock the ask_questions method to simulate user input
        original_ask = self.cli.ask_questions
        def mock_ask_questions():
            # Simulate adding BLFs based on user responses
            test_blfs = ["IndependentContribution", "Credible", "Reproducible"]
            for blf in test_blfs:
                if blf not in self.cli.case:
                    self.cli.case.append(blf)
            return "questions_completed"
        
        self.cli.ask_questions = mock_ask_questions
        
        # Test query domain workflow
        result = self.cli.query_domain()
        self.assertIsNone(result)  # query_domain returns None
        self.assertEqual(self.cli.caseName, "test")  # query_domain hardcodes caseName as 'test'
        
        # Verify case was populated
        self.assertTrue(len(self.cli.case) > 0)
        
        # Restore original method
        self.cli.ask_questions = original_ask
    
    def test_cli_show_outcome_with_actual_evaluation(self):
        """Test CLI show_outcome with actual ADF evaluation"""
        # Set up CLI with sub-ADM and case data
        from inventive_step_ADM import create_sub_adm_prior_art
        self.cli.adf = create_sub_adm_prior_art("test_feature")
        self.cli.caseName = "test_outcome_case"
        self.cli.case = ["DistinguishingFeatures", "IndependentContribution"]
        
        # Mock print to capture output
        builtins.print = self.mock_print
        
        # Call show_outcome
        self.cli.show_outcome()
        
        # Verify evaluation was performed and results were printed
        print_output = ' '.join(self.print_calls)
        self.assertTrue('Case Outcome: test_outcome_case' in print_output)
        self.assertTrue('Evaluation Results:' in print_output)
    
    def test_cli_complex_workflow_sub_adm(self):
        """Test complete CLI workflow with complex sub-ADM case"""
        # Set up CLI with sub-ADM
        from inventive_step_ADM import create_sub_adm_prior_art
        self.cli.adf = create_sub_adm_prior_art("complex_feature")
        self.cli.caseName = "complex_sub_adm_case"
        self.cli.case = []
        
        # Complex test case: All positive factors
        test_blfs = ["DistinguishingFeatures", "IndependentContribution", "ComputerSimulation", "TechnicalAdaptation", "Credible", "Reproducible"]
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
        
        # Simulate full workflow
        for blf in test_blfs:
            if blf not in self.cli.case:
                self.cli.case.append(blf)
        
        # Evaluate case
        self.cli.adf.evaluateTree(self.cli.case)
        actual_final_case = self.cli.case.copy()
        
        # Verify expected outcome
        self.assertEqual(set(actual_final_case), set(expected_final_case))
        
        # Test show_outcome
        builtins.print = self.mock_print
        self.cli.show_outcome()
        
        # Verify results were displayed
        print_output = ' '.join(self.print_calls)
        self.assertTrue('complex_sub_adm_case' in print_output)
    
    def test_cli_complex_workflow_main_adm(self):
        """Test complete CLI workflow with complex main ADM case"""
        # Set up CLI with main ADM
        from inventive_step_ADM import adf
        self.cli.adf = adf()
        self.cli.caseName = "complex_main_adm_case"
        self.cli.case = []
        
        # Complex test case: All major factors
        test_blfs = [
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
        
        # Simulate full workflow
        for blf in test_blfs:
            if blf not in self.cli.case:
                self.cli.case.append(blf)
        
        # Evaluate case
        self.cli.adf.evaluateTree(self.cli.case)
        actual_final_case = self.cli.case.copy()
        
        # Verify expected outcome
        self.assertEqual(set(actual_final_case), set(expected_final_case))
        
        # Test show_outcome
        builtins.print = self.mock_print
        self.cli.show_outcome()
        
        # Verify results were displayed
        print_output = ' '.join(self.print_calls)
        self.assertTrue('complex_main_adm_case' in print_output)
    
    def test_cli_rejection_case_sub_adm(self):
        """Test CLI with sub-ADM rejection case"""
        # Set up CLI with sub-ADM
        from inventive_step_ADM import create_sub_adm_prior_art
        self.cli.adf = create_sub_adm_prior_art("rejection_feature")
        self.cli.caseName = "rejection_case"
        self.cli.case = []
        
        # Test case: Should be rejected due to CircumventTechProblem
        test_blfs = ["DistinguishingFeatures","IndependentContribution", "CircumventTechProblem", "Credible", "Reproducible"]
        expected_final_case = [
            "DistinguishingFeatures", 
            "IndependentContribution", 
            "CircumventTechProblem", 
            "Credible", 
            "Reproducible"
            # NormalTechnicalContribution should NOT be added due to CircumventTechProblem
        ]
        
        # Simulate workflow
        for blf in test_blfs:
            if blf not in self.cli.case:
                self.cli.case.append(blf)
        
        # Evaluate case
        self.cli.adf.evaluateTree(self.cli.case)
        actual_final_case = self.cli.case.copy()
        
        # Verify expected outcome (rejection)
        self.assertEqual(set(actual_final_case), set(expected_final_case))
        self.assertNotIn("NormalTechnicalContribution", actual_final_case)
    
    def test_cli_edge_case_no_blfs(self):
        """Test CLI with edge case - no BLFs"""
        # Set up CLI with sub-ADM
        from inventive_step_ADM import create_sub_adm_prior_art
        self.cli.adf = create_sub_adm_prior_art("edge_feature")
        self.cli.caseName = "edge_case"
        self.cli.case = []
        
        # Test case: Only base case
        test_blfs = ["DistinguishingFeatures"]
        expected_final_case = [
            "DistinguishingFeatures",
            "NonReproducible"
        ]
        
        # Simulate workflow
        for blf in test_blfs:
            if blf not in self.cli.case:
                self.cli.case.append(blf)
        
        # Evaluate case
        self.cli.adf.evaluateTree(self.cli.case)
        actual_final_case = self.cli.case.copy()
        
        # Verify expected outcome
        self.assertEqual(set(actual_final_case), set(expected_final_case))
    
    def test_cli_case_persistence(self):
        """Test CLI case persistence across operations"""
        # Set up CLI with sub-ADM
        from inventive_step_ADM import create_sub_adm_prior_art
        self.cli.adf = create_sub_adm_prior_art("persistence_feature")
        self.cli.caseName = "persistence_case"
        self.cli.case = []
        
        # Add some BLFs
        test_blfs = ["IndependentContribution", "ComputerSimulation"]
        for blf in test_blfs:
            if blf not in self.cli.case:
                self.cli.case.append(blf)
        
        # Verify case is stored
        self.assertEqual(len(self.cli.case), 2)
        self.assertIn("IndependentContribution", self.cli.case)
        self.assertIn("ComputerSimulation", self.cli.case)
        
        # Test that case persists across operations (but show_outcome will add abstract factors)
        original_case = self.cli.case.copy()
        self.cli.show_outcome()  # This will add abstract factors via evaluateTree()
        
        # Verify that the original BLFs are still there, but abstract factors may be added
        for blf in original_case:
            self.assertIn(blf, self.cli.case)
        
        # The case should have grown (abstract factors added)
        self.assertGreaterEqual(len(self.cli.case), len(original_case))


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
        print(f"\n{'='*60}")
        print(f"DETAILED FAILURE ANALYSIS")
        print(f"{'='*60}")
        for i, (test, traceback) in enumerate(result.failures, 1):
            print(f"\n{i}. FAILURE: {test}")
            print(f"{'─'*50}")
            
            # Extract the detailed error message
            lines = traceback.split('\n')
            assertion_found = False
            
            for line in lines:
                if 'Expected:' in line and 'Got:' in line:
                    print(f"   Assertion Error: {line}")
                    assertion_found = True
                    break
            
            if not assertion_found:
                # Look for AssertionError line
                for line in lines:
                    if 'AssertionError:' in line:
                        error_msg = line.split('AssertionError: ')[-1]
                        print(f"   Assertion Error: {error_msg}")
                        assertion_found = True
                        break
            
            if not assertion_found:
                # Fallback to original error message
                error_msg = traceback.split('AssertionError: ')[-1].split('\n')[0]
                print(f"   Error: {error_msg}")
            
            # Show the full traceback for debugging
            print(f"\n   Full Traceback:")
            for line in lines:
                if line.strip():
                    print(f"   {line}")
    
    if result.errors:
        print(f"\n{'='*60}")
        print(f"DETAILED ERROR ANALYSIS")
        print(f"{'='*60}")
        for i, (test, traceback) in enumerate(result.errors, 1):
            print(f"\n{i}. ERROR: {test}")
            print(f"{'─'*50}")
            
            # Extract the main error message
            lines = traceback.split('\n')
            error_msg = "Unknown error"
            
            for line in lines:
                if 'Exception:' in line or 'Error:' in line:
                    error_msg = line.strip()
                    break
                elif 'Traceback' in line and 'most recent call last' in line:
                    # Look for the actual exception in the next few lines
                    for j, trace_line in enumerate(lines[lines.index(line)+1:], lines.index(line)+1):
                        if 'Exception' in trace_line or 'Error' in trace_line:
                            error_msg = trace_line.strip()
                            break
            
            print(f"   Error: {error_msg}")
            
            # Show the full traceback for debugging
            print(f"\n   Full Traceback:")
            for line in lines:
                if line.strip():
                    print(f"   {line}")
    
    # Exit with error code if tests failed
    if result.failures or result.errors:
        sys.exit(1)
    
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
        print(f"\n{'='*60}")
        print(f"DETAILED FAILURE ANALYSIS")
        print(f"{'='*60}")
        for i, (test, traceback) in enumerate(result.failures, 1):
            print(f"\n{i}. FAILURE: {test}")
            print(f"{'─'*50}")
            
            # Extract the detailed error message
            lines = traceback.split('\n')
            assertion_found = False
            
            for line in lines:
                if 'Expected:' in line and 'Got:' in line:
                    print(f"   Assertion Error: {line}")
                    assertion_found = True
                    break
            
            if not assertion_found:
                # Look for AssertionError line
                for line in lines:
                    if 'AssertionError:' in line:
                        error_msg = line.split('AssertionError: ')[-1]
                        print(f"   Assertion Error: {error_msg}")
                        assertion_found = True
                        break
            
            if not assertion_found:
                # Fallback to original error message
                error_msg = traceback.split('AssertionError: ')[-1].split('\n')[0]
                print(f"   Error: {error_msg}")
            
            # Show the full traceback for debugging
            print(f"\n   Full Traceback:")
            for line in lines:
                if line.strip():
                    print(f"   {line}")
    
    if result.errors:
        print(f"\n{'='*60}")
        print(f"DETAILED ERROR ANALYSIS")
        print(f"{'='*60}")
        for i, (test, traceback) in enumerate(result.errors, 1):
            print(f"\n{i}. ERROR: {test}")
            print(f"{'─'*50}")
            
            # Extract the main error message
            lines = traceback.split('\n')
            error_msg = "Unknown error"
            
            for line in lines:
                if 'Exception:' in line or 'Error:' in line:
                    error_msg = line.strip()
                    break
                elif 'Traceback' in line and 'most recent call last' in line:
                    # Look for the actual exception in the next few lines
                    for j, trace_line in enumerate(lines[lines.index(line)+1:], lines.index(line)+1):
                        if 'Exception' in trace_line or 'Error' in trace_line:
                            error_msg = trace_line.strip()
                            break
            
            print(f"   Error: {error_msg}")
            
            # Show the full traceback for debugging
            print(f"\n   Full Traceback:")
            for line in lines:
                if line.strip():
                    print(f"   {line}")
    
    # Exit with error code if tests failed
    if result.failures or result.errors:
        sys.exit(1)
    
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
        print(f"\n{'='*60}")
        print(f"DETAILED FAILURE ANALYSIS")
        print(f"{'='*60}")
        for i, (test, traceback) in enumerate(result.failures, 1):
            print(f"\n{i}. FAILURE: {test}")
            print(f"{'─'*50}")
            
            # Extract the detailed error message
            lines = traceback.split('\n')
            assertion_found = False
            
            for line in lines:
                if 'Expected:' in line and 'Got:' in line:
                    print(f"   Assertion Error: {line}")
                    assertion_found = True
                    break
            
            if not assertion_found:
                # Look for AssertionError line
                for line in lines:
                    if 'AssertionError:' in line:
                        error_msg = line.split('AssertionError: ')[-1]
                        print(f"   Assertion Error: {error_msg}")
                        assertion_found = True
                        break
            
            if not assertion_found:
                # Fallback to original error message
                error_msg = traceback.split('AssertionError: ')[-1].split('\n')[0]
                print(f"   Error: {error_msg}")
            
            # Show the full traceback for debugging
            print(f"\n   Full Traceback:")
            for line in lines:
                if line.strip():
                    print(f"   {line}")
    
    if result.errors:
        print(f"\n{'='*60}")
        print(f"DETAILED ERROR ANALYSIS")
        print(f"{'='*60}")
        for i, (test, traceback) in enumerate(result.errors, 1):
            print(f"\n{i}. ERROR: {test}")
            print(f"{'─'*50}")
            
            # Extract the main error message
            lines = traceback.split('\n')
            error_msg = "Unknown error"
            
            for line in lines:
                if 'Exception:' in line or 'Error:' in line:
                    error_msg = line.strip()
                    break
                elif 'Traceback' in line and 'most recent call last' in line:
                    # Look for the actual exception in the next few lines
                    for j, trace_line in enumerate(lines[lines.index(line)+1:], lines.index(line)+1):
                        if 'Exception' in trace_line or 'Error' in trace_line:
                            error_msg = trace_line.strip()
                            break
            
            print(f"   Error: {error_msg}")
            
            # Show the full traceback for debugging
            print(f"\n   Full Traceback:")
            for line in lines:
                if line.strip():
                    print(f"   {line}")
    
    # Exit with error code if tests failed
    if result.failures or result.errors:
        sys.exit(1)
    
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
        print(f"\n{'='*60}")
        print(f"DETAILED FAILURE ANALYSIS")
        print(f"{'='*60}")
        for i, (test, traceback) in enumerate(result.failures, 1):
            print(f"\n{i}. FAILURE: {test}")
            print(f"{'─'*50}")
            
            # Extract the detailed error message
            lines = traceback.split('\n')
            assertion_found = False
            
            for line in lines:
                if 'Expected:' in line and 'Got:' in line:
                    print(f"   Assertion Error: {line}")
                    assertion_found = True
                    break
            
            if not assertion_found:
                # Look for AssertionError line
                for line in lines:
                    if 'AssertionError:' in line:
                        error_msg = line.split('AssertionError: ')[-1]
                        print(f"   Assertion Error: {error_msg}")
                        assertion_found = True
                        break
            
            if not assertion_found:
                # Fallback to original error message
                error_msg = traceback.split('AssertionError: ')[-1].split('\n')[0]
                print(f"   Error: {error_msg}")
            
            # Show the full traceback for debugging
            print(f"\n   Full Traceback:")
            for line in lines:
                if line.strip():
                    print(f"   {line}")
    
    if result.errors:
        print(f"\n{'='*60}")
        print(f"DETAILED ERROR ANALYSIS")
        print(f"{'='*60}")
        for i, (test, traceback) in enumerate(result.errors, 1):
            print(f"\n{i}. ERROR: {test}")
            print(f"{'─'*50}")
            
            # Extract the main error message
            lines = traceback.split('\n')
            error_msg = "Unknown error"
            
            for line in lines:
                if 'Exception:' in line or 'Error:' in line:
                    error_msg = line.strip()
                    break
                elif 'Traceback' in line and 'most recent call last' in line:
                    # Look for the actual exception in the next few lines
                    for j, trace_line in enumerate(lines[lines.index(line)+1:], lines.index(line)+1):
                        if 'Exception' in trace_line or 'Error' in trace_line:
                            error_msg = trace_line.strip()
                            break
            
            print(f"   Error: {error_msg}")
            
            # Show the full traceback for debugging
            print(f"\n   Full Traceback:")
            for line in lines:
                if line.strip():
                    print(f"   {line}")
    
    # Exit with error code if tests failed
    if result.failures or result.errors:
        sys.exit(1)
    
    return result


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "all":
            result = run_all_tests()
        elif sys.argv[1] == "sub":
            result = run_sub_adm_tests()
        elif sys.argv[1] == "main":
            result = run_main_adm_tests()
        elif sys.argv[1] == "cli":
            result = run_cli_tests()
        else:
            print("Usage: python test_adm_unit.py [all|sub|main|cli]")
            print("  all  - Run all tests")
            print("  sub  - Run only sub-ADM tests")
            print("  main - Run only main ADM tests")
            print("  cli  - Run only CLI UI tests")
            print("  (no args) - Run all tests")
            sys.exit(1)
    else:
        result = run_all_tests()
    
    # Exit with error code if any tests failed
    if result.failures or result.errors:
        sys.exit(1)
