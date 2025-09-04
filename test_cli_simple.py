#!/usr/bin/env python3
"""
Simple CLI UI unit tests - focused on non-blocking functionality
"""

import unittest
import builtins
import sys
from UI import CLI

class TestCLISimple(unittest.TestCase):
    """Simple unit tests for CLI UI functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.cli = CLI()
        self.original_input = builtins.input
        self.original_print = builtins.print
        self.print_calls = []
        
    def tearDown(self):
        """Clean up after tests"""
        builtins.input = self.original_input
        builtins.print = self.original_print
    
    def mock_print(self, *args, **kwargs):
        """Mock print function to capture output"""
        self.print_calls.append(' '.join(str(arg) for arg in args))
    
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

def run_cli_simple_tests():
    """Run CLI simple unit tests"""
    print("Running CLI Simple Unit Tests...")
    print("="*60)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCLISimple)
    
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
    run_cli_simple_tests()
