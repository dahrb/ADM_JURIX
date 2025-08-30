#!/usr/bin/env python3
"""
Modern Web UI for ADM (Argumentation Decision Framework)
A responsive, dynamic interface for the ADM program
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_socketio import SocketIO, emit
import json
import os
import tempfile
import base64
from io import BytesIO
import uuid
import threading
import time

# Import the ADM classes
from MainClasses import *
from inventive_step_ADM import adf

app = Flask(__name__)
app.config['SECRET_KEY'] = 'adm-secret-key-2024'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variables for session management
sessions = {}

class ADMSession:
    """Manages an ADM session for a user"""
    
    def __init__(self, session_id):
        self.session_id = session_id
        self.adf = adf()  # Create the ADM instance
        self.current_question_index = 0
        self.answers = {}
        self.case = []
        self.evaluation_complete = False
        self.results = []
        self.graph_data = None
        self.created_at = time.time()
        
    def get_current_question(self):
        """Get the current question to ask the user"""
        # Check if we have pending factual questions first
        if hasattr(self, 'pending_factual_questions') and self.pending_factual_questions:
            # Return the next factual question
            if hasattr(self, 'current_factual_questions') and self.current_factual_questions:
                # Get the next factual question
                for fact_name, question_text in self.current_factual_questions.items():
                    if fact_name not in self.factual_answers:
                        return {
                            'type': 'factual_ascription',
                            'name': f"{self.current_factual_blf}_{fact_name}",
                            'question': question_text,
                            'blf_name': self.current_factual_blf,
                            'fact_name': fact_name
                        }
            
            # If all factual questions are answered, clear the flag and continue
            self.pending_factual_questions = False
            self.current_factual_blf = None
            self.current_factual_questions = None
            self.factual_answers = None
        
        if self.current_question_index >= len(self.adf.questionOrder):
            return None
            
        question_name = self.adf.questionOrder[self.current_question_index]
        
        # Handle question instantiators
        if question_name in self.adf.question_instantiators:
            instantiator = self.adf.question_instantiators[question_name]
            return {
                'type': 'instantiator',
                'name': question_name,
                'question': instantiator['question'],
                'choices': list(instantiator['blf_mapping'].keys()),
                'factual_ascription': instantiator.get('factual_ascription', {})
            }
        
        # Handle regular nodes
        node = self.adf.nodes.get(question_name)
        if node:
            if hasattr(node, 'algorithm_config') and node.algorithm_config:
                return {
                    'type': 'algorithmic',
                    'name': question_name,
                    'questions': node.algorithm_config['input_questions']
                }
            elif hasattr(node, 'question') and node.question:
                return {
                    'type': 'simple',
                    'name': question_name,
                    'question': node.question,
                    'choices': ['Yes', 'No']
                }
            elif hasattr(node, 'sub_adf_creator'):
                return {
                    'type': 'sub_adm',
                    'name': question_name,
                    'question': f"Evaluating sub-ADM for {question_name}",
                    'source_blf': getattr(node, 'source_blf', 'unknown')
                }
        
        return None
    
    def submit_answer(self, question_name, answer):
        """Submit an answer and process it"""
        self.answers[question_name] = answer
        
        # Handle question instantiators
        if question_name in self.adf.question_instantiators:
            instantiator = self.adf.question_instantiators[question_name]
            blf_names = instantiator['blf_mapping'].get(answer, [])
            
            if isinstance(blf_names, str):
                blf_names = [blf_names]
            
            # Add the instantiated BLFs to the case
            for blf_name in blf_names:
                if blf_name not in self.case:
                    self.case.append(blf_name)
                    
                    # Handle factual ascription if present
                    if instantiator.get('factual_ascription') and blf_name in instantiator['factual_ascription']:
                        factual_questions = instantiator['factual_ascription'][blf_name]
                        # Store for later processing
                        if 'factual_questions' not in self.answers:
                            self.answers['factual_questions'] = {}
                        self.answers['factual_questions'][blf_name] = factual_questions
                        
                        # Set a flag to indicate we need to ask factual questions
                        self.pending_factual_questions = True
                        self.current_factual_blf = blf_name
                        self.current_factual_questions = factual_questions
                        self.factual_answers = {}
                        
                        # Don't move to next question yet - we need to ask factual questions first
                        return
        
        # Handle algorithmic questions
        elif question_name in self.adf.nodes:
            node = self.adf.nodes[question_name]
            if hasattr(node, 'algorithm_config') and node.algorithm_config:
                # This is an algorithmic question - we need to collect all inputs first
                # Store the answer for now, we'll process it when all inputs are collected
                if not hasattr(self, 'algorithm_inputs'):
                    self.algorithm_inputs = {}
                if question_name not in self.algorithm_inputs:
                    self.algorithm_inputs[question_name] = []
                
                self.algorithm_inputs[question_name].append(answer)
                
                # Check if we have all inputs for this algorithmic question
                expected_inputs = len(node.algorithm_config.get('input_questions', []))
                if len(self.algorithm_inputs[question_name]) >= expected_inputs:
                    # Process the algorithmic question
                    self._process_algorithmic_question(question_name, node)
                    
            elif hasattr(node, 'sub_adf_creator'):
                # This is a SubADMBLF - we need to handle it specially
                # For now, we'll auto-accept it and let the evaluation handle the sub-ADM
                # In a full implementation, you might want to ask sub-questions
                print(f"SubADMBLF {question_name} detected - auto-processing")
                # We'll let the evaluation handle this
                
            elif hasattr(node, 'question') and node.question:
                if answer == 'Yes':
                    self.case.append(question_name)
        
        # Move to next question
        self.current_question_index += 1
        
        # Check if evaluation is complete
        if self.current_question_index >= len(self.adf.questionOrder):
            self.evaluate_case()
    
    def submit_factual_ascription(self, blf_name, fact_name, answer):
        """Submit a factual ascription answer"""
        if not hasattr(self, 'factual_answers'):
            self.factual_answers = {}
        
        self.factual_answers[fact_name] = answer
        
        # Store the fact in the ADF
        if hasattr(self.adf, 'setFact'):
            self.adf.setFact(blf_name, fact_name, answer)
        elif hasattr(self.adf, 'facts'):
            if blf_name not in self.adf.facts:
                self.adf.facts[blf_name] = {}
            self.adf.facts[blf_name][fact_name] = answer
        
        # Check if all factual questions are answered
        if hasattr(self, 'current_factual_questions'):
            all_answered = True
            for fact_name_check in self.current_factual_questions.keys():
                if fact_name_check not in self.factual_answers:
                    all_answered = False
                    break
            
            if all_answered:
                # Clear the factual question state and continue
                self.pending_factual_questions = False
                self.current_factual_blf = None
                self.current_factual_questions = None
                self.factual_answers = None
    
    def _process_algorithmic_question(self, question_name, node):
        """Process a complete algorithmic question with all inputs"""
        try:
            # Get the collected inputs
            inputs = self.algorithm_inputs[question_name]
            
            # Run the algorithm function
            algorithm_func = node.algorithm_config.get('algorithm')
            if algorithm_func and callable(algorithm_func):
                algorithm_result = algorithm_func(inputs)
                
                # Check acceptance condition
                acceptance_condition = node.algorithm_config.get('acceptance_condition')
                if acceptance_condition:
                    should_accept = self._evaluate_algorithm_condition(algorithm_result, acceptance_condition)
                    
                    if should_accept:
                        self.case.append(question_name)
                        # Store the algorithm result as a fact
                        if not hasattr(self.adf, 'facts'):
                            self.adf.facts = {}
                        if question_name not in self.adf.facts:
                            self.adf.facts[question_name] = {}
                        self.adf.facts[question_name]['result'] = algorithm_result
                        self.adf.facts[question_name]['items'] = algorithm_result
                    
                    # Store the result for display
                    if not hasattr(self, 'algorithm_results'):
                        self.algorithm_results = {}
                    self.algorithm_results[question_name] = {
                        'result': algorithm_result,
                        'accepted': should_accept,
                        'inputs': inputs
                    }
                    
                    print(f"Algorithmic question {question_name} processed: {algorithm_result} (accepted: {should_accept})")
                    
        except Exception as e:
            print(f"Error processing algorithmic question {question_name}: {e}")
            # If algorithm fails, don't add to case
    
    def _evaluate_algorithm_condition(self, result, condition):
        """Evaluate algorithm acceptance conditions"""
        try:
            if condition == ">= 1":
                return len(result) >= 1 if hasattr(result, '__len__') else result >= 1
            elif condition == "> 0":
                return len(result) > 0 if hasattr(result, '__len__') else result > 0
            elif condition == "== True":
                return bool(result)
            elif condition == "== False":
                return not bool(result)
            else:
                # Try to evaluate as a Python expression
                return eval(f"{result} {condition}")
        except:
            return False
    
    def evaluate_case(self):
        """Evaluate the complete case"""
        try:
            # Generate the graph visualization
            graph = self.adf.visualiseNetworkWithSubADMs(self.case)
            
            # Save graph to temporary file and convert to base64
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            graph.write_png(temp_file.name)
            
            with open(temp_file.name, 'rb') as f:
                graph_data = base64.b64encode(f.read()).decode('utf-8')
            
            os.unlink(temp_file.name)
            
            self.graph_data = graph_data
            
            # Evaluate the case
            self.results = self.adf.evaluateTree(self.case)
            self.evaluation_complete = True
            
        except Exception as e:
            self.results = [f"Error during evaluation: {str(e)}"]
            self.evaluation_complete = True

def create_session():
    """Create a new ADM session"""
    session_id = str(uuid.uuid4())
    sessions[session_id] = ADMSession(session_id)
    return session_id

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/start_session', methods=['POST'])
def start_session():
    """Start a new ADM session"""
    session_id = create_session()
    session['session_id'] = session_id
    return jsonify({'session_id': session_id, 'redirect': url_for('evaluation')})

@app.route('/evaluation')
def evaluation():
    """Evaluation page"""
    if 'session_id' not in session or session['session_id'] not in sessions:
        return redirect(url_for('index'))
    
    adm_session = sessions[session['session_id']]
    current_question = adm_session.get_current_question()
    
    return render_template('evaluation.html', 
                         session_id=session['session_id'],
                         current_question=current_question)

@app.route('/api/question', methods=['GET'])
def get_question():
    """Get the current question for a session"""
    session_id = request.args.get('session_id')
    if session_id not in sessions:
        return jsonify({'error': 'Invalid session'}), 400
    
    adm_session = sessions[session_id]
    current_question = adm_session.get_current_question()
    
    if current_question is None:
        return jsonify({'status': 'complete'})
    
    return jsonify(current_question)

@app.route('/api/answer', methods=['POST'])
def submit_answer():
    """Submit an answer for a question"""
    data = request.get_json()
    session_id = data.get('session_id')
    question_name = data.get('question_name')
    answer = data.get('answer')
    
    if session_id not in sessions:
        return jsonify({'error': 'Invalid session'}), 400
    
    adm_session = sessions[session_id]
    adm_session.submit_answer(question_name, answer)
    
    # Get next question
    next_question = adm_session.get_current_question()
    
    if next_question is None:
        # Evaluation complete
        return jsonify({
            'status': 'complete',
            'case': adm_session.case,
            'results': adm_session.results,
            'graph_data': adm_session.graph_data
        })
    
    return jsonify({
        'status': 'next_question',
        'question': next_question
    })

@app.route('/results')
def results():
    """Results page"""
    if 'session_id' not in session or session['session_id'] not in sessions:
        return redirect(url_for('index'))
    
    adm_session = sessions[session['session_id']]
    
    if not adm_session.evaluation_complete:
        return redirect(url_for('evaluation'))
    
    return render_template('results.html',
                         case=adm_session.case,
                         results=adm_session.results,
                         graph_data=adm_session.graph_data,
                         session=adm_session)

@app.route('/api/session_info', methods=['GET'])
def get_session_info():
    """Get session information"""
    session_id = request.args.get('session_id')
    if session_id not in sessions:
        return jsonify({'error': 'Invalid session'}), 400
    
    adm_session = sessions[session_id]
    return jsonify({
        'total_questions': len(adm_session.adf.questionOrder),
        'current_question': adm_session.current_question_index + 1,
        'progress': (adm_session.current_question_index / len(adm_session.adf.questionOrder)) * 100
    })

@app.route('/api/factual_ascription', methods=['POST'])
def submit_factual_ascription():
    """Submit a factual ascription answer"""
    data = request.get_json()
    session_id = data.get('session_id')
    blf_name = data.get('blf_name')
    fact_name = data.get('fact_name')
    answer = data.get('answer')
    
    if not all([session_id, blf_name, fact_name, answer]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    session = sessions.get(session_id)
    if not session:
        return jsonify({'error': 'Session not found'}), 404
    
    # Submit the factual ascription answer
    session.submit_factual_ascription(blf_name, fact_name, answer)
    
    # Get the next question
    next_question = session.get_current_question()
    
    if next_question:
        return jsonify({
            'status': 'next_question',
            'question': next_question
        })
    else:
        return jsonify({'status': 'complete'})

@app.route('/api/restart', methods=['POST'])
def restart_session():
    """Restart the current session"""
    if 'session_id' in session and session['session_id'] in sessions:
        # Clean up old session
        del sessions[session['session_id']]
    
    session_id = create_session()
    session['session_id'] = session_id
    return jsonify({'session_id': session_id, 'redirect': url_for('evaluation')})

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
