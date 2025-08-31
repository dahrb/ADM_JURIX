"""
ADM Command Line Interface
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
        self.cases = {}
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
            
            choice = '1' #input("Enter your choice (1-2): ").strip()
            
            if choice == "1":
                self.load_existing_domain()
            elif choice == "2":
                print("Goodbye!")
                sys.exit(0)
            else:
                print("Invalid choice. Please try again.")
            
            break
    
    def load_existing_domain(self):
        """Load one of the predefined domains"""
        print("\n" + "="*50)
        print("Load Existing Domain")
        print("="*50)
        print("1. Academic Research Project")
        print("2. Back to main menu")
        print("-"*50)
        
        choice = '1'#input("Enter your choice (1-2): ").strip()
        
        if choice == "1":
            self.load_academic_research_domain()
        elif choice == "2":
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
            
            choice = '1'#input("Enter your choice (1-3): ").strip()
            
            if choice == "1":
                self.query_domain()
                return
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
        
        self.caseName = 'test'#input("Enter case name: ").strip()
        if not self.caseName:
            print("No case name provided.")
            return

        # Reset case and start questioning
        self.case = []
        self.ask_questions()
        
        print(f"Case: {self.case}")

        return

    def ask_questions(self):
        """Ask questions to build the case"""
        print("\nAnswer questions to build your case...")
        
        # Get a copy of nodes and question order
        nodes = self.adf.nodes.copy()
        question_order = self.adf.questionOrder.copy() if self.adf.questionOrder else []

        
        if question_order != []:
            while question_order:
                question_order, nodes = self.questiongen(question_order, nodes)
        
        #NO OPTION IF QUESTION ORDER NOT SPECIFIED
        else:
            print("No question order specified")

        self.show_outcome()

    def questiongen(self, question_order, nodes):
        """
        Generates questions based on the question order and current nodes
        """
        if not question_order:
            return question_order, nodes
            return question_order, nodes
        
        current_question = question_order[0]
        
        # Check if this is a question instantiator first
        if current_question in self.adf.question_instantiators:
            x = self.questionHelper(None, current_question)
            if x == 'Done':
                question_order.pop(0)
                return self.questiongen(question_order, nodes)
            else:
                return question_order, nodes
        
        # Check if this is a regular node (including DependentBLF and EvaluationBLF)
        elif current_question in self.adf.nodes:
            current_node = self.adf.nodes[current_question]
            
            # Check if this is a DependentBLF
            if hasattr(current_node, 'checkDependency'):
                return self.handleDependentBLF(current_question, current_node, question_order, nodes)
            
            # Check if this is an EvaluationBLF
            elif hasattr(current_node, 'evaluateResults'):
                return self.handleEvaluationBLF(current_question, current_node, question_order, nodes)
            
            else:
                #process regular blf
                x = self.questionHelper(current_node, current_question)
                if x == 'Done':
                    question_order.pop(0)
                    return self.questiongen(question_order, nodes)
                else:
                    return question_order, nodes
        else:
            question_order.pop(0)
            return self.questiongen(question_order, nodes)
        
  
    def questionHelper(self, current_node, current_question):
        """
        Helper method to handle individual questions
        """
        if current_node is None:
            # This is a question instantiator
            instantiator = self.adf.question_instantiators[current_question]
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
            for blf_name in blf_names:
                # Add the BLF to the case
                if blf_name not in self.case:
                    self.case.append(blf_name)
                else:
                    pass
                
                # Ask factual ascription questions if configured
                if instantiator.get('factual_ascription') and blf_name in instantiator['factual_ascription']:
                    factual_questions = instantiator['factual_ascription'][blf_name]
                    for fact_name, question in factual_questions.items():
                        answer = input(f"{question}: ").strip()
                        if answer:
                            self.adf.setFact(blf_name, fact_name, answer)
            
            return 'Done'
        else:
            # This is a regular node
            
            # Check if this is a SubADMBLF (sub-ADM evaluator)
            if hasattr(current_node, 'evaluateSubADMs'):
                return self.handleSubADMBLF(current_question, current_node)
            
            # Handle regular nodes with questions
            elif hasattr(current_node, 'question') and current_node.question:
                question_text = current_node.question
                
                # Ask the question
                answer = input(f"{question_text}\nAnswer (y/n): ").strip().lower()
                
                if answer in ['y', 'yes']:
                    if current_question not in self.case:
                        self.case.append(current_question)
                    else:
                        pass
                    return 'Done'
                elif answer in ['n', 'no']:
                    return 'Done'
                else:
                    print("Invalid answer, please answer y/n")
                    return 'Invalid'
            else:
                if current_question not in self.case:
                    self.case.append(current_question)
                else:
                    pass
                return 'Done'

    def handleDependentBLF(self, current_question, current_node, question_order, nodes):
        """
        Handles the processing of a DependentBLF node
        
        Parameters
        ----------
        current_question : str
            the name of the current question being processed
        current_node : DependentBLF
            the DependentBLF node to process
        question_order : list
            the current question order
        nodes : dict
            the current nodes dictionary
            
        Returns
        -------
        tuple: (question_order, nodes) - the updated question order and nodes
        """
        if current_node.checkDependency(self.adf, self.case):
            # Process the DependentBLF using questionHelper
            # First resolve the question template with inherited facts
            resolved_question = current_node.resolveQuestion(self.adf, self.case)
            
            x = self.questionHelper(current_node, current_question)
            if x == 'Done':
                question_order.pop(0)
                return self.questiongen(question_order, nodes)
            else:
                return question_order, nodes
        else:
        
            dependency_node_name = current_node.dependency_node
            dependency_node = self.adf.nodes[dependency_node_name]
       
            # Check if dependency node has acceptance conditions and can be evaluated
            if hasattr(dependency_node, 'acceptance') and dependency_node.acceptance:
                
                # Try to evaluate the dependency node's acceptance condition
                # This is a simplified evaluation - just check if all children are in case
                if hasattr(dependency_node, 'children') and dependency_node.children:
                    all_children_in_case = all(child in self.case for child in dependency_node.children)
                    if all_children_in_case:
                        if dependency_node_name not in self.case:
                            self.case.append(dependency_node_name)
                        else:
                            pass
                        # NEW: General automatic fact inheritance for abstract factors
                        if hasattr(self.adf, 'facts') and hasattr(self.adf, 'nodes'):
                            if (dependency_node_name in self.adf.nodes and 
                                hasattr(self.adf.nodes[dependency_node_name], 'children') and 
                                self.adf.nodes[dependency_node_name].children):
                                inherited_facts = self.adf.getInheritedFacts(dependency_node_name, self.case)
                                if inherited_facts:
                                    if dependency_node_name not in self.adf.facts:
                                        self.adf.facts[dependency_node_name] = {}
                                    for fact_name, value in inherited_facts.items():
                                        self.adf.facts[dependency_node_name][fact_name] = value
                        
                        # Now re-check if dependency is satisfied
                        if current_node.checkDependency(self.adf, self.case):
                            # Process the DependentBLF using questionHelper
                            # First resolve the question template with inherited facts
                            resolved_question = current_node.resolveQuestion(self.adf, self.case)
                            
                            x = self.questionHelper(current_node, current_question)
                            if x == 'Done':
                                question_order.pop(0)
                                return self.questiongen(question_order, nodes)
                            else:
                                return question_order, nodes
                        else:
                            question_order.pop(0)
                            return question_order, nodes
                    else:
                        question_order.pop(0)
                        return question_order, nodes
                else:
                    question_order.pop(0)
                    return question_order, nodes
            else:
                question_order.pop(0)
                return question_order, nodes

    def handleEvaluationBLF(self, current_question, current_node, question_order, nodes):
        """
        Handles the processing of an EvaluationBLF node
        
        Parameters
        ----------
        current_question : str
            the name of the current question being processed
        current_node : EvaluationBLF
            the EvaluationBLF node to process
        question_order : list
            the current question order
        nodes : dict
            the current nodes dictionary
            
        Returns
        -------
        tuple: (question_order, nodes) - the updated question order and nodes
        """
        # Call the evaluateResults method to process the evaluation
        evaluation_result = current_node.evaluateResults(self.adf)
        
        if evaluation_result:
            # Evaluation was successful, add to case
            if current_question not in self.case:
                self.case.append(current_question)
            else:
                pass
        else:
            # Evaluation failed, don't add to case
            pass
        
        # Remove from question order and continue
        question_order.pop(0)
        return self.questiongen(question_order, nodes)

    def handleSubADMBLF(self, current_question, current_node):
        """
        Handles the processing of a SubADMBLF node
        
        Parameters
        ----------
        current_question : str
            the name of the current question being processed
        current_node : SubADMBLF
            the SubADMBLF node to process
            
        Returns
        -------
        str: 'Done' if processing completed successfully
        """
        # Call the evaluateSubADMs method to process all sub-ADMs
        # This will handle the evaluation of sub-ADMs for each item
        sub_adm_result = current_node.evaluateSubADMs(self)
        
        if sub_adm_result:
            # Sub-ADM evaluation was successful, add to case
            if current_question not in self.case:
                self.case.append(current_question)
            else:
                pass
            return 'Done'
        else:
            # Sub-ADM evaluation failed, don't add to case
            return 'Done'

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