#!/usr/bin/env python3
"""
ADM Unit Testing System
Generates random test cases and provides detailed evaluation reports
"""

import random
import copy
from datetime import datetime
from MainClasses import ADF, Node, DependentBLF, SubADMBLF, EvaluationBLF, SubADM

class ADMTester:
    """Comprehensive testing system for ADM evaluation"""
    
    def __init__(self, adm_instance):
        self.adm = adm_instance
        self.test_results = []
        self.test_counter = 0
        
    def generate_random_test_case(self, complexity=5):
        """
        Generate a random test case with specified complexity
        
        Parameters:
        -----------
        complexity : int
            Number of BLFs to randomly accept/reject (1-10)
        """
        # Get only actual BLFs (nodes without children, excluding special nodes)
        blfs = []
        for name, node in self.adm.nodes.items():
            # Only include nodes that are actual BLFs (no children, not special types)
            if (not hasattr(node, 'children') or not node.children) and \
               not hasattr(node, 'checkDependency') and \
               not hasattr(node, 'evaluateResults') and \
               not hasattr(node, 'evaluateSubADMs'):
                blfs.append(name)
        
        if not blfs:
            return []
        
        # Randomly select BLFs to accept
        num_to_accept = min(complexity, len(blfs))
        accepted_blfs = random.sample(blfs, num_to_accept)
        
        # Add some factual ascriptions if the ADM supports them
        if hasattr(self.adm, 'facts'):
            for blf in accepted_blfs:
                # Randomly add some facts
                if random.random() < 0.3:  # 30% chance
                    fact_name = f"test_fact_{random.randint(1, 5)}"
                    fact_value = f"value_{random.randint(1, 100)}"
                    self.adm.setFact(blf, fact_name, fact_value)
        
        return accepted_blfs
    
    def run_single_test(self, test_case, test_name=None):
        """
        Run a single test case and return detailed results
        
        Parameters:
        -----------
        test_case : list
            List of BLF names to accept
        test_name : str, optional
            Name for this test case
            
        Returns:
        --------
        dict: Detailed test results
        """
        if test_name is None:
            test_name = f"Test_{self.test_counter}"
            self.test_counter += 1
        
        print(f"\n{'='*60}")
        print(f"RUNNING: {test_name}")
        print(f"Test Case: {test_case}")
        print(f"{'='*60}")
        
        # Create a copy of the ADM for testing
        test_adm = copy.deepcopy(self.adm)
        
        # Track evaluation steps
        evaluation_steps = []
        
        # Step 1: Initial case setup
        step = {
            'step': 1,
            'description': 'Initial case setup',
            'case': test_case.copy(),
            'non_leaf_nodes': list(test_adm.nonLeaf.keys()) if hasattr(test_adm, 'nonLeaf') else [],
            'statements': []
        }
        evaluation_steps.append(step)
        
        print(f"\nStep 1: Initial case setup")
        print(f"  Case: {test_case}")
        print(f"  Non-leaf nodes: {step['non_leaf_nodes']}")
        
        # Step 2: Evaluate the tree
        try:
            print(f"\nStep 2: Evaluating tree...")
            
            # Store original case
            original_case = test_adm.case.copy() if hasattr(test_adm, 'case') else []
            
            # Run evaluation
            statements = test_adm.evaluateTree(test_case)
            
            # Get final case
            final_case = test_adm.case.copy() if hasattr(test_adm, 'case') else []
            
            step = {
                'step': 2,
                'description': 'Tree evaluation completed',
                'case': final_case,
                'statements': statements,
                'evaluation_success': True,
                'error': None
            }
            evaluation_steps.append(step)
            
            print(f"  Evaluation completed successfully")
            print(f"  Final case: {final_case}")
            print(f"  Statements: {statements}")
            
        except Exception as e:
            step = {
                'step': 2,
                'description': 'Tree evaluation failed',
                'case': test_case,
                'statements': [],
                'evaluation_success': False,
                'error': str(e)
            }
            evaluation_steps.append(step)
            
            print(f"  Evaluation failed: {e}")
        
        # Step 3: Analyze results
        step = {
            'step': 3,
            'description': 'Result analysis',
            'initial_blfs': test_case,
            'final_blfs': final_case if 'final_case' in locals() else test_case,
            'added_blfs': [b for b in (final_case if 'final_case' in locals() else test_case) if b not in test_case],
            'statements_count': len(statements) if 'statements' in locals() else 0
        }
        evaluation_steps.append(step)
        
        print(f"\nStep 3: Result analysis")
        print(f"  Initial BLFs: {step['initial_blfs']}")
        print(f"  Final BLFs: {step['final_blfs']}")
        print(f"  Added BLFs: {step['added_blfs']}")
        print(f"  Statements generated: {step['statements_count']}")
        
        # Compile test results
        test_result = {
            'test_name': test_name,
            'test_case': test_case,
            'evaluation_steps': evaluation_steps,
            'success': step['evaluation_success'] if 'evaluation_success' in step else True,
            'timestamp': datetime.now().isoformat()
        }
        
        self.test_results.append(test_result)
        return test_result
    
    def run_multiple_tests(self, num_tests=10, complexity_range=(3, 8)):
        """
        Run multiple random test cases
        
        Parameters:
        -----------
        num_tests : int
            Number of test cases to run
        complexity_range : tuple
            Range of complexity (min, max) for test cases
        """
        print(f"\n{'='*80}")
        print(f"RUNNING {num_tests} RANDOM TEST CASES")
        print(f"Complexity range: {complexity_range[0]}-{complexity_range[1]} BLFs per test")
        print(f"{'='*80}")
        
        for i in range(num_tests):
            complexity = random.randint(complexity_range[0], complexity_range[1])
            test_case = self.generate_random_test_case(complexity)
            test_name = f"Random_Test_{i+1}_Complexity_{complexity}"
            
            self.run_single_test(test_case, test_name)
        
        self.generate_summary_report()
    
    def run_edge_case_tests(self):
        """Run tests for edge cases and potential error conditions"""
        print(f"\n{'='*80}")
        print(f"RUNNING EDGE CASE TESTS")
        print(f"{'='*80}")
        
        # Test 1: Empty case
        self.run_single_test([], "Edge_Empty_Case")
        
        # Test 2: Single BLF
        blfs = [name for name, node in self.adm.nodes.items() 
                if (not hasattr(node, 'children') or not node.children) and \
                   not hasattr(node, 'checkDependency') and \
                   not hasattr(node, 'evaluateResults') and \
                   not hasattr(node, 'evaluateSubADMs')]
        if blfs:
            self.run_single_test([blfs[0]], "Edge_Single_BLF")
        
        # Test 3: All BLFs
        if blfs:
            self.run_single_test(blfs, "Edge_All_BLFs")
        
        # Test 4: Non-existent BLFs
        self.run_single_test(["NON_EXISTENT_1", "NON_EXISTENT_2"], "Edge_NonExistent_BLFs")
        
        # Test 5: Mixed valid and invalid
        if blfs:
            mixed_case = blfs[:2] + ["NON_EXISTENT_1"]
            self.run_single_test(mixed_case, "Edge_Mixed_Valid_Invalid")
    
    def generate_summary_report(self):
        """Generate a comprehensive summary report"""
        print(f"\n{'='*80}")
        print(f"COMPREHENSIVE TEST SUMMARY REPORT")
        print(f"{'='*80}")
        
        total_tests = len(self.test_results)
        successful_tests = sum(1 for r in self.test_results if r['success'])
        failed_tests = total_tests - successful_tests
        
        print(f"\nOverall Statistics:")
        print(f"  Total tests run: {total_tests}")
        print(f"  Successful tests: {successful_tests}")
        print(f"  Failed tests: {failed_tests}")
        print(f"  Success rate: {(successful_tests/total_tests)*100:.1f}%")
        
        # Detailed test results
        print(f"\nDetailed Test Results:")
        print(f"{'Test Name':<25} {'Status':<10} {'Initial BLFs':<15} {'Final BLFs':<15} {'Statements':<10}")
        print(f"{'-'*25} {'-'*10} {'-'*15} {'-'*15} {'-'*10}")
        
        for result in self.test_results:
            status = "PASS" if result['success'] else "FAIL"
            initial_count = len(result['test_case'])
            final_count = len(result['evaluation_steps'][-1]['final_blfs']) if result['evaluation_steps'] else 0
            statements_count = result['evaluation_steps'][-1]['statements_count'] if result['evaluation_steps'] else 0
            
            print(f"{result['test_name']:<25} {status:<10} {initial_count:<15} {final_count:<15} {statements_count:<10}")
        
        # Error analysis
        if failed_tests > 0:
            print(f"\nError Analysis:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  {result['test_name']}: {result['evaluation_steps'][-1].get('error', 'Unknown error')}")
        
        # Performance analysis
        print(f"\nPerformance Analysis:")
        total_statements = sum(r['evaluation_steps'][-1]['statements_count'] for r in self.test_results if r['evaluation_steps'])
        avg_statements = total_statements / total_tests if total_tests > 0 else 0
        print(f"  Total statements generated: {total_statements}")
        print(f"  Average statements per test: {avg_statements:.1f}")
        
        # Save detailed report to file
        self.save_detailed_report()
    
    def save_detailed_report(self):
        """Save detailed test results to a file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"adm_test_report_{timestamp}.txt"
        
        with open(filename, 'w') as f:
            f.write("ADM COMPREHENSIVE TEST REPORT\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n")
            f.write(f"ADM Name: {self.adm.name}\n\n")
            
            for result in self.test_results:
                f.write(f"TEST: {result['test_name']}\n")
                f.write(f"Timestamp: {result['timestamp']}\n")
                f.write(f"Test Case: {result['test_case']}\n")
                f.write(f"Success: {result['success']}\n\n")
                
                for step in result['evaluation_steps']:
                    f.write(f"  Step {step['step']}: {step['description']}\n")
                    if 'case' in step:
                        f.write(f"    Case: {step['case']}\n")
                    if 'statements' in step:
                        f.write(f"    Statements: {step['statements']}\n")
                    if 'error' in step and step['error']:
                        f.write(f"    Error: {step['error']}\n")
                    f.write("\n")
                
                f.write("-" * 50 + "\n\n")
        
        print(f"\nDetailed report saved to: {filename}")
    
    def analyze_acceptance_conditions(self):
        """Analyze and display all acceptance conditions in the ADM"""
        print(f"\n{'='*80}")
        print(f"ACCEPTANCE CONDITIONS ANALYSIS")
        print(f"{'='*80}")
        
        for name, node in self.adm.nodes.items():
            if hasattr(node, 'acceptance') and node.acceptance:
                print(f"\nNode: {name}")
                print(f"  Type: {type(node).__name__}")
                print(f"  Acceptance conditions: {node.acceptance}")
                if hasattr(node, 'children') and node.children:
                    print(f"  Children: {node.children}")
                if hasattr(node, 'question'):
                    print(f"  Question: {node.question}")
                print(f"  Statements: {node.statement if hasattr(node, 'statement') else 'None'}")

def main():
    """Main testing function"""
    print("ADM Unit Testing System")
    print("=" * 50)
    
    # Import your ADM instance here
    try:
        # Try to import the academic research ADM
        from academic_research_ADM import adf
        print(f"Loaded ADM: {adf.name}")
    except ImportError:
        print("Could not import academic_research_ADM.adf")
        print("Please ensure your ADM is properly defined and importable")
        return
    
    # Create tester instance
    tester = ADMTester(adf)
    
    # Analyze acceptance conditions
    tester.analyze_acceptance_conditions()
    
    # Run edge case tests
    tester.run_edge_case_tests()
    
    # Run random tests
    tester.run_multiple_tests(num_tests=15, complexity_range=(2, 6))
    
    print(f"\n{'='*80}")
    print(f"TESTING COMPLETED")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()

