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
            import academic_research_ADM
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
        # Process the question order
        question_order = self.adf.questionOrder.copy()
        nodes = self.adf.nodes
        
        print("Answer questions to build your case...")
        
        while question_order:
            question_name = question_order.pop(0)
            
            # Check if this is a question instantiator
            if question_name in self.adf.question_instantiators:
                # Get the question instantiator (it's a dictionary)
                question_instantiator = self.adf.question_instantiators[question_name]
                
                # Ask the question
                print(f"\nQuestion: {question_instantiator['question']}")
                
                # Get the answer choices from the blf_mapping
                answer_choices = list(question_instantiator['blf_mapping'].keys())
                
                # Show multiple choice options
                for i, answer in enumerate(answer_choices, 1):
                    print(f"{i}. {answer}")
                
                while True:
                    try:
                        choice = int(input("Enter your choice (number): ")) - 1
                        if 0 <= choice < len(answer_choices):
                            selected_answer = answer_choices[choice]
                            break
                        else:
                            print("Invalid choice. Please try again.")
                    except ValueError:
                        print("Please enter a valid number.")
                
                # Get the BLF names to instantiate based on the selected answer
                blf_names = question_instantiator['blf_mapping'][selected_answer]
                
                # Ensure blf_names is always a list
                if isinstance(blf_names, str):
                    blf_names = [blf_names]
                
                # Create the BLF nodes and add them to the ADF
                for blf_name in blf_names:
                    # Create a simple BLF node
                    from MainClasses import Node
                    blf_node = Node(blf_name, None, [f"{blf_name} is accepted", f"{blf_name} is rejected"])
                    self.adf.nodes[blf_name] = blf_node
                    
                    # Add to case
                    self.case.append(blf_name)
                
                # Handle factual ascriptions if present
                if question_instantiator.get('factual_ascription'):
                    factual_config = question_instantiator['factual_ascription']
                    for blf_name in blf_names:
                        if blf_name in factual_config:
                            ascription_config = factual_config[blf_name]
                            if isinstance(ascription_config, dict):
                                for ascription_name, question_text in ascription_config.items():
                                    print(f"\nFactual question for {blf_name}: {question_text}")
                                    answer = input("Answer: ").strip()
                                    
                                    # Store the fact in the ADF
                                    if answer and hasattr(self.adf, 'setFact'):
                                        self.adf.setFact(blf_name, ascription_name, answer)
                                        print(f"DEBUG: Stored fact {blf_name}.{ascription_name} = {answer}")
                
                # Debug: Check what facts were stored
                print(f"DEBUG: Checking stored facts...")
                for blf_name in blf_names:
                    if hasattr(self.adf, 'getFact'):
                        facts = {}
                        for attr in dir(self.adf):
                            if attr.startswith('facts'):
                                facts = getattr(self.adf, attr, {})
                                break
                        if blf_name in facts:
                            print(f"DEBUG: Facts for {blf_name}: {facts[blf_name]}")
                        else:
                            print(f"DEBUG: No facts found for {blf_name}")
                
                # Remove the question instantiator from the ADF
                del self.adf.question_instantiators[question_name]
                
                # Set up abstract factor relationships after instantiating BLFs
                self._setup_abstract_factor_relationships()
                
                # Create MIXED_METHODS node if it doesn't exist (it depends on QUANTITATIVE and QUALITATIVE)
                if "MIXED_METHODS" not in self.adf.nodes and "QUANTITATIVE" in self.adf.nodes and "QUALITATIVE" in self.adf.nodes:
                    from MainClasses import Node
                    mixed_methods_node = Node("MIXED_METHODS", ["QUANTITATIVE and QUALITATIVE"], 
                                           ["MIXED_METHODS is accepted", "MIXED_METHODS is rejected"])
                    self.adf.nodes["MIXED_METHODS"] = mixed_methods_node
                    print(f"DEBUG: Created MIXED_METHODS node with children: {mixed_methods_node.children}")
                
            else:
                # Regular node question
                if question_name in nodes:
                    current_node = nodes[question_name]
                    
                    # Check if this is a DependentBLF that needs dependency checking
                    if hasattr(current_node, 'checkDependency'):
                        if not current_node.checkDependency(self.adf, self.case):
                            print(f"\nSkipping {question_name} - dependency not met")
                            continue
                    
                    # Process the node based on its type
                    if hasattr(current_node, 'resolveQuestion'):
                        # DependentBLF - resolve the question dynamically
                        question_text = current_node.resolveQuestion(self.adf)
                        print(f"\nQuestion: {question_text}")
                        
                        answer = input("Answer (y/n): ").strip().lower()
                        if answer in ['y', 'yes']:
                            self.case.append(question_name)
                            
                    elif hasattr(current_node, 'runAlgorithm'):
                        # AlgorithmicBLF - run the algorithm
                        if current_node.runAlgorithm(self):
                            self.case.append(question_name)
                            
                            # Force evaluation of abstract factors after algorithmic BLF addition
                            self._force_evaluate_abstract_factors()
                        else:
                            pass
                            
                    elif hasattr(current_node, 'evaluateSubADMs'):
                        # SubADMBLF - evaluate sub-ADMs
                        if current_node.evaluateSubADMs(self):
                            self.case.append(question_name)
                            
                            # Force evaluation of abstract factors after sub-ADM BLF addition
                            self._force_evaluate_abstract_factors()
                        else:
                            pass
                            
                    elif hasattr(current_node, 'evaluateResults'):
                        # EvaluationBLF - evaluate automatically
                        if current_node.evaluateResults(self):
                            self.case.append(question_name)
                        else:
                            pass
                            
                    else:
                        # Regular node - ask the question
                        if hasattr(current_node, 'question') and current_node.question:
                            print(f"\nQuestion: {current_node.question}")
                            
                            answer = input("Answer (y/n): ").strip().lower()
                            if answer in ['y', 'yes']:
                                self.case.append(question_name)
                        else:
                            # No question, just add to case
                            self.case.append(question_name)
                    
                    # Remove the node from the nodes dict to prevent duplicate processing
                    if question_name in nodes:
                        del nodes[question_name]
                        
                else:
                    print(f"\nWarning: Could not find {question_name} in the ADF")
        
        # Force evaluation of any remaining abstract factors
        self._force_evaluate_abstract_factors()
        
        # Final evaluation of abstract factors
        self._evaluate_abstract_factors()
        
        # Show the evaluation outcome with proper statements
        self.show_outcome()
        
        return self.case
    
    def _force_evaluate_abstract_factors(self):
        """
        Force evaluation of abstract factors immediately after BLFs are processed
        This ensures dependencies are resolved before checking them
        """
        # Find abstract factors (nodes with children that aren't in case yet)
        abstract_factors = []
        for node_name, node in self.adf.nodes.items():
            if node.children and node_name not in self.case:
                # Check if all children are in the case
                if all(child in self.case for child in node.children):
                    abstract_factors.append(node_name)
        
        # Add accepted abstract factors to the case
        for factor_name in abstract_factors:
            if factor_name not in self.case:
                self.case.append(factor_name)
    
    def _evaluate_abstract_factors(self):
        """
        Evaluate abstract factors after all BLFs have been processed
        """
        # Find abstract factors (nodes with children that aren't in case yet)
        abstract_factors = []
        for node_name, node in self.adf.nodes.items():
            if node.children and node_name not in self.case:
                # Check if all children are in the case
                if all(child in self.case for child in node.children):
                    abstract_factors.append(node_name)
        
        # Evaluate each abstract factor
        for factor_name in abstract_factors:
            try:
                # Simple evaluation: if all children are in case, add the factor
                if factor_name not in self.case:
                    self.case.append(factor_name)
            except Exception as e:
                pass
    
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
        
        print("Evaluation Results:")
        
        # Show statements for abstract factors (nodes with children)
        statement_count = 1
        for factor_name in self.case:
            if factor_name in self.adf.nodes:
                node = self.adf.nodes[factor_name]
                if hasattr(node, 'children') and node.children:
                    # This is an abstract factor, show its acceptance statement
                    if hasattr(node, 'statement') and node.statement and len(node.statement) > 0:
                        print(f"{statement_count}. {factor_name}: {node.statement[0]}")
                        statement_count += 1
        
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