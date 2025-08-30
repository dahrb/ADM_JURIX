#!/usr/bin/env python3
"""
ADM Web Application
Web-based UI that replicates the exact functionality of the command line UI.py
"""

import os
import sys
import json
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from MainClasses import *
import WildAnimals
import inventive_step_ADM
import academic_research_ADM

# Override the built-in input function to work with our web UI
class WebInputHandler:
    def __init__(self):
        self.pending_inputs = {}
        self.current_input_index = 0
    
    def input(self, prompt):
        """Override the built-in input function"""
        # Store the input request
        input_id = f"input_{self.current_input_index}"
        self.pending_inputs[input_id] = {
            'prompt': prompt,
            'response': None
        }
        self.current_input_index += 1
        
        # For now, return a default response to allow evaluation to continue
        # This will be replaced with actual user input from the frontend
        return "surveys,interviews,documents"  # Default response for source collection
    
    def set_response(self, input_id, response):
        """Set the response for a pending input request"""
        if input_id in self.pending_inputs:
            self.pending_inputs[input_id]['response'] = response
            return True
        return False

# Create global input handler and override built-in input
input_handler = WebInputHandler()
builtin_input = input
input = input_handler.input

app = Flask(__name__)
app.secret_key = 'adm_secret_key_2024'

class WebUI:
    def __init__(self):
        self.adf = None
        self.case = []
        self.caseName = None
        self.nodes = {}  # Track remaining nodes
        self.question_order = []  # Track question order
    
    def load_wild_animals_domain(self):
        """Load the Wild Animals domain"""
        try:
            import WildAnimals
            self.adf = WildAnimals.adf()
            self.cases = WildAnimals.cases()
            print("Wild Animals domain loaded successfully!")
            return True
        except Exception as e:
            print(f"Error loading Wild Animals domain: {e}")
            return False
    
    def load_academic_research_domain(self):
        """Load the Academic Research Project domain"""
        try:
            import academic_research_ADM
            self.adf = academic_research_ADM.adf()
            self.cases = academic_research_ADM.cases()
            print("Academic Research Project domain loaded successfully!")
            return True
        except Exception as e:
            print(f"Error loading Academic Research Project domain: {e}")
            return False
    
    def start_query(self):
        """Start a new query - reset case and initialize question flow"""
        if not self.adf:
            return None
        
        # Reset case and start questioning (exactly like CLI)
        self.case = []
        self.caseName = "Custom Case"
        
        # Get a copy of nodes and question order (exactly like CLI)
        self.nodes = self.adf.nodes.copy()
        self.question_order = self.adf.questionOrder.copy() if self.adf.questionOrder else []
        
        print(f"DEBUG: Initial question order: {self.question_order}")
        print(f"DEBUG: Available nodes: {list(self.nodes.keys())}")
        
        return self.get_next_question()
    
    def get_next_question(self):
        """Get the next question following CLI logic exactly"""
        if not self.adf:
            return None
        
        # Check if we have questions in the question order
        if self.question_order:
            current_question = self.question_order[0]
            print(f"DEBUG: Processing question order item: {current_question}")
            
            # Check if this is a question instantiator
            if current_question in self.adf.question_instantiators:
                print(f"DEBUG: Found question instantiator: {current_question}")
                question_instantiator = self.adf.question_instantiators[current_question]
                
                # Handle question instantiator as dictionary (not object)
                if isinstance(question_instantiator, dict):
                    return {
                        'type': 'question_instantiator',
                        'node_name': current_question,
                        'question': question_instantiator.get('question', 'Choose your research type:'),
                        'answers': list(question_instantiator.get('blf_mapping', {}).keys())
                    }
                else:
                    # Handle as object if it has attributes
                    return {
                        'type': 'question_instantiator',
                        'node_name': current_question,
                        'question': getattr(question_instantiator, 'question', 'Choose your research type:'),
                        'answers': getattr(question_instantiator, 'answers', [])
                    }
            
            # Check if this is a regular node
            if current_question in self.adf.nodes:
                current_node = self.adf.nodes[current_question]
                print(f"DEBUG: Found node in ADF: {current_question}")
                
                # Resolve question if it's a DependentBLF (exactly like CLI)
                if hasattr(current_node, 'resolveQuestion'):
                    current_node.resolveQuestion(self.adf)
                
                # Check if this is a SubADMBLF (exactly like CLI)
                if hasattr(current_node, 'evaluateSubADMs'):
                    print(f"DEBUG: Found sub-ADM node: {current_question}")
                    print(f"DEBUG: Sub-ADM {current_question} needs user input for source collection")
                    return {
                        'type': 'sub_adm_input',
                        'node_name': current_question,
                        'prompt': 'What sources do you have access to? (comma-separated list):',
                        'needed_prompt': 'What sources do you need for your research? (comma-separated list):'
                    }
                
                # Check if this is an EvaluationBLF
                if hasattr(current_node, 'evaluateResults'):
                    print(f"DEBUG: Processing EvaluationBLF: {current_question}")
                    
                    # Store sub-ADM results in ADF facts if this is SECONDARY_SOURCES_EVALUATION
                    if current_question == 'SECONDARY_SOURCES_EVALUATION' and hasattr(self, 'sub_adm_tracking'):
                        # Convert sub-ADM tracking to ADF facts format
                        if 'PRIMARY_SOURCES' in self.sub_adm_tracking:
                            tracking = self.sub_adm_tracking['PRIMARY_SOURCES']
                            if 'answers' in tracking and 'sub_adf' in tracking:
                                # First, evaluate the sub-ADM to create the proper results
                                sub_adf = tracking['sub_adf']
                                sub_case = []
                                
                                # Process the answers to create sub-ADM case
                                for key, answer in tracking['answers'].items():
                                    source, node_type = key.split('_', 1)
                                    if answer.lower() in ['yes', 'y', 'true', '1']:
                                        sub_case.append(f"{source}_{node_type}")
                                
                                print(f"DEBUG: Sub-ADM case: {sub_case}")
                                
                                # Evaluate the sub-ADM to get the results
                                sub_statements, sub_error = sub_adf.evaluateCase(sub_case)
                                if not sub_error:
                                    print(f"DEBUG: Sub-ADM evaluation successful: {sub_statements}")
                                    
                                    # Extract NEGATIVE_RESOURCE results from sub-ADM evaluation
                                    negative_resources = []
                                    for statement in sub_statements:
                                        if "NEGATIVE_RESOURCE is accepted" in statement:
                                            # Extract the source from the statement
                                            # Statement format: "NEGATIVE_RESOURCE is accepted - secondary source"
                                            negative_resources.append("NEGATIVE_RESOURCE")
                                    
                                    print(f"DEBUG: Found negative resources: {negative_resources}")
                                    
                                    # Store the results in ADF facts for EvaluationBLF to access
                                    if negative_resources:
                                        self.adf.facts["NEGATIVE_RESOURCE"] = negative_resources
                                        print(f"DEBUG: Stored NEGATIVE_RESOURCE in ADF facts: {negative_resources}")
                                    else:
                                        print(f"DEBUG: No NEGATIVE_RESOURCE found in sub-ADM results")
                                else:
                                    print(f"DEBUG: Sub-ADM evaluation failed: {sub_error}")
                    
                    # Now evaluate the EvaluationBLF
                    result = current_node.evaluateResults(self.adf)
                    print(f"DEBUG: EvaluationBLF {current_question} result: {result}")
                    
                    if result:
                        self.case.append(current_question)
                        print(f"DEBUG: Added {current_question} to case")
                        
                        # Remove from question order and nodes
                        if current_question in self.question_order:
                            self.question_order.remove(current_question)
                        if current_question in self.nodes:
                            del self.nodes[current_question]
                        
                        # Force abstract factor evaluation
                        self._force_evaluate_abstract_factors()
                        self._setup_abstract_factor_relationships()
                        
                        return self.get_next_question()
                    else:
                        print(f"DEBUG: {current_question} rejected")
                        # Remove from question order and nodes
                        if current_question in self.question_order:
                            self.question_order.remove(current_question)
                        if current_question in self.nodes:
                            del self.nodes[current_question]
                        
                        # Force abstract factor evaluation
                        self._force_evaluate_abstract_factors()
                        self._setup_abstract_factor_relationships()
                        
                        return self.get_next_question()
                
                # Check if this is an AlgorithmicBLF
                if hasattr(current_node, 'algorithm'):
                    return {
                        'type': 'algorithmic',
                        'node_name': current_question,
                        'question': current_node.question,
                        'algorithm_config': current_node.algorithm
                    }
                
                # Regular node with yes/no question
                if hasattr(current_node, 'question') and current_node.question:
                    return {
                        'type': 'yes_no',
                        'node_name': current_question,
                        'question': current_node.question
                    }
                
                # Node without question, add to case and remove
                self.case.append(current_question)
                self.question_order.pop(0)
                self.nodes.pop(current_question, None)
                return self.get_next_question()
        
        # No question order, process remaining nodes
        print("DEBUG: No question order, processing remaining nodes")
        remaining_nodes = list(self.nodes.keys())
        
        for node_name in remaining_nodes:
            if node_name in self.adf.nodes:
                node = self.adf.nodes[node_name]
                if hasattr(node, 'question') and node.question:
                    print(f"DEBUG: Found base-level node: {node_name}")
                    return {
                        'type': 'yes_no',
                        'node_name': node_name,
                        'question': node.question
                    }
        
        print("DEBUG: No current node found, ending questions")
        # Return case evaluation response instead of None
        return {
            'type': 'case_evaluation',
            'message': 'All questions completed. Case evaluation ready.'
        }
    
    def get_factor_display_name(self, factor_name):
        """Get a meaningful display name for a factor"""
        if not self.adf or factor_name not in self.adf.nodes:
            return factor_name
        
        node = self.adf.nodes[factor_name]
        
        # Map common factor names to meaningful descriptions
        factor_mappings = {
            'QUANTITATIVE': 'Quantitative Methods',
            'QUALITATIVE': 'Qualitative Methods', 
            'MIXED_METHODS': 'Mixed Methods Approach',
            'DATA_ANALYSIS': 'Data Analysis Methods',
            'NOVELTY': 'Research Novelty',
            'PRIMARY_SOURCES': 'Primary Sources',
            'SECONDARY_SOURCES_EVALUATION': 'Secondary Sources Evaluation',
            'RESEARCH_QUALITY': 'Research Quality Assessment'
        }
        
        # Return mapped name if available, otherwise return the original
        return factor_mappings.get(factor_name, factor_name)
    
    def process_answer(self, node_name, answer, answer_type='yes_no', algorithm_inputs=None):
        """Process the user's answer and update the case - following CLI logic exactly"""
        if not self.adf:
            return None
        
        print(f"DEBUG: Processing answer for {node_name}: {answer} (type: {answer_type})")
        
        if answer_type == 'yes_no':
            # Handle yes/no answers for BLF nodes (exactly like CLI)
            print(f"DEBUG: Processing yes_no answer for {node_name}")
            print(f"DEBUG: Current question order before processing: {self.question_order}")
            print(f"DEBUG: Current nodes before processing: {list(self.nodes.keys())}")
            
            if answer.lower() in ['yes', 'y', 'true', '1']:
                self.case.append(node_name)
                print(f"DEBUG: Added {node_name} to case")
                
                # Show statement if available (exactly like CLI)
                if node_name in self.adf.nodes:
                    node = self.adf.nodes[node_name]
                    if hasattr(node, 'statement') and node.statement and len(node.statement) > 0:
                        print(f"DEBUG: {node.statement[0]}")
                    else:
                        print(f"DEBUG: {node_name} is accepted")
            else:
                # Show rejection statement if available (exactly like CLI)
                if node_name in self.adf.nodes:
                    node = self.adf.nodes[node_name]
                    if hasattr(node, 'statement') and node.statement and len(node.statement) > 1:
                        print(f"DEBUG: {node.statement[1]}")
                    elif hasattr(node, 'statement') and node.statement and len(node.statement) > 0:
                        print(f"DEBUG: {node.statement[0]}")
                    else:
                        print(f"DEBUG: {node_name} is rejected")
            
            # Force evaluation of abstract factors after BLF instantiation (exactly like CLI)
            self._force_evaluate_abstract_factors()
            
            # Remove from question order and nodes (exactly like CLI)
            print(f"DEBUG: Attempting to remove {node_name} from question order")
            print(f"DEBUG: Question order contains {node_name}: {node_name in self.question_order}")
            if node_name in self.question_order:
                self.question_order.remove(node_name)
                print(f"DEBUG: Successfully removed {node_name} from question order after yes_no answer")
            else:
                print(f"DEBUG: WARNING: {node_name} not found in question order!")
                print(f"DEBUG: Current question order: {self.question_order}")
            
            if node_name in self.nodes:
                self.nodes.pop(node_name, None)
                print(f"DEBUG: Removed {node_name} from self.nodes after yes_no answer")
            
            print(f"DEBUG: Question order after removal: {self.question_order}")
            print(f"DEBUG: Nodes after removal: {list(self.nodes.keys())}")
            
        elif answer_type == 'multiple_choice':
            # This is a question instantiator - handle exactly like CLI
            if node_name in self.adf.question_instantiators:
                instantiator = self.adf.question_instantiators[node_name]
                blf_names = instantiator['blf_mapping'].get(answer, [])
                if isinstance(blf_names, str):
                    blf_names = [blf_names]
                
                # Add the selected BLFs to the case (exactly like CLI)
                for blf_name in blf_names:
                    if blf_name not in self.case:
                        self.case.append(blf_name)
                        print(f"DEBUG: Added {blf_name} to case")
                
                # Ask factual ascription questions if configured (exactly like CLI)
                needs_factual_ascription = False
                factual_config = {}
                
                if 'factual_ascription' in instantiator:
                    factual_ascription = instantiator['factual_ascription']
                    for blf_name in blf_names:
                        if blf_name in factual_ascription:
                            needs_factual_ascription = True
                            factual_config[blf_name] = factual_ascription[blf_name]
                
                if needs_factual_ascription:
                    # Remove from question order even when factual ascriptions are needed (exactly like CLI)
                    if node_name in self.question_order:
                        self.question_order.remove(node_name)
                        print(f"DEBUG: Removed {node_name} from question order (factual ascriptions needed)")
                    
                    return {
                        'needs_factual_ascription': True,
                        'blf_names': blf_names,
                        'factual_config': factual_config,
                        'question_instantiator_name': node_name
                    }
                else:
                    # Remove the question instantiator from both places (exactly like CLI)
                    if node_name in self.adf.question_instantiators:
                        del self.adf.question_instantiators[node_name]
                    
                    # Remove from question order if it's there (exactly like CLI)
                    if node_name in self.question_order:
                        self.question_order.remove(node_name)
                        print(f"DEBUG: Removed {node_name} from question order")
                    
                    # Force evaluation and setup relationships (exactly like CLI)
                    self._force_evaluate_abstract_factors()
                    self._setup_abstract_factor_relationships()
            
        elif answer_type == 'algorithmic':
            if algorithm_inputs:
                # Run the algorithm with the provided inputs (exactly like CLI)
                if node_name in self.adf.nodes:
                    node = self.adf.nodes[node_name]
                    if hasattr(node, 'runAlgorithm'):
                        try:
                            result = node.runAlgorithm(algorithm_inputs)
                            if result:
                                self.case.append(node_name)
                                print(f"DEBUG: Algorithm succeeded, added {node_name} to case")
                        except Exception as e:
                            print(f"DEBUG: Algorithm failed: {e}")
            
            # Force evaluation of abstract factors after algorithmic answers (exactly like CLI)
            self._force_evaluate_abstract_factors()
            
        elif answer_type == 'sub_adm':
            # Handle sub-ADM questions exactly like CLI - call evaluateSubADMs
            print(f"DEBUG: Processing sub-ADM node: {node_name}")
            if node_name in self.adf.nodes:
                node = self.adf.nodes[node_name]
                if hasattr(node, 'evaluateSubADMs'):
                    try:
                        # Pass self as the ui_instance parameter like CLI does
                        result = node.evaluateSubADMs(self)
                        if result:
                            self.case.append(node_name)
                            print(f"DEBUG: Sub-ADM evaluation succeeded, added {node_name} to case")
                        else:
                            print(f"DEBUG: Sub-ADM evaluation failed")
                    except Exception as e:
                        print(f"DEBUG: Sub-ADM evaluation failed: {e}")
            
            # Force evaluation of abstract factors after sub-ADM answers (exactly like CLI)
            self._force_evaluate_abstract_factors()
            
        elif answer_type == 'evaluation':
            # For evaluation BLFs, just add to case (no forced evaluation)
            if answer.lower() in ['yes', 'y', 'true', '1']:
                self.case.append(node_name)
                print(f"DEBUG: Added {node_name} to case")
            # Note: No _force_evaluate_abstract_factors() call here, matching CLI behavior
        
        print(f"DEBUG: Current case after processing answer: {self.case}")
        
        # Remove the processed node from self.nodes if it's there
        if node_name in self.nodes:
            self.nodes.pop(node_name)
            print(f"DEBUG: Removed {node_name} from self.nodes after processing")
        
        return None
    
    def process_sub_adm_input(self, node_name, available_sources, needed_sources):
        """Process sub-ADM input and set up sub-ADM question tracking for one-at-a-time questioning"""
        if not self.adf or node_name not in self.adf.nodes:
            return False
        
        print(f"DEBUG: Processing sub-ADM input for {node_name}")
        print(f"DEBUG: Available sources: {available_sources}")
        print(f"DEBUG: Needed sources: {needed_sources}")
        
        # Calculate missing sources (this is what the CLI does)
        available_list = [item.strip() for item in available_sources.split(',') if item.strip()]
        needed_list = [item.strip() for item in needed_sources.split(',') if item.strip()]
        missing_sources = [item for item in needed_list if item not in available_list]
        
        print(f"DEBUG: Available sources: {available_list}")
        print(f"DEBUG: Needed sources: {needed_list}")
        print(f"DEBUG: Missing sources: {missing_sources}")
        
        # Get the sub-ADM node
        current_node = self.adf.nodes[node_name]
        
        # Now set up sub-ADM question tracking for one-at-a-time questioning
        # This mimics what the CLI does - it asks sub-ADM questions one at a time
        if missing_sources:
            # Create the sub-ADF
            sub_adf = current_node.sub_adf_creator() if hasattr(current_node, 'sub_adf_creator') else None
            
            if sub_adf:
                # Set up sub-ADM question tracking
                if not hasattr(self, 'sub_adm_tracking'):
                    self.sub_adm_tracking = {}
                
                # Generate all questions but store them for sequential access
                all_questions = self._get_sub_adm_questions(sub_adf, missing_sources)
                
                self.sub_adm_tracking[node_name] = {
                    'questions': all_questions,
                    'current_index': 0,
                    'completed': False,
                    'sub_adf': sub_adf
                }
                
                # Return the first question
                return {
                    'type': 'sub_adm_question',
                    'node_name': node_name,
                    'question': all_questions[0],
                    'total_questions': len(all_questions),
                    'current_question': 1
                }
            else:
                print(f"DEBUG: No sub-ADF creator found for {node_name}")
                return False
        else:
            # No missing sources, add to case and continue
            self.case.append(node_name)
            print(f"DEBUG: No missing sources, adding {node_name} to case")
            
            # Remove from question order and nodes
            if node_name in self.question_order:
                self.question_order.remove(node_name)
            self.nodes.pop(node_name, None)
            
            return True
    
    def _get_sub_adm_questions(self, sub_adf, sources):
        """Get the questions for each source in the sub-ADM"""
        questions = []
        
        for source in sources:
            # For each source, we need to ask the sub-ADM questions
            # This mimics what the CLI does when it processes sub-ADMs
            source_questions = []
            
            # Get the BLF questions from the sub-ADF
            for node_name, node in sub_adf.nodes.items():
                if hasattr(node, 'question') and node.question:
                    # Resolve the question template with the source
                    question_text = node.question.replace('{item}', source)
                    source_questions.append({
                        'source': source,
                        'node_name': node_name,
                        'question': question_text,
                        'type': 'yes_no'
                    })
            
            questions.extend(source_questions)
        
        return questions
    
    def complete_factual_ascription(self, question_instantiator_name):
        """Complete factual ascription for a question instantiator - following CLI logic exactly"""
        print(f"DEBUG: Completing factual ascription for {question_instantiator_name}")
        
        # Remove the question instantiator from ADF (exactly like CLI)
        if question_instantiator_name in self.adf.question_instantiators:
            del self.adf.question_instantiators[question_instantiator_name]
            print(f"DEBUG: Removed {question_instantiator_name} from ADF question instantiators")
        
        # Force evaluation and setup relationships (exactly like CLI)
        self._force_evaluate_abstract_factors()
        self._setup_abstract_factor_relationships()
        
        print(f"DEBUG: Factual ascription completed for {question_instantiator_name}")
        return True, f"Factual ascription completed for {question_instantiator_name}"

    def _force_evaluate_abstract_factors(self):
        """Force evaluation of abstract factors - following CLI logic exactly"""
        print("DEBUG: Forcing evaluation of abstract factors...")
        
        # Check all abstract factors (nodes with children)
        for node_name, node in list(self.nodes.items()):
            if hasattr(node, 'children') and node.children:
                # Check if all children are in the case
                if all(child in self.case for child in node.children):
                    if node_name not in self.case:
                        self.case.append(node_name)
                        print(f"DEBUG: Added abstract factor {node_name} to case")
                    
                    # Remove from nodes since it's been evaluated
                    self.nodes.pop(node_name, None)
                    print(f"DEBUG: Removed evaluated abstract factor {node_name} from nodes")
        
        print(f"DEBUG: Case after abstract factor evaluation: {self.case}")

    def _setup_abstract_factor_relationships(self):
        """Setup relationships between abstract factors - following CLI logic exactly"""
        print("DEBUG: Setting up abstract factor relationships...")
        
        # This would handle any additional setup needed for abstract factors
        # For now, just log that we're doing this step
        pass

    def process_factual_ascription(self, blf_name, fact_name, value):
        """
        Process factual ascription answer and store it in the ADF
        
        Parameters
        ----------
        blf_name : str
            the name of the BLF
        fact_name : str
            the name of the fact
        value : str
            the value of the fact
        """
        if not self.adf:
            return False, "No domain loaded"
        
        try:
            self.adf.setFact(blf_name, fact_name, value)
            return True, f"Fact {fact_name}: {value} stored for {blf_name}"
        except Exception as e:
            return False, f"Error storing fact: {e}"
    
    def evaluate_case(self):
        """Evaluate the final case - following CLI logic exactly"""
        if not self.adf:
            return None, "No domain loaded"
        
        try:
            # Get statements for all nodes in the case
            statements = []
            for node_name in self.case:
                if node_name in self.adf.nodes:
                    node = self.adf.nodes[node_name]
                    if hasattr(node, 'statement') and node.statement:
                        if len(node.statement) > 0:
                            statements.append(f"{node_name}: {node.statement[0]}")
                        else:
                            statements.append(f"{node_name}: Accepted")
                    else:
                        statements.append(f"{node_name}: Accepted")
            
            return statements, None
        except Exception as e:
            return None, str(e)
    
    def get_visualization(self, case=None):
        """Generate visualization of the domain"""
        if not self.adf:
            return None, "No domain loaded"
        
        try:
            if case:
                graph = self.adf.visualiseNetworkWithSubADMs(case)
            else:
                graph = self.adf.visualiseNetworkWithSubADMs()
            
            # Convert to PNG and return as base64
            import base64
            import io
            
            # Save to bytes buffer
            png_data = graph.write_png()
            
            # Convert to base64
            base64_data = base64.b64encode(png_data).decode('utf-8')
            
            return base64_data, None
        except Exception as e:
            return None, f"Error generating visualization: {e}"

    def get_next_sub_adm_question(self, node_name):
        """Get the next sub-ADM question for sequential questioning"""
        if not hasattr(self, 'sub_adm_tracking') or node_name not in self.sub_adm_tracking:
            return None
        
        tracking = self.sub_adm_tracking[node_name]
        current_index = tracking['current_index']
        questions = tracking['questions']
        
        if current_index >= len(questions):
            # All questions completed
            tracking['completed'] = True
            return None
        
        # Return the current question
        question = questions[current_index]
        return {
            'type': 'sub_adm_question',
            'node_name': node_name,
            'question': question,
            'total_questions': len(questions),
            'current_question': current_index + 1
        }
    
    def process_sub_adm_answer(self, question_instantiator_name, source, node_name, answer):
        """Process answer to a sub-ADM BLF question and advance to the next question"""
        if not hasattr(self, 'sub_adm_tracking') or question_instantiator_name not in self.sub_adm_tracking:
            return False
        
        tracking = self.sub_adm_tracking[question_instantiator_name]
        
        # Store the answer
        key = f"{source}_{node_name}"
        if 'answers' not in tracking:
            tracking['answers'] = {}
        tracking['answers'][key] = answer
        
        print(f"DEBUG: Stored answer: {key} = {answer}")
        print(f"DEBUG: Current tracking: {tracking}")
        
        # Advance to the next question
        tracking['current_index'] += 1
        
        # Check if we've completed all questions
        if tracking['current_index'] >= len(tracking['questions']):
            tracking['completed'] = True
            print(f"DEBUG: All sub-ADM questions completed for {question_instantiator_name}")
            
            # Add the sub-ADM node to the case since all questions are answered
            if question_instantiator_name not in self.case:
                self.case.append(question_instantiator_name)
                print(f"DEBUG: Added {question_instantiator_name} to case after completing sub-ADM questions")
            
            # Remove from question order and nodes
            if question_instantiator_name in self.question_order:
                self.question_order.remove(question_instantiator_name)
            self.nodes.pop(question_instantiator_name, None)
            
            # Clean up tracking
            del self.sub_adm_tracking[question_instantiator_name]
            
            return True
        
        return True

# Global web UI instance
web_ui = WebUI()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/load_domain', methods=['POST'])
def load_domain():
    """Load a domain"""
    # Handle both form data and JSON data
    if request.is_json:
        data = request.get_json()
        domain_type = data.get('domain_type')
    else:
        domain_type = request.form.get('domain_type')
    
    if domain_type == 'wild_animals':
        success = web_ui.load_wild_animals_domain()
        if success:
            return jsonify({'success': True, 'message': 'Wild Animals domain loaded successfully!'})
        else:
            return jsonify({'success': False, 'message': 'Failed to load Wild Animals domain'})
    elif domain_type == 'academic_research':
        success = web_ui.load_academic_research_domain()
        if success:
            return jsonify({'success': True, 'message': 'Academic Research Project domain loaded successfully!'})
        else:
            return jsonify({'success': False, 'message': 'Failed to load Academic Research Project domain'})
    else:
        return jsonify({'success': False, 'message': 'Invalid domain type'})

@app.route('/start_query', methods=['GET'])
def start_query():
    """Start a new query"""
    if not web_ui.adf:
        return jsonify({'success': False, 'message': 'No domain loaded'})
    
    question_data = web_ui.start_query()
    
    if question_data:
        return jsonify({
            'success': True,
            'question': question_data
        })
    else:
        return jsonify({
            'success': True,
            'completed': True,
            'message': 'No more questions'
        })

@app.route('/get_question', methods=['GET'])
def get_question():
    """Get the next question"""
    if not web_ui.adf:
        return jsonify({'success': False, 'message': 'No domain loaded'})
    
    question_data = web_ui.get_next_question()
    
    if question_data:
        return jsonify({
            'success': True,
            'question': question_data
        })
    else:
        return jsonify({
            'success': True,
            'completed': True,
            'message': 'No more questions'
        })

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    """Submit an answer to a question"""
    if not web_ui.adf:
        return jsonify({'success': False, 'message': 'No domain loaded'})
    
    data = request.get_json()
    node_name = data.get('node_name')
    answer = data.get('answer')
    answer_type = data.get('answer_type', 'yes_no')
    algorithm_inputs = data.get('algorithm_inputs')
    
    result = web_ui.process_answer(node_name, answer, answer_type, algorithm_inputs)
    
    # Check if this is a factual ascription response
    if isinstance(result, dict) and result.get('needs_factual_ascription'):
        return jsonify({
            'success': True, 
            'needs_factual_ascription': True,
            'blf_names': result['blf_names'],
            'factual_config': result['factual_config'],
            'question_instantiator_name': result['question_instantiator_name']
        })
    
    # Normal response - process_answer now returns None on success
    if result is None:
        return jsonify({'success': True, 'message': 'Answer processed successfully'})
    else:
        return jsonify({'success': False, 'message': str(result)})

@app.route('/submit_factual_ascription', methods=['POST'])
def submit_factual_ascription():
    """Submit a factual ascription answer"""
    if not web_ui.adf:
        return jsonify({'success': False, 'message': 'No domain loaded'})
    
    data = request.get_json()
    blf_name = data.get('blf_name')
    fact_name = data.get('fact_name')
    value = data.get('value')
    
    success, message = web_ui.process_factual_ascription(blf_name, fact_name, value)
    
    if success:
        return jsonify({'success': True, 'message': message})
    else:
        return jsonify({'success': False, 'message': message})

@app.route('/complete_factual_ascription', methods=['POST'])
def complete_factual_ascription():
    """Complete factual ascription processing"""
    if not web_ui.adf:
        return jsonify({'success': False, 'message': 'No domain loaded'})
    
    data = request.get_json()
    question_instantiator_name = data.get('question_instantiator_name')
    
    if not question_instantiator_name:
        return jsonify({'success': False, 'message': 'No question instantiator name provided'})
    
    success, message = web_ui.complete_factual_ascription(question_instantiator_name)
    
    if success:
        return jsonify({'success': True, 'message': message})
    else:
        return jsonify({'success': False, 'message': message})

@app.route('/visualize')
def visualize():
    """Generate visualization"""
    if not web_ui.adf:
        return jsonify({'success': False, 'message': 'No domain loaded'})
    
    base64_data, error = web_ui.get_visualization(web_ui.case if web_ui.case else None)
    
    if error:
        return jsonify({'success': False, 'message': error})
    
    return jsonify({
        'success': True, 
        'image_data': base64_data,
        'filename': f"{web_ui.adf.name}.png"
    })

@app.route('/get_case_status')
def get_case_status():
    """Get current case status"""
    if not web_ui.adf:
        return jsonify({'success': False, 'message': 'No domain loaded'})
    
    return jsonify({
        'success': True,
        'case': web_ui.case,
        'case_name': web_ui.caseName,
        'domain_name': web_ui.adf.name
    })

@app.route('/get_case_evaluation', methods=['GET'])
def get_case_evaluation():
    """Get the final case evaluation data"""
    if not web_ui.adf:
        return jsonify({'success': False, 'message': 'No domain loaded'})
    
    try:
        # Get case evaluation data
        statements, error = web_ui.evaluate_case()
        if error:
            return jsonify({'success': False, 'message': error})
        
        # Get visualization
        visualization, viz_error = web_ui.get_visualization(web_ui.case)
        
        # Get meaningful factor names
        meaningful_case = []
        for factor in web_ui.case:
            display_name = web_ui.get_factor_display_name(factor)
            meaningful_case.append({
                'original_name': factor,
                'display_name': display_name
            })
        
        return jsonify({
            'success': True,
            'case': meaningful_case,
            'statements': statements,
            'visualization': visualization if not viz_error else None
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error getting case evaluation: {e}'})

@app.route('/debug_state', methods=['GET'])
def debug_state():
    """Debug endpoint to check current state"""
    if not web_ui.adf:
        return jsonify({'success': False, 'message': 'No domain loaded'})
    
    return jsonify({
        'success': True,
        'case': web_ui.case,
        'question_order': web_ui.question_order,
        'nodes': list(web_ui.nodes.keys()),
        'question_instantiators': list(web_ui.adf.question_instantiators.keys()) if hasattr(web_ui.adf, 'question_instantiators') else [],
        'all_nodes': list(web_ui.adf.nodes.keys())
    })

@app.route('/submit_sub_adm_input', methods=['POST'])
def submit_sub_adm_input():
    """Submit sub-ADM input and process the sub-ADM node"""
    if not web_ui.adf:
        return jsonify({'success': False, 'message': 'No domain loaded'})
    
    data = request.get_json()
    node_name = data.get('node_name')
    available_sources = data.get('available_sources', '')
    needed_sources = data.get('needed_sources', '')
    
    if not node_name:
        return jsonify({'success': False, 'message': 'Missing node name'})
    
    print(f"DEBUG: Received sub-ADM input for {node_name}")
    print(f"DEBUG: Available: {available_sources}, Needed: {needed_sources}")
    
    # Process the sub-ADM input
    result = web_ui.process_sub_adm_input(node_name, available_sources, needed_sources)
    
    if result:
        # Check if the result is a dictionary indicating sub-ADM questions
        if isinstance(result, dict) and result.get('type') == 'sub_adm_question':
            return jsonify({
                'success': True,
                'message': 'Sub-ADM input processed successfully',
                'next_question': result
            })
        # Normal response - process_sub_adm_input now returns True on success
        return jsonify({'success': True, 'message': 'Sub-ADM input processed successfully'})
    else:
        return jsonify({'success': False, 'message': 'Failed to process sub-ADM input'})

@app.route('/submit_sub_adm_answer', methods=['POST'])
def submit_sub_adm_answer():
    """Submit answer to a sub-ADM BLF question"""
    if not web_ui.adf:
        return jsonify({'success': False, 'message': 'No domain loaded'})
    
    data = request.get_json()
    question_instantiator_name = data.get('question_instantiator_name')
    source = data.get('source')
    node_name = data.get('node_name')
    answer = data.get('answer')
    
    if not all([question_instantiator_name, source, node_name, answer]):
        return jsonify({'success': False, 'message': 'Missing required data'})
    
    print(f"DEBUG: Received sub-ADM answer for {question_instantiator_name}")
    print(f"DEBUG: Source: {source}, Node: {node_name}, Answer: {answer}")
    
    # Process the sub-ADM answer
    success = web_ui.process_sub_adm_answer(question_instantiator_name, source, node_name, answer)
    
    if success:
        # Check if we have more sub-ADM questions
        next_sub_adm_question = web_ui.get_next_sub_adm_question(question_instantiator_name)
        
        if next_sub_adm_question:
            # Return the next sub-ADM question
            return jsonify({
                'success': True,
                'message': 'Sub-ADM answer processed successfully',
                'next_question': next_sub_adm_question
            })
        else:
            # All sub-ADM questions completed, get the next main question
            next_question = web_ui.get_next_question()
            
            if next_question:
                return jsonify({
                    'success': True,
                    'message': 'Sub-ADM completed, moving to next main question',
                    'next_question': next_question
                })
            else:
                return jsonify({
                    'success': True,
                    'message': 'Sub-ADM completed, no more questions',
                    'completed': True
                })
    else:
        return jsonify({'success': False, 'message': 'Failed to process sub-ADM answer'})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)
