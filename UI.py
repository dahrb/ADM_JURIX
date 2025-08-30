#!/usr/bin/env python3
"""
ADM Command Line Interface
Replaces the tkinter-based UI with a comprehensive command-line interface
"""

import os
import sys
import shlex
from MainClasses import *
import WildAnimals
import inventive_step_ADM
import academic_research_ADM

class CLI:
    def __init__(self):
        self.adf = None
        self.case = []
        self.caseList = {}
        self.caseName = None
        
    def main_menu(self):
        """Main menu with options"""
        while True:
            print("\n" + "="*50)
            print("ADM TOOL - Main Menu")
            print("="*50)
            print("1. Load existing domain")
            print("2. Exit")
            print("-"*50)
            
            choice = input("Enter your choice (1-2): ").strip()
            
            if choice == "1":
                self.load_existing_domain()
            elif choice == "2":
                print("Goodbye!")
                sys.exit(0)
            else:
                print("Invalid choice. Please try again.")
    
    def load_existing_domain(self):
        """Load one of the predefined domains"""
        print("\n" + "="*50)
        print("Load Existing Domain")
        print("="*50)
        print("1. Wild Animals")
        print("2. Academic Research Project")
        print("3. Back to main menu")
        print("-"*50)
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            self.load_wild_animals_domain()
        elif choice == "2":
            self.load_academic_research_domain()
        elif choice == "3":
            return
        else:
            print("Invalid choice. Please try again.")
            self.load_existing_domain()
    
    def load_academic_research_domain(self):
        """Load the Academic Research Project domain"""
        try:

            self.adf = academic_research_ADM.adf()
            self.cases = academic_research_ADM.cases()
            print("Academic Research Project domain loaded successfully!")
            self.domain_menu()
        except Exception as e:
            print(f"Error loading Academic Research Project domain: {e}")
            self.load_existing_domain()
    
    def domain_menu(self):
        """Domain operations menu"""
        while True:
            print("\n" + "="*50)
            print(f"Domain: {self.adf.name}")
            print("="*50)
            print("1. Query domain")
            print("2. Visualize domain")
            print("3. Back to main menu")
            print("-"*50)
            
            choice = input("Enter your choice (1-3): ").strip()
            
            if choice == "1":
                self.query_domain()
            elif choice == "2":
                self.visualize_domain()
            elif choice == "3":
                return
        else:
                print("Invalid choice. Please try again.")
    
    def query_domain(self):
        """Query the domain by answering questions"""
        print("\n" + "="*50)
        print("Query Domain")
        print("="*50)
        
        # Ask for case name or select predefined case
        if self.caseList:
            print("Predefined cases:")
            for i, case_name in enumerate(self.caseList.keys(), 1):
                print(f"{i}. {case_name}")
            print(f"{len(self.caseList) + 1}. Enter custom case name")
            
            choice = input(f"Select case (1-{len(self.caseList) + 1}): ").strip()
            try:
                choice = int(choice)
                if 1 <= choice <= len(self.caseList):
                    case_names = list(self.caseList.keys())
                    self.caseName = case_names[choice - 1]
                    self.case = self.caseList[self.caseName]
                    print(f"Using predefined case: {self.caseName}")
                    self.show_outcome()
                    return
                elif choice == len(self.caseList) + 1:
                    pass
                else:
                    print("Invalid choice.")
                    return
            except ValueError:
                print("Invalid input.")
                return
        
        # Custom case name
        self.caseName = input("Enter case name: ").strip()
        if not self.caseName:
            print("No case name provided.")
            return

        # Reset case and start questioning
        self.case = []
        self.ask_questions()
    
    def ask_questions(self):
        """Ask questions to build the case"""
        print("\nAnswer questions to build your case...")
        
        # Get a copy of nodes and question order
        nodes = self.adf.nodes.copy()
        question_order = self.adf.questionOrder.copy() if self.adf.questionOrder else []
        
        print(f"DEBUG: Initial question order: {question_order}")
        
        question_number = 1
        
        while question_order or nodes:
            current_node = None
            
            # Check question order first
            if question_order:

                # Process the first item in question order
                question_name = question_order[0]
                print(f"DEBUG: Processing question order item: {question_name}")
                
                # Check if this is a question instantiator
                if question_name in self.adf.question_instantiators:
                    # print(f"DEBUG: Processing question instantiator: {question_name}")
                    instantiator = self.adf.question_instantiators[question_name]
                    
                    # Ask the question
                    print(f"\n{instantiator['question']}")
                    
                    # Show available answers
                    answers = list(instantiator['blf_mapping'].keys())
                    for i, answer in enumerate(answers, 1):
                        print(f"{i}. {answer}")
                    
                    # Get user choice
                    while True:
                        try:
                            choice = int(input("Choose an answer (enter number): ")) - 1
                            if 0 <= choice < len(answers):
                                selected_answer = answers[choice]
                                break
                            else:
                                print("Invalid choice. Please try again.")
                        except ValueError:
                            print("Invalid input. Please enter a number.")
                    
                    # Instantiate the corresponding BLF(s)
                    blf_names = instantiator['blf_mapping'][selected_answer]
                    if isinstance(blf_names, str):
                        blf_names = [blf_names]
                    
                    # print(f"DEBUG: Instantiating BLFs: {blf_names}")
                    
                    for blf_name in blf_names:
                        # Add the BLF to the case
                        self.case.append(blf_name)
                        # print(f"DEBUG: Added {blf_name} to case")
                        
                        # Ask factual ascription questions if configured
                        if instantiator.get('factual_ascription') and blf_name in instantiator['factual_ascription']:
                            factual_questions = instantiator['factual_ascription'][blf_name]
                            for fact_name, question in factual_questions.items():
                                answer = input(f"{question}: ").strip()
                                if answer:
                                    self.adf.setFact(blf_name, fact_name, answer)
                                    # print(f"DEBUG: Stored fact {blf_name}.{fact_name} = {answer}")
                    
                    # Force evaluation of abstract factors after BLF instantiation
                    self._force_evaluate_abstract_factors()
                    
                    # Set up parent-child relationships for abstract factors
                    self._setup_abstract_factor_relationships()
                    
                    # Remove from question order to prevent duplicate processing
                    question_order.pop(0)  # Remove from local copy only
                    
                    # Also remove from question_instantiators to prevent reprocessing
                    if question_name in self.adf.question_instantiators:
                        del self.adf.question_instantiators[question_name]
                    
                    continue
                
                # Check if it's a regular node
                elif question_name in nodes:
                    print(f"DEBUG: Found regular node: {question_name}")
                    current_node = nodes[question_name]
                    question_order.pop(0)  # Remove from local copy only
                    # Also remove from nodes to prevent duplicate processing
                    nodes.pop(question_name, None)
                
                # Check if it's a DependentBLF or other node type that should be processed
                elif question_name in self.adf.nodes:
                    print(f"DEBUG: Found node in ADF: {question_name}")
                    current_node = self.adf.nodes[question_name]
                    question_order.pop(0)  # Remove from local copy only
                    # Also remove from nodes to prevent duplicate processing
                    nodes.pop(question_name, None)
        
                else:
                    print(f"DEBUG: Could not find {question_name} in any category")
                    # Remove unknown items from question order
                    question_order.pop(0)  # Remove from local copy only
                    continue
            
            # If no question order, process remaining nodes
            if not current_node and not question_order:
                for node_name, node in list(nodes.items()):
                    if node.children is None or not node.children:
                        current_node = node
                        nodes.pop(node_name)
                        break
            
            if not current_node:
                break
            
            # Ask the question
            if current_node.question or hasattr(current_node, 'question_template'):
                print(f"DEBUG: Processing question for node: {current_node.name}")
                print(f"DEBUG: Node type: {type(current_node)}")
                print(f"DEBUG: Has resolveQuestion: {hasattr(current_node, 'resolveQuestion')}")
                print(f"DEBUG: Has checkDependency: {hasattr(current_node, 'checkDependency')}")
                print(f"DEBUG: Has runAlgorithm: {hasattr(current_node, 'runAlgorithm')}")
                
                # Check if this is an AlgorithmicBLF
                if hasattr(current_node, 'runAlgorithm'):
                    print(f"DEBUG: Processing AlgorithmicBLF: {current_node.name}")
                    should_accept = current_node.runAlgorithm(self)
                    
                    if should_accept:
                        self.case.append(current_node.name)
                        print(f"DEBUG: Algorithm accepted {current_node.name}, added to case")
                        
                        # Force evaluate abstract factors after adding algorithmic BLF
                        print("DEBUG: Forcing evaluation of abstract factors after algorithmic BLF addition...")
                        self._force_evaluate_abstract_factors()
                    else:
                        print(f"DEBUG: Algorithm rejected {current_node.name}")
                    
                    question_number += 1
                    continue
                
                # Check if this is a SubADMBLF
                elif hasattr(current_node, 'evaluateSubADMs'):
                    print(f"DEBUG: Processing SubADMBLF: {current_node.name}")
                    should_accept = current_node.evaluateSubADMs(self)
                    
                    if should_accept:
                        self.case.append(current_node.name)
                        print(f"DEBUG: SubADMBLF accepted {current_node.name}, added to case")
                        
                        # Force evaluate abstract factors after adding sub-ADM BLF
                        print("DEBUG: Forcing evaluation of abstract factors after sub-ADM BLF addition...")
                        self._force_evaluate_abstract_factors()
                    else:
                        print(f"DEBUG: SubADMBLF rejected {current_node.name}")
                    
                    # Remove from nodes to prevent duplicate processing
                    nodes.pop(current_node.name, None)
                    continue
                
                # Check if this is an EvaluationBLF that needs to evaluate sub-ADM results
                elif hasattr(current_node, 'evaluateResults'):
                    # print(f"DEBUG: Processing EvaluationBLF: {current_node.name}...")
                    
                    # Call the evaluation method
                    should_accept = current_node.evaluateResults(self.adf)
                    
                    if should_accept:
                        self.case.append(current_node.name)
                        # print(f"DEBUG: {current_node.name} accepted, added to case")
                    else:
                        # print(f"DEBUG: {current_node.name} rejected")
                        pass
                    
                    # Remove from nodes to prevent duplicate processing
                    nodes.pop(current_node.name, None)
                    continue
                
                # Process regular nodes with questions
                elif current_node.question:
                    # print(f"DEBUG: Processing regular node: {current_node.name}")
                    
                    # Resolve question if it's a DependentBLF
                    if hasattr(current_node, 'resolveQuestion'):
                        current_node.resolveQuestion(self.adf)
                    
                    # Ask the question
                    print(f"\n{current_node.question}")
                    
                    while True:
                        answer = input("Answer (y/n): ").strip().lower()
                        if answer in ['y', 'yes']:
                            self.case.append(current_node.name)
                            # print(f"DEBUG: {current_node.name} accepted, added to case")
                            if hasattr(current_node, 'statement') and current_node.statement and len(current_node.statement) > 0:
                                print(f"\n{current_node.statement[0]}")
                            else:
                                print(f"\n{current_node.name} is accepted")
                            break
                        elif answer in ['n', 'no']:
                            # print(f"DEBUG: {current_node.name} rejected")
                            if hasattr(current_node, 'statement') and current_node.statement and len(current_node.statement) > 1:
                                print(f"\n{current_node.statement[1]}")
                            elif hasattr(current_node, 'statement') and current_node.statement and len(current_node.statement) > 0:
                                print(f"\n{current_node.statement[0]}")
                            else:
                                print(f"\n{current_node.name} is rejected")
                            break
                        else:
                            print("Please answer 'y' or 'n'.")
                    
                    # Force evaluation of abstract factors after BLF instantiation
                    self._force_evaluate_abstract_factors()
                    
                    # Remove from nodes to prevent duplicate processing
                    nodes.pop(current_node.name, None)
                    continue
            else:
                # No question, evaluate automatically
                pass
            
            question_number += 1
            
            # Ensure the processed node is completely removed from consideration
            if current_node and current_node.name in nodes:
                nodes.pop(current_node.name, None)
                print(f"DEBUG: Removed {current_node.name} from nodes to prevent duplicate processing")
        
        print(f"\nCase completed: {self.caseName}")
        self.show_outcome()
    
    def _force_evaluate_abstract_factors(self):
        """
        Force evaluation of abstract factors immediately after BLFs are processed
        This ensures dependencies are resolved before checking them
        """
        print("DEBUG: Force evaluating abstract factors...")
        
        # Find abstract factors (nodes with children that aren't in case yet)
        abstract_factors = []
        for node_name, node in self.adf.nodes.items():
            if node.children and node_name not in self.case:
                # Check if all children are in the case
                if all(child in self.case for child in node.children):
                    abstract_factors.append(node_name)
        
        print(f"DEBUG: Found abstract factors ready for evaluation: {abstract_factors}")
        
        # Evaluate each abstract factor
        for factor_name in abstract_factors:
            try:
                print(f"DEBUG: Evaluating {factor_name}...")
                
                # Create a temporary case with just the children to evaluate this factor
                temp_case = [child for child in self.adf.nodes[factor_name].children if child in self.case]
                
                # Use the ADF's evaluation logic for this specific factor
                # We need to temporarily set the case and evaluate
                original_case = getattr(self.adf, 'case', None)
                self.adf.case = temp_case
                
                # Force evaluation of this specific node
                if self.adf.evaluateNode(self.adf.nodes[factor_name]):
                    self.case.append(factor_name)
                    print(f"DEBUG: {factor_name} was accepted and added to case")
                else:
                    print(f"DEBUG: {factor_name} was not accepted")
                
                # Restore original case
                if original_case is not None:
                    self.adf.case = original_case
                else:
                    delattr(self.adf, 'case')
                    
            except Exception as e:
                print(f"DEBUG: Error evaluating {factor_name}: {e}")
        
        print(f"DEBUG: Case after force evaluation: {self.case}")
    
    def _evaluate_abstract_factors(self):
        """
        Evaluate abstract factors after all BLFs have been processed
        """
        print("DEBUG: Starting abstract factor evaluation...")
        
        # Find abstract factors (nodes with children that aren't in case yet)
        abstract_factors = []
        for node_name, node in self.adf.nodes.items():
            if node.children and node_name not in self.case:
                # Check if all children are in the case
                if all(child in self.case for child in node.children):
                    abstract_factors.append(node_name)
        
        print(f"DEBUG: Found abstract factors to evaluate: {abstract_factors}")
        
        # Evaluate each abstract factor
        for factor_name in abstract_factors:
            try:
                # Use the ADF's evaluation logic
                statements = self.adf.evaluateTree(self.case)
                print(f"DEBUG: Evaluated {factor_name}, statements: {statements}")
                
                # Check if the factor was accepted (should be in case now)
                if factor_name in self.case:
                    print(f"DEBUG: {factor_name} was accepted and added to case")
                else:
                    print(f"DEBUG: {factor_name} was not accepted")
                    
            except Exception as e:
                print(f"DEBUG: Error evaluating {factor_name}: {e}")
        
        print(f"DEBUG: Final case after abstract factor evaluation: {self.case}")
    
    def _setup_abstract_factor_relationships(self):
        """
        Set up parent-child relationships for abstract factors
        This ensures that abstract factors can properly identify their children
        """
        for node_name, node in self.adf.nodes.items():
            if hasattr(node, 'children') and node.children:
                # This is an abstract factor, ensure its children know about it
                for child_name in node.children:
                    if child_name in self.adf.nodes:
                        child_node = self.adf.nodes[child_name]
                        # Ensure the child has a parent reference
                        if not hasattr(child_node, 'parent'):
                            child_node.parent = node_name
    
    def _ask_factual_ascription_questions(self, blf_name, instantiator):
        """
        Ask factual ascription questions for a BLF
        
        Parameters
        ----------
        blf_name : str
            the name of the BLF
        instantiator : dict
            the question instantiator configuration
        """
        if 'factual_ascription' in instantiator and instantiator['factual_ascription']:
            factual_config = instantiator['factual_ascription']
            
            if blf_name in factual_config:
                ascription_config = factual_config[blf_name]
                
                if isinstance(ascription_config, dict):
                    for ascription_name, question_text in ascription_config.items():
                        print(f"\nFactual question for {blf_name}: {question_text}")
                        answer = input("Answer: ").strip()
                        
                        # Store the fact in the ADF
                        if answer:
                            self.adf.setFact(blf_name, ascription_name, answer)
                            print(f"Stored {ascription_name}: {answer} for {blf_name}")
    
    def show_outcome(self):
        """Show the evaluation outcome"""
        print("\n" + "="*50)
        print(f"Case Outcome: {self.caseName}")
        print("="*50)
        
        try:
            statements = self.adf.evaluateTree(self.case)
            print("Evaluation Results:")
            for i, statement in enumerate(statements, 1):
                print(f"{i}. {statement}")
        except Exception as e:
            print(f"Error evaluating case: {e}")
        
        input("\nPress Enter to continue...")
    
    def visualize_domain(self):
        """Visualize the domain as a graph"""
        print("\n" + "="*50)
        print("Visualize Domain")
        print("="*50)
        
        try:
            # Determine filename based on whether we have a case
            if self.caseName and self.case:
                filename = f"{self.caseName}.png"
                # Visualize with case data to show accepted/rejected nodes in color
                # Visualize the network
                print("\nGenerating visualization...")
                try:
                    # Use the comprehensive visualization that includes sub-ADMs
                    G = self.adf.visualiseNetworkWithSubADMs(self.case)
                    
                    # Save the visualization
                    filename = f"{self.caseName}.png"
                    G.write_png(filename)
                    print(f"Visualization saved as {filename}")
                    
                except Exception as e:
                    print(f"Error generating visualization: {e}")
                    # Fallback to regular visualization
                    try:
                        G = self.adf.visualiseNetwork(self.case)
                        filename = f"{self.caseName}.png"
                        G.write_png(filename)
                        print(f"Basic visualization saved as {filename}")
                    except Exception as e2:
                        print(f"Error with fallback visualization: {e2}")
            else:
                filename = f"{self.adf.name}.png"
                # Visualize domain without case data, but still include sub-ADMs
                print(f"Visualizing domain: {self.adf.name}")
                try:
                    # Use the comprehensive visualization that includes sub-ADMs even without case data
                    graph = self.adf.visualiseNetworkWithSubADMs()
                    graph.write_png(filename)
                    print(f"Graph saved as: {filename}")
                except Exception as e:
                    print(f"Error with sub-ADM visualization: {e}")
                    # Fallback to regular visualization
                    try:
                        graph = self.adf.visualiseNetwork()
                        graph.write_png(filename)
                        print(f"Basic visualization saved as: {filename}")
                    except Exception as e2:
                        print(f"Error with fallback visualization: {e2}")
                        return
            
            # Try to open the image if possible
            try:
                if sys.platform.startswith('linux'):
                    os.system(f"xdg-open {shlex.quote(filename)}")
                elif sys.platform.startswith('darwin'):
                    os.system(f"open {shlex.quote(filename)}")
                elif sys.platform.startswith('win'):
                    os.system(f"start {shlex.quote(filename)}")
            except:
                print(f"Image saved as {filename}. Please open it manually.")
                
        except Exception as e:
            print(f"Error creating visualization: {e}")

def main():
    """Main function"""
    print("Welcome to ADM Tool - Command Line Interface")
    print("This tool helps you work with Argumentation Decision Frameworks")
    
    cli = CLI()
    
    try:
        cli.main_menu()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()  