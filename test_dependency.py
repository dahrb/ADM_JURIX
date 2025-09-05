#!/usr/bin/env python3
"""
Dependency evaluation tests for debugging CommonKnowledge dependency issues
"""

import unittest
import sys
import os
# Capture debug output
import io
import sys
from contextlib import redirect_stdout

# Add the current directory to the path so we can import the modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from MainClasses import *
from inventive_step_ADM import adf
from UI import CLI

class TestDependencyEvaluation(unittest.TestCase):
    """Unit tests for dependency evaluation debugging"""

    def setUp(self):
        """Set up test fixtures"""
        self.adf_instance = adf()
        self.ui = CLI()
        self.ui.adf = self.adf_instance
        
    def test_evaluateDependency_detailed_debug(self):
        """Test: Detailed debug output for evaluateDependency method"""
        # Set up case with TechnicalSurvey to enable the full chain
        self.ui.case = ["Contested","TechnicalSurvey"]
        
        output = io.StringIO()
        with redirect_stdout(output):
            # Test evaluateDependency for CommonKnowledge directly
            result = self.ui.evaluateDependency("CommonKnowledge", "Access")
        
        debug_output = output.getvalue()
        
        # Print detailed debug output for analysis
        print(f"\nDetailed debug output for evaluateDependency:")
        print("="*80)
        print(debug_output)
        print("="*80)
        print(f"Final case: {self.ui.case}")
        print(f"Result: {result}")
        
        # Basic assertions - should see successful evaluation
        self.assertIn("Trying to evaluate dependency", debug_output, "Should see dependency evaluation")
        self.assertIn("CommonKnowledge", debug_output, "Should see CommonKnowledge in debug output")
        self.assertIn("CommonKnowledge now satisfied", debug_output, "Should see CommonKnowledge now satisfied message")
        self.assertIn("DocumentaryEvidence now satisfied", debug_output, "Should see DocumentaryEvidence now satisfied message")
        
        # Check that both dependencies were added to case
        self.assertIn("DocumentaryEvidence", self.ui.case, "DocumentaryEvidence should be added to case")
        self.assertIn("CommonKnowledge", self.ui.case, "CommonKnowledge should be added to case")
    
    def test_evaluateDependency_combination_motive_chain(self):
        """Test: CombinationMotive dependency chain"""
        # Set up case with required components for CombinationMotive
        # CombinationMotive requires: ClosestPriorArt, SkilledPerson, CombinationAttempt
        self.ui.case = ["ClosestPriorArt", "SkilledPerson", "CombinationAttempt", "TechnicalSurvey"]
        
        output = io.StringIO()
        with redirect_stdout(output):
            # Test evaluateDependency for CombinationMotive directly
            result = self.ui.evaluateDependency("CombinationMotive", "TestQuestion")
        
        debug_output = output.getvalue()
        
        # Print debug output for analysis
        print(f"\nDebug output for CombinationMotive dependency chain:")
        print("="*80)
        print(debug_output)
        print("="*80)
        print(f"Final case: {self.ui.case}")
        print(f"Result: {result}")
        
        # Should see dependency evaluation
        self.assertIn("Trying to evaluate dependency", debug_output, "Should see dependency evaluation")
        self.assertIn("CombinationMotive", debug_output, "Should see CombinationMotive in debug output")

    def test_evaluateDependency_combination_motive_failure_case(self):
        """Test: CombinationMotive failure case - missing required dependency"""
        # Set up case missing CombinationAttempt (required for CombinationMotive)
        self.ui.case = ["ClosestPriorArt", "SkilledPerson", "TechnicalSurvey"]
        
        output = io.StringIO()
        with redirect_stdout(output):
            # Test evaluateDependency for CombinationMotive directly
            result = self.ui.evaluateDependency("CombinationMotive", "TestQuestion")
        
        debug_output = output.getvalue()
        
        # Print debug output for analysis
        print(f"\nDebug output for CombinationMotive failure case:")
        print("="*80)
        print(debug_output)
        print("="*80)
        print(f"Final case: {self.ui.case}")
        print(f"Result: {result}")
        
        # Should see dependency evaluation attempt but CombinationMotive should not be satisfied
        self.assertIn("Trying to evaluate dependency", debug_output, "Should see dependency evaluation")
        self.assertIn("CombinationMotive", debug_output, "Should see CombinationMotive in debug output")
        # CombinationMotive should not be added to case due to missing CombinationAttempt
        self.assertNotIn("CombinationMotive", self.ui.case, "CombinationMotive should not be added with missing dependencies")
    
    
    def test_evaluateDependency_basis_to_associate_chain(self):
        """Test: BasisToAssociate dependency chain"""
        # Set up case with required components for BasisToAssociate
        self.ui.case = ["ClosestPriorArt", "SkilledPerson", "CombinationAttempt", "TechnicalSurvey"]
        
        output = io.StringIO()
        with redirect_stdout(output):
            # Test evaluateDependency for BasisToAssociate directly
            result = self.ui.evaluateDependency("BasisToAssociate", "TestQuestion")
        
        debug_output = output.getvalue()
        
        # Print debug output for analysis
        print(f"\nDebug output for BasisToAssociate dependency chain:")
        print("="*80)
        print(debug_output)
        print("="*80)
        print(f"Final case: {self.ui.case}")
        print(f"Result: {result}")
        
        # Should see dependency evaluation
        self.assertIn("Trying to evaluate dependency", debug_output, "Should see dependency evaluation")
        self.assertIn("BasisToAssociate", debug_output, "Should see BasisToAssociate in debug output")
    
    def test_evaluateDependency_closest_prior_art_chain(self):
        """Test: ClosestPriorArt dependency chain"""
        # Set up case with required components for ClosestPriorArt
        # ClosestPriorArt requires: RelevantPriorArt and SingleReference and MinModifications and AssessedBy
        self.ui.case = ["RelevantPriorArt", "SingleReference", "MinModifications", "AssessedBy", "SameField"]
        
        output = io.StringIO()
        with redirect_stdout(output):
            # Test evaluateDependency for ClosestPriorArt directly
            result = self.ui.evaluateDependency("ClosestPriorArt", "TestQuestion")
        
        debug_output = output.getvalue()
        
        # Print debug output for analysis
        print(f"\nDebug output for ClosestPriorArt dependency chain:")
        print("="*80)
        print(debug_output)
        print("="*80)
        print(f"Final case: {self.ui.case}")
        print(f"Result: {result}")
        
        # Should see dependency evaluation
        self.assertIn("Trying to evaluate dependency", debug_output, "Should see dependency evaluation")
        self.assertIn("ClosestPriorArt", debug_output, "Should see ClosestPriorArt in debug output")
    
    def test_evaluateDependency_combination_documents_chain(self):
        """Test: CombinationDocuments dependency chain"""
        # Set up case with required components for CombinationDocuments
        self.ui.case = ["CombinationAttempt", "SameFieldCPA", "CombinationMotive", "BasisToAssociate", "TechnicalSurvey"]
        
        output = io.StringIO()
        with redirect_stdout(output):
            # Test evaluateDependency for CombinationDocuments directly
            result = self.ui.evaluateDependency("CombinationDocuments", "TestQuestion")
        
        debug_output = output.getvalue()
        
        # Print debug output for analysis
        print(f"\nDebug output for CombinationDocuments dependency chain:")
        print("="*80)
        print(debug_output)
        print("="*80)
        print(f"Final case: {self.ui.case}")
        print(f"Result: {result}")
        
        # Should see dependency evaluation
        self.assertIn("Trying to evaluate dependency", debug_output, "Should see dependency evaluation")
        self.assertIn("CombinationDocuments", debug_output, "Should see CombinationDocuments in debug output")
    
    def test_evaluateDependency_relevant_prior_art_chain(self):
        """Test: RelevantPriorArt dependency chain"""
        # Set up case with required components for RelevantPriorArt
        self.ui.case = ["SameField", "SimilarField", "SimilarPurpose", "SimilarEffect"]
        
        output = io.StringIO()
        with redirect_stdout(output):
            # Test evaluateDependency for RelevantPriorArt directly
            result = self.ui.evaluateDependency("RelevantPriorArt", "TestQuestion")
        
        debug_output = output.getvalue()
        
        # Print debug output for analysis
        print(f"\nDebug output for RelevantPriorArt dependency chain:")
        print("="*80)
        print(debug_output)
        print("="*80)
        print(f"Final case: {self.ui.case}")
        print(f"Result: {result}")
        
        # Should see dependency evaluation
        self.assertIn("Trying to evaluate dependency", debug_output, "Should see dependency evaluation")
        self.assertIn("RelevantPriorArt", debug_output, "Should see RelevantPriorArt in debug output")
    
    def test_evaluateDependency_person_chain(self):
        """Test: Person dependency chain"""
        # Set up case with required components for Person
        self.ui.case = ["Individual", "ResearchTeam", "ProductionTeam"]
        
        output = io.StringIO()
        with redirect_stdout(output):
            # Test evaluateDependency for Person directly
            result = self.ui.evaluateDependency("Person", "TestQuestion")
        
        debug_output = output.getvalue()
        
        # Print debug output for analysis
        print(f"\nDebug output for Person dependency chain:")
        print("="*80)
        print(debug_output)
        print("="*80)
        print(f"Final case: {self.ui.case}")
        print(f"Result: {result}")
        
        # Should see dependency evaluation
        self.assertIn("Trying to evaluate dependency", debug_output, "Should see dependency evaluation")
        self.assertIn("Person", debug_output, "Should see Person in debug output")
    
    def test_evaluateDependency_skilled_in_chain(self):
        """Test: SkilledIn dependency chain"""
        # Set up case with required components for SkilledIn
        # SkilledIn depends on RelevantPriorArt
        self.ui.case = ["RelevantPriorArt", "SameField"]
        
        output = io.StringIO()
        with redirect_stdout(output):
            # Test evaluateDependency for SkilledIn directly
            result = self.ui.evaluateDependency("SkilledIn", "TestQuestion")
        
        debug_output = output.getvalue()
        
        # Print debug output for analysis
        print(f"\nDebug output for SkilledIn dependency chain:")
        print("="*80)
        print(debug_output)
        print("="*80)
        print(f"Final case: {self.ui.case}")
        print(f"Result: {result}")
        
        # Should see dependency evaluation
        self.assertIn("Trying to evaluate dependency", debug_output, "Should see dependency evaluation")
        self.assertIn("SkilledIn", debug_output, "Should see SkilledIn in debug output")
    
    def test_evaluateDependency_combination_attempt_chain(self):
        """Test: CombinationAttempt dependency chain"""
        # Set up case with required components for CombinationAttempt
        self.ui.case = ["ClosestPriorArt", "SkilledPerson", "MinModifications", "AssessedBy"]
        
        output = io.StringIO()
        with redirect_stdout(output):
            # Test evaluateDependency for CombinationAttempt directly
            result = self.ui.evaluateDependency("CombinationAttempt", "TestQuestion")
        
        debug_output = output.getvalue()
        
        # Print debug output for analysis
        print(f"\nDebug output for CombinationAttempt dependency chain:")
        print("="*80)
        print(debug_output)
        print("="*80)
        print(f"Final case: {self.ui.case}")
        print(f"Result: {result}")
        
        # Should see dependency evaluation
        self.assertIn("Trying to evaluate dependency", debug_output, "Should see dependency evaluation")
        self.assertIn("CombinationAttempt", debug_output, "Should see CombinationAttempt in debug output")
    
    def test_evaluateDependency_complex_failure_case(self):
        """Test: Complex failure case with missing dependencies"""
        # Set up case with incomplete dependencies
        self.ui.case = ["TechnicalSurvey"]  # Missing other required components
        
        output = io.StringIO()
        with redirect_stdout(output):
            # Test evaluateDependency for SkilledPerson (should fail due to missing dependencies)
            result = self.ui.evaluateDependency("SkilledPerson", "TestQuestion")
        
        debug_output = output.getvalue()
        
        # Print debug output for analysis
        print(f"\nDebug output for complex failure case:")
        print("="*80)
        print(debug_output)
        print("="*80)
        print(f"Final case: {self.ui.case}")
        print(f"Result: {result}")
        
        # Should see dependency evaluation attempts but failures
        self.assertIn("Trying to evaluate dependency", debug_output, "Should see dependency evaluation attempts")
        self.assertIn("SkilledPerson", debug_output, "Should see SkilledPerson in debug output")
        
        # SkilledPerson should not be added due to missing dependencies
        self.assertNotIn("SkilledPerson", self.ui.case, "SkilledPerson should not be added with incomplete dependencies")
    
    # Note: Sub-ADM tests removed because those nodes are in sub_adf, not the main adf
    # The evaluateDependency method only works with nodes in the main ADF

if __name__ == "__main__":
    # Run the dependency evaluation tests
    print("Running Dependency Evaluation Tests...")
    print("="*60)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDependencyEvaluation)
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    # Exit with error code if tests failed
    if result.failures or result.errors:
        sys.exit(1)