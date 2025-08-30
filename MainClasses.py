
from pythonds import Stack
import pydot

class ADF:
    """
    A class used to represent the ADF graph

    Attributes
    ----------
    name : str
        the name of the ADF
    nodes : dict
        the nodes which constitute the ADF
    reject : bool, default False
        is set to true when the reject keyword is used which lets the software know to reject the node rather than accep it when the condition is true
    nonLeaf : dict
        the nodes which are non-leaf that have children
    questionOrder : list
        an ordered list which determines which order the questions are asked in
    question : str, optional
        if the node is a base-level factor this stores the question
    statements : list
        the statements to be shown if the node is accepted or rejected
    nodeDone : list
        nodes which have been evaluated
    case : list
        the list of factors forming the case    
    
    Methods
    -------
    addNodes(name, acceptance = None, statement=None, question=None)
        allows nodes to be added to the ADF from the Node() class
    addMulti(name, acceptance, statement, question)
        allows nodes to be added to the ADF from the MultiChoice() class
    nonLeafGen()
        determines what is a non-leaf factor
    evaluateTree(case)
        evaluates the ADF for a specified case
    evaluateNode(node)
        evaluates the acceptance conditions of the node
    postfixEvaluation(acceptance)
        evaluates the individual acceptance conditions which are in postfix notation
    checkCondition(operator, op1, op2 = None):
        checks the logical conditions for the acceptance condition, returning a boolean
    checkNonLeaf(node)
        checks if a node has children which need to be evaluated before it is evaluated
    questionAssignment()
        checks if any node requires a question to be assigned
    visualiseNetwork(case=None)
        allows visualisation of the ADF
    saveNew(name)
        allows the ADF to be saved as a .xlsx file
    saveHelper(wb,name)
        helper class for saveNew which provides core functionality
    """
    
    def __init__(self, name):
        """
        Parameters
        ----------
        name : str
            the name of the ADF
        """
      
        self.name = name
        
        #dictionary of nodes --> 'name': 'node object
        self.nodes = {}
        
        self.reject = False
        
        #dictionary of nodes which have children
        self.nonLeaf = {}
        
        self.questionOrder = []
        
    def addNodes(self, name, acceptance = None, statement=None, question=None):
        """
        adds nodes to ADF
        
        Parameters
        ----------
        name : str
            the name of the node
        acceptance : list
            a list of the acceptance conditions each of which should be a string
        statement : list
            a list of the statements which will be shown if a condition is accepted or rejected
        question : str
            the question to determine whether a node is absent or present
        
        """
        
        node = Node(name, acceptance, statement, question)
        
        self.nodes[name] = node
        
        self.question = question
        
        #creates children nodes
        if node.children != None:
            for childName in node.children:
                if childName not in self.nodes:
                    node = Node(childName)
                    self.nodes[childName] = node
    
    def addMulti(self,name, acceptance, statement, question):
        """
        adds MultiChoice() nodes to the ADF
        
        Parameters
        ----------
        name : str
            the name of the node
        acceptance : list
            a list of the acceptance conditions each of which should be a string
        statement : list
            a list of the statements which will be shown if a condition is accepted or rejected
        question : str
            the question to determine whether a node is absent or present
        
        """
    
        node = MultiChoice(name, acceptance, statement, question)
        
        self.nodes[name] = node
    
    def addQuestionInstantiator(self, question, blf_mapping, factual_ascription=None, question_order_name=None):
        """
        Adds a question that can instantiate BLFs without creating additional nodes in the model
        
        Parameters
        ----------
        question : str
            the question text to ask the user
        blf_mapping : dict
            dictionary mapping answer choices to BLF names (or lists of BLF names) to instantiate
        factual_ascription : dict, optional
            dictionary mapping BLF names to additional factual questions to ask
        question_order_name : str, optional
            name to use in question order (if None, will be auto-generated)
        """
        
        # Create a unique name for this question if not provided
        if question_order_name is None:
            question_order_name = f"question_{len(self.questionOrder) + 1}"
        
        # Store the question and mapping in the ADF for later use
        if not hasattr(self, 'question_instantiators'):
            self.question_instantiators = {}
        
        self.question_instantiators[question_order_name] = {
            'question': question,
            'blf_mapping': blf_mapping,
            'factual_ascription': factual_ascription
        }
        
        # Add the question to the question order
        if question_order_name not in self.questionOrder:
            self.questionOrder.append(question_order_name)
    
    def addSubADMBLF(self, name, sub_adf_creator, source_blf, statements=None, sub_questions=None):
        """
        Adds a BLF that depends on evaluating a sub-ADM for each item
        
        Parameters
        ----------
        name : str
            the name of the BLF to be instantiated
        sub_adf_creator : function
            function that creates and returns a sub-ADM instance
        source_blf : str
            the name of the BLF that contains the list of items to evaluate
        statements : list, optional
            statements to show if the BLF is accepted or rejected
        sub_questions : dict, optional
            custom questions for sub-ADM evaluation with keys 'positive' and 'negative'
        """
        
        # Create a special node that handles sub-ADM evaluation
        node = SubADMBLF(name, sub_adf_creator, source_blf, statements or [f"{name} is accepted", f"{name} is rejected"], sub_questions)
        self.nodes[name] = node
        
        # Add to question order
        if name not in self.questionOrder:
            self.questionOrder.append(name)
    
    def addAlgorithmicQuestion(self, name, algorithm_config, statements=None):
        """
        Adds an algorithmic question that runs an algorithm to determine BLF acceptance
        
        Parameters
        ----------
        name : str
            the name of the BLF to be instantiated
        algorithm_config : dict
            configuration for the algorithm including:
            - 'input_questions': list of questions to ask user
            - 'algorithm': function or lambda that processes inputs
            - 'acceptance_condition': condition for accepting the BLF
        statements : list, optional
            statements to show if the BLF is accepted or rejected
        """
        
        # Create a special node that handles algorithmic processing
        node = AlgorithmicBLF(name, algorithm_config, statements or [f"{name} is accepted", f"{name} is rejected"])
        self.nodes[name] = node
        
        # Add to question order
        if name not in self.questionOrder:
            self.questionOrder.append(name)
    
    def addDependentBLF(self, name, dependency_node, question_template, statements, factual_ascription=None):
        """
        Adds a BLF that depends on another node and inherits its factual ascriptions
        
        Parameters
        ----------
        name : str
            the name of the BLF
        dependency_node : str
            the name of the node this BLF depends on
        question_template : str
            the question template that can reference inherited factual ascriptions
        statements : list
            the statements to show if the BLF is accepted or rejected
        factual_ascription : dict, optional
            additional factual ascriptions for this BLF
        """
        
        # Create a special node that tracks dependencies
        node = DependentBLF(name, dependency_node, question_template, statements, factual_ascription)
        self.nodes[name] = node
        
        # Add to question order
        if name not in self.questionOrder:
            self.questionOrder.append(name)
    
    def addEvaluationBLF(self, name, source_blf, evaluation_condition, statements=None):
        """
        Adds a BLF that automatically evaluates based on sub-ADM results from another BLF
        
        Parameters
        ----------
        name : str
            the name of the BLF to be instantiated
        source_blf : str
            the name of the BLF that contains the sub-ADM results to evaluate
        evaluation_condition : str
            the condition to check in the sub-ADM results (e.g., 'NEGATIVE_RESOURCE', 'POSITIVE_RESOURCE')
        statements : list, optional
            statements to show if the BLF is accepted or rejected
        """
        
        # Create a special node that handles result evaluation
        node = EvaluationBLF(name, source_blf, evaluation_condition, statements or [f"{name} is accepted", f"{name} is rejected"])
        self.nodes[name] = node
        
        # Add to question order
        if name not in self.questionOrder:
            self.questionOrder.append(name)
    
    def setFact(self, blf_name, fact_name, value):
        """
        Sets a fact for a BLF
        
        Parameters
        ----------
        blf_name : str
            the name of the BLF
        fact_name : str
            the name of the fact
        value : any
            the value of the fact
        """
        if not hasattr(self, 'facts'):
            self.facts = {}
        
        if blf_name not in self.facts:
            self.facts[blf_name] = {}
        
        self.facts[blf_name][fact_name] = value
    
    def getFact(self, blf_name, fact_name):
        """
        Gets a fact for a BLF
        
        Parameters
        ----------
        blf_name : str
            the name of the BLF
        fact_name : str
            the name of the fact
            
        Returns:
            the value of the fact, or None if not found
        """
        if hasattr(self, 'facts') and blf_name in self.facts:
            return self.facts[blf_name].get(fact_name)
        return None
    
    def getInheritedFacts(self, node_name):
        """
        Gets facts inherited from child nodes
        
        Parameters
        ----------
        node_name : str
            the name of the node to get inherited facts for
            
        Returns:
            dict: dictionary of inherited facts
        """
        inherited = {}
        
        if hasattr(self, 'facts') and node_name in self.nodes:
            node = self.nodes[node_name]
            
            if hasattr(node, 'children') and node.children:
                for child_name in node.children:
                    if hasattr(self, 'facts') and child_name in self.facts:
                        for fact_name, value in self.facts[child_name].items():
                            # Don't double the prefix - just use the fact name as is
                            inherited[fact_name] = value
            else:
                pass  # Node has no children
        else:
            pass  # Node not found or no facts attribute
        
        return inherited or {}  # Ensure we never return None
    
    def nonLeafGen(self):
        """
        determines which of the nodes is non-leaf        
        """
        
        #sets it back to an empty dictionary
        self.nonLeaf = {}
        
        #checks each node and determines if it is a non-leaf node (one with children)
        for name,node in zip(self.nodes,self.nodes.values()):
            
            #adds node to dict of nodes with children
            if node.children != None and node.children != []:
                self.nonLeaf[name] = node
            else:
                pass
                   
    def evaluateTree(self, case):
        """
        evaluates the ADF for a given case
        
        Parameters
        ----------
        case : list
            the list of factors forming the case 
        
        """
        #keep track of print statements
        self.statements = []
        #list of non-leaf nodes which have been evaluated
        self.nodeDone = []
        self.case = case
        #generates the non-leaf nodes
        self.nonLeafGen()
        #while there are nonLeaf nodes which have not been evaluated, evaluate a node in this list in ascending order  
        while self.nonLeaf != {}:
            for name,node in zip(self.nonLeaf,self.nonLeaf.values()):
                #checks if the node's children are non-leaf nodes
                if name == 'Decide' and len(self.nonLeaf) != 1:
                    pass     
                elif self.checkNonLeaf(node):
                    #adds to list of evaluated nodes
                    self.nodeDone.append(name) 
                    #checks candidate node's acceptance conditions
                    if self.evaluateNode(node):
                        #enables rejection clauses - handy for automobile
                        if self.reject != True:
                            #adds factor to case if present
                            self.case.append(name)
                        #deletes node from nonLeaf nodes
                        self.nonLeaf.pop(name)
                        if hasattr(node, 'statement') and node.statement and len(node.statement) > self.counter:
                            self.statements.append(node.statement[self.counter])
                        else:
                            self.statements.append(f"{node.name} is accepted")
                        self.reject = False
                        break
                    #if node's acceptance conditions are false                       
                    else:
                        #deletes node from nonLeaf nodes but doesn't add to case
                        self.nonLeaf.pop(name)
                        #the last statement is always the rejection statement
                        if hasattr(node, 'statement') and node.statement and len(node.statement) > 0:
                            self.statements.append(node.statement[-1])
                        else:
                            self.statements.append(f"{node.name} is rejected")
                        self.reject = False
                        break
        
        return self.statements
                                  
    def evaluateNode(self, node):
        """
        evaluates a node in respect to its acceptance conditions
        
        x will be always be a boolean value
        
        Parameters
        ----------
        node : class
            the node class to be evaluated
        
        """
        
        #for visualisation purposes - this tracks the attacking nodes
        self.vis = []
        
        #counter to index the statements to be shown to the user
        self.counter = -1
        
        #checks each acceptance condition seperately
        for i in node.acceptance:
            self.reject = False
            self.counter+=1
            x = self.postfixEvaluation(i)
            if x == True:
                return x  

        return x
    
    def postfixEvaluation(self,acceptance):
        """
        evaluates the given acceptance condition 
        
        Parameters
        ----------
        acceptance : str
            a string with the names of nodes seperated by logical operators            
        
        """
        #initialises stack of operands
        operandStack = Stack()
        #list of tokens from acceptance conditions
        tokenList = acceptance.split()
        #checks each token's acceptance conditions
        for token in tokenList:
            #checks if something is a rejection condition
            if token == 'reject':
                self.reject = True
                try:
                    if x in self.case:
                        return True
                    else:
                        return False
                except:
                    pass          
            elif token == 'not':
                operand1 = operandStack.pop()
                result = self.checkCondition(token,operand1)
                operandStack.push(result)
                self.vis.append(operand1)
                
            elif token == 'and' or token == 'or':
                operand2 = operandStack.pop()
                operand1 = operandStack.pop()
                result = self.checkCondition(token,operand1,operand2)
                operandStack.push(result)    
                                
            #for an acceptance condition with no operator 
            elif len(tokenList) == 1 or (len(tokenList) ==2 and 'reject' in tokenList):
                if 'reject' in tokenList and 'reject' != token:
                    x = token   
                else:
                    if token in self.case:
                        return True
                    else:
                        return False
            else:
                #adds the operand to the stack
                operandStack.push(token)
        
        return operandStack.pop()

    def checkCondition(self, operator, op1, op2 = None):
        """
        checks the logical condition and returns a boolean
        
        Parameters
        ----------
        operator : str
            the logical operator such as or, and, not  
        op1 : str
            the first operand
        op2 : str, optional
            the second operand
        """
        
        if operator == "or":
            if op1 in self.case or op2 in self.case or op1 == True or op2 == True:
                return True
            else:
                return False
            
        elif operator == "and":
            if op1 == True or op1 in self.case:
                if op2 in self.case or op2 == True:
                    return True 
                else: 
                    return False
            elif op2 == True or op2 in self.case:
                if op1 in self.case or op1 == True:
                    return True
                else:
                    return False   
            else:
                return False
            
        elif operator == "not":
            if op1 == True:
                return False
            if op1 == False:
                return True
            elif op1 not in self.case:
                return True
            else:
                return False
        
    def checkNonLeaf(self, node):
        """
        checks if a given node has children which need to be evaluated 
        before it can be evaluated
        
        Parameters
        ----------
        node : class
            the node class to be evaluated
        
        """
        for j in node.children:
    
            if j in self.nonLeaf:
                
                if j in self.nodeDone:
                    pass
                
                else:
                    return False

            else:
                pass

        return True
    
    def questionAssignment(self):
        """
        used by the user interface to determine whether a node needs a
        question assigning to it
        """
        for i in self.nodes.values():
            
            if i.children == None and i.question == None:
                
                return i.name  
            
        return None

    def visualiseNetwork(self,case=None):    
        """
        allows the ADF to be visualised as a graph
        
        can be for the domain with or without a case
        
        if there is a case it will highlight the nodes green which have been
        accepted and red the ones which have been rejected        
        
        Parameters
        ----------
        case : list, optional
            the list of factors constituting the case
        """
        
        #initialises the graph
        G = pydot.Dot('{}'.format(self.name), graph_type='graph')
        
        # Set graph direction to top-to-bottom for better hierarchical layout
        G.set_rankdir('TB')

        if case != None:
            # Temporarily set the case for evaluation
            original_case = getattr(self, 'case', None)
            self.case = case
            
            #checks each node
            for i in self.nodes.values():
                
                #checks if node is already in the graph
                if i not in G.get_node_list():
                    
                    #checks if the node was accepted in the case
                    if i.name in case:
                        a = pydot.Node(i.name,label=i.name,color='green')
                    else:
                        a = pydot.Node(i.name,label=i.name,color='red')
                                        
                    G.add_node(a)
                
                #creates edges between a node and its children
                if i.children != None and i.children != []:
                    
                    self.evaluateNode(i)

                    for j in i.children:
                        
                                                
                        if j not in G.get_node_list():
                            
                            if j in case:
                                a = pydot.Node(j,label=j,color='green')
                            else:
                                a = pydot.Node(j,label=j,color='red')
                            
                            G.add_node(a)
                        
                        #self.vis is a list which tracks whether a node is an attacking or defending node
                        if j in self.vis:
                            if j in case:
                                my_edge = pydot.Edge(i.name, j, color='green',label='-')
                            else:
                                my_edge = pydot.Edge(i.name, j, color='red',label='-')
                        else:
                            if j in case:
                                my_edge = pydot.Edge(i.name, j, color='green',label='+')
                            else:
                                my_edge = pydot.Edge(i.name, j, color='red',label='+')

                        G.add_edge(my_edge)
            
            # Restore original case if it existed
            if original_case is not None:
                self.case = original_case
            else:
                delattr(self, 'case')
            
            # Add dependency relationships for DependentBLF nodes
            for node_name, node in self.nodes.items():
                if hasattr(node, 'dependency_node') and node.dependency_node:
                    # Create a dotted black line from dependent node to dependency node
                    dependency_edge = pydot.Edge(node_name, node.dependency_node, 
                                               color='black', style='dotted')
                    G.add_edge(dependency_edge)
            
            # Assign ranks to ensure proper hierarchical layout
            self._assign_node_ranks(G)
        
        else:
            
            #creates self.vis if not already created
            self.evaluateTree([])
            
            #checks each node
            for i in self.nodes.values():
                
                #checks if node is already in the graph
                if i not in G.get_node_list():
                    
                    a = pydot.Node(i.name,label=i.name,color='black')

                    G.add_node(a)
                
                #creates edges between a node and its children
                if i.children != None and i.children != []:
                    
                    self.evaluateNode(i)

                    for j in i.children:
                        
                        if j not in G.get_node_list():
                            
                            a = pydot.Node(j,label=j,color='black')
                           
                            G.add_node(a)
                        
                        #self.vis is a list which tracks whether a node is an attacking or defending node
                        if j in self.vis:
                            my_edge = pydot.Edge(i.name, j, color='black',label='-')

                        else:
                            my_edge = pydot.Edge(i.name, j, color='black',label='+')

                        G.add_edge(my_edge)
            
            # Add dependency relationships for DependentBLF nodes (without case)
            for node_name, node in self.nodes.items():
                if hasattr(node, 'dependency_node') and node.dependency_node:
                    # Create a dotted black line from dependent node to dependency node
                    dependency_edge = pydot.Edge(node_name, node.dependency_node, 
                                               color='black', style='dotted')
                    G.add_edge(dependency_edge)
            
            # Assign ranks to ensure proper hierarchical layout
            self._assign_node_ranks(G)
        
        return G
    
    def visualiseNetworkWithSubADMs(self, case=None):
        """
        Creates a comprehensive visualization including main ADM and sub-ADMs side by side
        
        Parameters
        ----------
        case : list, optional
            the list of factors constituting the case
            
        Returns:
            pydot.Dot: combined graph with main ADM and sub-ADMs
        """
        # Create main graph
        main_graph = self.visualiseNetwork(case)
        
        # Create a new combined graph
        combined_graph = pydot.Dot(f'{self.name}_with_subADMs', graph_type='graph')
        combined_graph.set_rankdir('TB')  # Top to bottom for vertical layout
        
        # Add main ADM as a subgraph at the top
        main_subgraph = pydot.Subgraph('cluster_main')
        main_subgraph.set_label(f'Main ADM: {self.name}')
        
        # Copy all nodes and edges from main graph to main subgraph
        for node in main_graph.get_node_list():
            main_subgraph.add_node(node)
        for edge in main_graph.get_edge_list():
            main_subgraph.add_edge(edge)
        
        combined_graph.add_subgraph(main_subgraph)
        
        # Find and create sub-ADMs
        sub_adm_count = 0
        
        # Track which nodes use the same sub-ADM
        sub_adm_mapping = {}
        # Track which nodes should link to which sub-models
        node_to_sub_model = {}
        
        # First pass: identify all sub-ADM creators and create sub-models
        for node_name, node in self.nodes.items():
            if hasattr(node, 'sub_adf_creator'):
                # Check if this sub-ADM creator is already mapped
                sub_adm_key = str(node.sub_adf_creator)
                if sub_adm_key not in sub_adm_mapping:
                    sub_adm_count += 1
                    sub_adm_mapping[sub_adm_key] = sub_adm_count
                
                # Map this node to its sub-model
                current_sub_adm_num = sub_adm_mapping[sub_adm_key]
                node_to_sub_model[node_name] = current_sub_adm_num
                
                # Create sub-ADM instance (only if we haven't created it yet)
                if current_sub_adm_num == sub_adm_count:  # Only create once
                    try:
                        sub_adf = node.sub_adf_creator()
                        
                        # Create sub-ADM graph
                        sub_graph = sub_adf.visualiseNetwork()
                        
                        # Create a subgraph to position the sub-model to the right
                        sub_subgraph = pydot.Subgraph(f'cluster_sub_{current_sub_adm_num}')
                        sub_subgraph.set_label(f'Sub-Model {current_sub_adm_num}')
                        
                        # Create a small label node that the red lines will point to
                        # Position it closer to the main ADM
                        label_node = pydot.Node(f"sub_model_label_{current_sub_adm_num}", 
                                               label=f"SUB-MODEL {current_sub_adm_num}",
                                               shape="box",
                                               style="filled",
                                               fillcolor="lightgreen",
                                               width="1.5",
                                               height="0.5")
                        
                        # Add the label node to the main subgraph (not the combined graph)
                        # This positions it within the main ADM area, closer to the nodes
                        main_subgraph.add_node(label_node)
                        
                        # Add all nodes and edges from the sub-ADM to the subgraph
                        for sub_node in sub_graph.get_node_list():
                            sub_subgraph.add_node(sub_node)
                        for sub_edge in sub_graph.get_edge_list():
                            sub_subgraph.add_edge(sub_edge)
                        
                        combined_graph.add_subgraph(sub_subgraph)
                        
                    except Exception as e:
                        print(f"ERROR: Could not create sub-ADM for {node_name}: {e}")
                        import traceback
                        traceback.print_exc()
        
        # Second pass: identify EvaluationBLF nodes that should link to the same sub-models
        for node_name, node in self.nodes.items():
            if hasattr(node, 'source_blf') and node.source_blf in node_to_sub_model:
                # This is an EvaluationBLF that should link to the same sub-model as its source
                source_sub_model = node_to_sub_model[node.source_blf]
                node_to_sub_model[node_name] = source_sub_model
        
        # Third pass: create all connection edges
        for node_name, sub_model_num in node_to_sub_model.items():
            # Add connection edge from main BLF to the label node
            connection_edge = pydot.Edge(
                node_name,
                f"sub_model_label_{sub_model_num}",
                style='dashed',
                color='red',
                label=f'→ sub-model'
            )
            combined_graph.add_edge(connection_edge)
        
        if len(sub_adm_mapping) == 0:
            print("No sub-ADMs found in this ADM")
            return main_graph
        
        return combined_graph
    
    def _assign_node_ranks(self, G):
        """
        Assign ranks to nodes to ensure proper hierarchical layout
        DependentBLF nodes are positioned at the same level as other BLFs (bottom level)
        """
        # Create subgraphs for different ranks
        rank_0 = pydot.Subgraph(rank='same')
        rank_1 = pydot.Subgraph(rank='same')
        
        # Rank 0: Abstract factors (nodes with children) - top level
        # Rank 1: Base level factors (BLFs) and DependentBLFs - bottom level
        
        for node_name, node in self.nodes.items():
            if node.children and node.children != []:
                # Abstract factors go to rank 0 (top level)
                rank_0.add_node(pydot.Node(node_name))
            else:
                # Base level factors and DependentBLFs go to rank 1 (bottom level)
                rank_1.add_node(pydot.Node(node_name))
        
        # Add subgraphs to the main graph
        if rank_0.get_node_list():
            G.add_subgraph(rank_0)
        if rank_1.get_node_list():
            G.add_subgraph(rank_1)

class Node:
    """
    A class used to represent an individual node, whose acceptance conditions
    are instantiated by 'yes' or 'no' questions

    Attributes
    ----------
    name : str
        the name of the node
    question : str, optional
        the question which will instantiate the blf
    answers : 
        set to None type to indicate to other methods the Node is not from MultiChoice()
    acceptanceOriginal : str
        the original acceptance condition before being converted to postfix notation
    statement : list
        the statements which will be output depending on whether the node is accepted or rejected
    acceptance : list
        the acceptance condition in postfix form
    children : list
        a list of the node's children nodes
    
    Methods
    -------
    attributes(acceptance)
        sets the acceptance conditions and determines the children nodes  
    
    logicConverter(expression)
        converts the acceptance conditions into postfix notation
        
    """
    def __init__(self, name, acceptance=None, statement=None, question=None):
        """
        Parameters
        ----------
        name : str
            the name of the node
        statement : list, optional
            the statements which will be output depending on whether the node is accepted or rejected
        acceptance : list, optional
            the acceptance condition in postfix form
        question : str, optional
            the question which will instantiate the blf
        """
        #name of the node
        self.name = name
        
        #question for base leve factor
        self.question = question
        
        self.answers = None
        
        self.acceptanceOriginal = acceptance
    
        #sets postfix acceptance conditions and children nodes
        try:
            self.attributes(acceptance)
            self.statement = statement
        except:
            self.acceptance = None
            self.children = None
            self.statement = None
    
    def attributes(self, acceptance):
        """
        sets the acceptance condition and children for the node
        
        Parameters
        ----------
        acceptance : list or None
            the acceptance condition in postfix form
        """
        
        #sets acceptance condition to postfix if acceptance condition specified
        self.acceptance = []
        self.children = []
        
        # Handle None acceptance gracefully
        if acceptance is None:
            return
        
        for i in acceptance:
            self.acceptance.append(self.logicConverter(i))
        
        for i in self.acceptance:
            splitAcceptance = i.split()
            
            #sets the children nodes
            for token in splitAcceptance:
                
                if token not in ['and','or','not','reject'] and token not in self.children:
                    
                    self.children.append(token)

    def logicConverter(self, expression):
        """
        converts a logical expression from infix to postfix notation
        
        Parameters
        ----------
        expression : list
            the acceptance condition to be converted into postfix form
        """
        
        #precedent dictionary of logical operators and reject keyword
        precedent = {'(':1,'or':2,'and':3,'not':4,'reject':5}
        
        #creates the stack
        operatorStack = Stack()
        
        #splits the tokens in the logical expression
        tokenList = expression.split()
        
        #stores the postfix expression
        postfixList = []

        #checks each token in the expression and pushes or pops on the stack accordingly
        for token in tokenList:
            
            if token == '(':
                operatorStack.push(token)
            elif token == ')':
                topToken = operatorStack.pop()
                while topToken != '(':
                    postfixList.append(topToken)
                    topToken = operatorStack.pop()

                                
            elif token == 'and' or token == 'or' or token == 'not' or token == 'reject':
                while (not operatorStack.isEmpty()) and (precedent[operatorStack.peek()] >= precedent[token]):
                    postfixList.append(operatorStack.pop())
                operatorStack.push(token)
                
            else:
                postfixList.append(token)

        #while operator stack not empty pop the operators to the postfix list
        while not operatorStack.isEmpty():
            postfixList.append(operatorStack.pop())
        
        #returns the post fix expression as a string  
        return " ".join(postfixList)

class MultiChoice(Node):
    """
    for the creation of multiple choice base level factors, especially to 
    facilitate the exception to the 4th amendment and NIHL domains
    
    Methods inherited from Node()
    
    Attributes
    ----------
    name : str
        the name of the node
    question : str, optional
        the question which will instantiate the blf
    answers : list
        the multiple choice answers to be selected from
    acceptanceOriginal : str
        the original acceptance condition before being converted to postfix notation
    statement : list
        the statements which will be output depending on whether the node is accepted or rejected
    acceptance : list
        the acceptance condition in postfix form
    children : list
        a list of the node's children nodes
        
    Methods
    -------
    attributes(acceptance)
        sets the acceptance conditions and determines the children nodes  
    
    logicConverter(expression)
        converts the acceptance conditions into postfix notation
    
    """
    def __init__(self, name, acceptance, statement, question=None):
        """
        Parameters
        ----------
        name : str
            the name of the node
        statement : list, optional
            the statements which will be output depending on whether the node is accepted or rejected
        acceptance : list, optional
            the acceptance condition in postfix form
        question : str, optional
            the question which will instantiate the blf
        """
        
        #name of the node
        self.name = name
        
        #quetion for base level factor
        self.question = question
        
        self.acceptanceOriginal = acceptance

        #sets postfix acceptance conditions and children nodes
        try:
            self.attributes(acceptance)
            self.statement = statement
        except:
            self.acceptance = None
            self.children = None
            self.statement = None
                
        self.answers = self.children
  
class DependentBLF(Node):
    """
    A BLF that depends on another node and inherits its factual ascriptions
    
    Attributes
    ----------
    name : str
        the name of the BLF
    dependency_node : str
        the name of the node this BLF depends on
    question_template : str
        the question template that can reference inherited factual ascriptions
    statements : list
        the statements to show if the BLF is accepted or rejected
    factual_ascription : dict
        additional factual ascriptions for this BLF
    """
    
    def __init__(self, name, dependency_node, question_template, statements, factual_ascription=None):
        """
        Parameters
        ----------
        name : str
            the name of the BLF
        dependency_node : str
            the name of the node this BLF depends on
        question_template : str
            the question template that can reference inherited factual ascriptions
        statements : list
            the statements to show if the BLF is accepted or rejected
        factual_ascription : dict, optional
            additional factual ascriptions for this BLF
        """
        
        # Initialize as a regular Node but with special dependency handling
        super().__init__(name, None, statements, question_template)
        
        self.dependency_node = dependency_node
        self.factual_ascription = factual_ascription or {}
        
        # Override the question to be dynamic
        self.question_template = question_template
        self.question = question_template  # Will be resolved dynamically
    
    def resolveQuestion(self, adf):
        """
        Resolves the question template by replacing placeholders with inherited facts
        
        Parameters
        ----------
        adf : ADF
            the ADF instance to get facts from
        """
        question_text = self.question_template
        
        # Get inherited facts from the dependency node
        inherited = adf.getInheritedFacts(self.dependency_node)
        
        # Safety check: ensure inherited is a dictionary
        if not isinstance(inherited, dict):
            print(f"DEBUG: Warning: getInheritedFacts returned {type(inherited)} instead of dict for {self.dependency_node}")
            inherited = {}
        
        # Replace placeholders in the question template
        # This is now generic - any placeholder like {ICE_CREAM_flavour} will be replaced
        for key, value in inherited.items():
            placeholder = "{" + key + "}"
            if placeholder in question_text:
                question_text = question_text.replace(placeholder, str(value))
        
        # Clean up any remaining unresolved placeholders and format the question nicely
        import re
        # Remove any remaining {placeholder} patterns
        question_text = re.sub(r'\{[^}]+\}', '', question_text)
        # Clean up extra commas and spaces
        question_text = question_text.replace(', ,', ',')
        question_text = question_text.replace(', ,', ',')  # Handle double commas
        question_text = question_text.replace('  ', ' ')  # Handle double spaces
        question_text = question_text.strip()
        # Remove trailing comma if it exists
        if question_text.endswith(','):
            question_text = question_text[:-1]
        
        self.question = question_text
        return question_text
    
    def checkDependency(self, adf, case):
        """
        Checks if the dependency node is satisfied
        
        Parameters
        ----------
        adf : ADF
            the ADF instance
        case : list
            the current case
            
        Returns:
            bool: True if dependency is satisfied, False otherwise
        """
        return self.dependency_node in case

class SubADMBLF(Node):
    """
    A BLF that depends on evaluating a sub-ADM for each item from another BLF
    
    Attributes
    ----------
    name : str
        the name of the BLF
    sub_adf_creator : function
        function that creates and returns a sub-ADM instance
    source_blf : str
        the name of the BLF that contains the list of items to evaluate
    statements : list
        statements to show if the BLF is accepted or rejected
    sub_questions : dict, optional
        custom questions for sub-ADM evaluation with keys 'positive' and 'negative'
    """
    
    def __init__(self, name, sub_adf_creator, source_blf, statements, sub_questions=None):
        """
        Parameters
        ----------
        name : str
            the name of the BLF
        sub_adf_creator : function
            function that creates and returns a sub-ADM instance
        source_blf : str
            the name of the BLF that contains the list of items to evaluate
        statements : list
            statements to show if the BLF is accepted or rejected
        sub_questions : dict, optional
            custom questions for sub-ADM evaluation with keys 'positive' and 'negative'
        """
        
        # Ensure statements is a list
        if statements is None:
            statements = [f"{name} is accepted", f"{name} is rejected"]
        
        # Initialize as a regular Node
        super().__init__(name, None, statements, None)
        
        # Override the statement that might have been set to None by the parent constructor
        self.statement = statements
        
        self.sub_adf_creator = sub_adf_creator
        self.source_blf = source_blf
        self.sub_adf_results = {}
        
        # Set default questions if none provided
        self.sub_questions = sub_questions or {
            'positive': 'Is {item} positive data?',
            'negative': 'Is {item} negative data?'
        }
        
        # Override the question to indicate this is a sub-ADM question
        self.question = f"Sub-ADM evaluation: {name}"
    
    def _get_source_items(self, ui_instance):
        """
        Gets the list of items to evaluate from the source
        
        Parameters
        ----------
        ui_instance : UI
            the UI instance to access the main ADF
            
        Returns:
            list: list of items to evaluate
        """
        # Check if source_blf is a function (callable)
        if callable(self.source_blf):
            # If source_blf is a function, call it
            return self.source_blf(ui_instance)
        elif isinstance(self.source_blf, list):
            # If source_blf is already a list, return it
            return self.source_blf
        else:
            # Try to get items from facts if source_blf is a string (BLF name)
            if hasattr(ui_instance.adf, 'getFact'):
                return ui_instance.adf.getFact(self.source_blf, 'items') or []
            return []

    def evaluateSubADMs(self, ui_instance):
        """
        Evaluates sub-ADMs for each item to determine BLF acceptance
        
        Parameters
        ----------
        ui_instance : UI
            the UI instance to access the main ADF and case
            
        Returns:
            bool: True if BLF should be accepted, False otherwise
        """
        try:
            # Get the list of items to evaluate
            items = self._get_source_items(ui_instance)
            
            if not items:
                return False
            
            positive_count = 0
            negative_count = 0
            item_results = []
            
            # Evaluate sub-ADM for each item
            for item in items:
                try:
                    # Create a new sub-ADM instance
                    sub_adf = self.sub_adf_creator()
                    
                    # Set the item name in the sub-ADM
                    if hasattr(sub_adf, 'setFact'):
                        sub_adf.setFact('ITEM', 'name', item)
                    
                    # Evaluate the sub-ADM
                    sub_result, sub_case = self._evaluateSubADM(sub_adf, item)
                    
                    self.sub_adf_results[item] = sub_result
                    item_results.append(sub_case)
                    
                    if sub_result == 'POSITIVE':
                        positive_count += 1
                    elif sub_result == 'NEGATIVE':
                        negative_count += 1
                        
                except Exception as e:
                    self.sub_adf_results[item] = 'ERROR'
                    item_results.append(['ERROR'])
            
            # Store the detailed results in the main ADF for other BLFs to access
            if hasattr(ui_instance.adf, 'setFact'):
                ui_instance.adf.setFact(self.name, 'results', item_results)
                ui_instance.adf.setFact(self.name, 'positive_count', positive_count)
                ui_instance.adf.setFact(self.name, 'negative_count', negative_count)
            
            # Determine final acceptance based on results
            if positive_count >= 1:
                return True
            else:
                return False
                
        except Exception as e:
            return False
    
    def _evaluateSubADM(self, sub_adf, item):
        """
        Evaluates a single sub-ADM for an item
        
        Parameters
        ----------
        sub_adf : ADF
            the sub-ADM instance to evaluate
        item : str
            the item name being evaluated
            
        Returns:
            str: 'POSITIVE', 'NEGATIVE', or 'UNKNOWN'
        """
        try:
            # print(f"Evaluating sub-ADM for item: {item}")
            
            # Set the item name in the sub-ADM
            if hasattr(sub_adf, 'setFact'):
                sub_adf.setFact('ITEM', 'name', item)
            
            # Ask the user the questions for this item
            case = []
            
            # Ask POSITIVE_DATA question
            positive_question = self.sub_questions['positive'].format(item=item)
            print(f"\nQuestion: {positive_question}")
            positive_answer = input("Answer (y/n): ").strip().lower()
            if positive_answer in ['y', 'yes']:
                case.append('POSITIVE_DATA')
                print(f"Added POSITIVE_DATA to case for {item}")
            
            # Ask NEGATIVE_DATA question
            negative_question = self.sub_questions['negative'].format(item=item)
            print(f"Question: {negative_question}")
            negative_answer = input("Answer (y/n): ").strip().lower()
            if negative_answer in ['y', 'yes']:
                case.append('NEGATIVE_DATA')
                print(f"Added NEGATIVE_DATA to case for {item}")
            
            print(f"Case for {item}: {case}")
            
            # Evaluate the abstract factors
            if 'POSITIVE_DATA' in case and 'NEGATIVE_DATA' not in case:
                case.append('POSITIVE_RESOURCE')
                print(f"{item} is POSITIVE (POSITIVE_DATA and not NEGATIVE_DATA)")
                return 'POSITIVE', case
            elif 'NEGATIVE_DATA' in case and 'POSITIVE_DATA' not in case:
                case.append('NEGATIVE_RESOURCE')
                print(f"{item} is NEGATIVE (NEGATIVE_DATA and not POSITIVE_DATA)")
                return 'NEGATIVE', case
            else:
                print(f"{item} is neither clearly POSITIVE nor NEGATIVE")
                return 'UNKNOWN', case
            
        except Exception as e:
            # print(f"Error in sub-ADM evaluation: {e}")
            return 'UNKNOWN', []

class AlgorithmicBLF(Node):
    """
    A BLF that uses an algorithm to determine acceptance based on user inputs
    
    Attributes
    ----------
    name : str
        the name of the BLF
    algorithm_config : dict
        configuration for the algorithm including input questions, algorithm function, and acceptance condition
    statements : list
        statements to show if the BLF is accepted or rejected
    """
    
    def __init__(self, name, algorithm_config, statements):
        """
        Parameters
        ----------
        name : str
            the name of the BLF
        algorithm_config : dict
            configuration for the algorithm
        statements : list
            statements to show if the BLF is accepted or rejected
        """
        
        # Ensure statements is a list
        if statements is None:
            statements = [f"{name} is accepted", f"{name} is rejected"]
        
        # Initialize as a regular Node but with algorithmic processing
        super().__init__(name, None, statements, None)
        
        # Override the statement that might have been set to None by the parent constructor
        self.statement = statements
        
        self.algorithm_config = algorithm_config
        self.algorithm_result = None
        
        # Override the question to indicate this is algorithmic
        self.question = f"Algorithmic question: {name}"
    
    def runAlgorithm(self, ui_instance):
        """
        Runs the algorithm to determine BLF acceptance
        
        Parameters
        ----------
        ui_instance : UI
            the UI instance to ask questions and store results
            
        Returns:
            bool: True if BLF should be accepted, False otherwise
        """
        try:
            # Get input questions and ask user
            input_questions = self.algorithm_config.get('input_questions', [])
            user_inputs = []
            
            # print(f"\nRunning algorithm for {self.name}...")
            
            for i, question in enumerate(input_questions, 1):
                # print(f"Input {i}: {question}")
                user_input = input("Answer: ").strip()
                user_inputs.append(user_input)
            
            # Run the algorithm function
            algorithm_func = self.algorithm_config.get('algorithm')
            if algorithm_func:
                self.algorithm_result = algorithm_func(user_inputs)
                # print(f"Algorithm result: {self.algorithm_result}")
            else:
                # print("Warning: No algorithm function provided")
                self.algorithm_result = None
            
            # Check acceptance condition
            acceptance_condition = self.algorithm_config.get('acceptance_condition')
            if acceptance_condition:
                if callable(acceptance_condition):
                    should_accept = acceptance_condition(self.algorithm_result)
                else:
                    # Simple condition like ">= 1" or "> 0"
                    should_accept = self._evaluateSimpleCondition(self.algorithm_result, acceptance_condition)
                
                # Display the appropriate statement
                if self.statement and len(self.statement) > 0:
                    if should_accept:
                        print(f"\n{self.statement[0]}")
                    else:
                        print(f"\n{self.statement[1] if len(self.statement) > 1 else self.statement[0]}")
                else:
                    # print(f"DEBUG: Cannot display statement - self.statement is {self.statement}")
                    pass
                
                # Store the algorithm result as a fact for other BLFs to access
                if hasattr(ui_instance, 'adf') and hasattr(ui_instance.adf, 'setFact'):
                    ui_instance.adf.setFact(self.name, 'result', self.algorithm_result)
                    # Store as 'items' fact for any algorithmic BLF
                    ui_instance.adf.setFact(self.name, 'items', self.algorithm_result)
                
                return should_accept
                
        except Exception as e:
            # print(f"Error running algorithm: {e}")
            return False
    
    def _evaluateSimpleCondition(self, result, condition):
        """
        Evaluates simple acceptance conditions like ">= 1", "> 0", etc.
        
        Parameters
        ----------
        result : any
            the result from the algorithm
        condition : str
            the condition string to evaluate
            
        Returns:
            bool: True if condition is met, False otherwise
        """
        try:
            # Handle common conditions
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
            # print(f"Could not evaluate condition '{condition}' with result '{result}'")
            return False

class EvaluationBLF(Node):
    """
    A BLF that automatically evaluates based on sub-ADM results from another BLF
    
    Attributes
    ----------
    name : str
        the name of the BLF
    source_blf : str
        the name of the BLF that contains the sub-ADM results to evaluate
    evaluation_condition : str
        the condition to check in the sub-ADM results (e.g., 'NEGATIVE_RESOURCE', 'POSITIVE_RESOURCE')
    statements : list
        statements to show if the BLF is accepted or rejected
    """
    
    def __init__(self, name, source_blf, evaluation_condition, statements):
        """
        Parameters
        ----------
        name : str
            the name of the BLF
        source_blf : str
            the name of the BLF that contains the sub-ADM results to evaluate
        evaluation_condition : str
            the condition to check in the sub-ADM results
        statements : list
            statements to show if the BLF is accepted or rejected
        """
        
        # Ensure statements is a list
        if statements is None:
            statements = [f"{name} is accepted", f"{name} is rejected"]
        
        # Initialize as a regular Node
        super().__init__(name, None, statements, None)
        
        # Override the statement that might have been set to None by the parent constructor
        self.statement = statements
        
        self.source_blf = source_blf
        self.evaluation_condition = evaluation_condition
        
        # Override the question to indicate this is an evaluation BLF
        self.question = f"Evaluation: {name} based on {source_blf} results"
    
    def evaluateResults(self, adf):
        """
        Evaluates the sub-ADM results to determine BLF acceptance
        
        Parameters
        ----------
        adf : ADF
            the ADF instance to get facts from
            
        Returns:
            bool: True if BLF should be accepted, False otherwise
        """
        try:
            # print(f"\nEvaluating {self.name} based on {self.source_blf} results...")
            
            # Get the detailed results from the source BLF
            if not hasattr(adf, 'getFact'):
                # print(f"Warning: ADF does not have getFact method")
                return False
            
            detailed_results = adf.getFact(self.source_blf, 'results')
            if not detailed_results:
                # print(f"Warning: No results found from {self.source_blf}")
                return False
            
            # print(f"Found detailed results: {detailed_results}")
            
            # Check if any item contains the evaluation condition in its detailed case
            condition_found = False
            for item_case in detailed_results:
                if isinstance(item_case, list) and self.evaluation_condition in item_case:
                    condition_found = True
                    # print(f"Found {self.evaluation_condition} in item case: {item_case}")
                    break
            
            if condition_found:
                # print(f"{self.name} is accepted (found {self.evaluation_condition} in sub-ADM results)")
                # print(f"\n{self.statement[0]}")
                return True
            else:
                # print(f"{self.name} is rejected (no {self.evaluation_condition} found in sub-ADM results)")
                # print(f"\n{self.statement[1]}")
                return False
                
        except Exception as e:
            # print(f"Error evaluating results: {e}")
            return False