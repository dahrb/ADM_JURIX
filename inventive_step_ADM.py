"""
Inventive Step ADM 
"""

from MainClasses import *

#Sub-ADM 1 
def create_sub_adm_1(item_name, key_facts=None):
    """Creates a sub-ADM """
    sub_adf = SubADM("Sub-Model 1", item_name)

    # Store key facts in the sub-ADM if provided
    if key_facts:
        sub_adf.facts = key_facts.copy()
        print(f"Sub-ADM for {item_name} initialized with {len(key_facts)} key facts")

    #blfs
    #F30 - Q17
    sub_adf.addNodes("IndependentContribution",question='Does the feature make an independent technical contribution to the invention?')

    #F31 - Q18
    sub_adf.addNodes("CombinationContribution",question='Does the feature make a contribution in combination with other technical features to the invention?')

    #F33/F34/F35/F36 - Q20
    sub_adf.addQuestionInstantiator(
    "What is the primary nature of the distinguishing feature?",
    {
        "A computer simulation.": "ComputerSimulation",
        "The processing of numerical data.": "NumericalData",
        "A mathematical method or algorithm.": "MathematicalMethod",
        "Other excluded field":"OtherExlusions",
        "None of the above":""
    },
    None,
    "nature_feat")

    #F32 - Q21
    sub_adf.addNodes("CircumventTechProblem",question='Is the feature a technical implementation of a non-technical method i.e. game rules or a business method, and does it circumvent the technical problem rather than addressing it in an inherently technical way?')

    #F41 - Q22 - ADD DEPENDENCY
    sub_adf.addNodes("TechnicalAdaptation",question='Is the feature a specific technical adaptation which is specific for that implementation in that its design is motivated by technical considerations relating to the internal functioning of the computer system or network.')

    #bridge node to make things easier
    sub_adf.addNodes("NumOrComp",["NumericalData","ComputerSimulation"],["The feature involves numercial data","The feature involves a computer simulation","The feature does involve a computer simulation or numerical data"])

    #F37 - Q23
    sub_adf.addDependentBLF("IntendedTechnicalUse","NumOrComp",
                            'Is there an intended use of the data resulting from the feature?',
                            None)
    #F38 - Q24
    sub_adf.addDependentBLF("TechUseSpecified","IntendedTechnicalUse",
                            'Is the potential technical effect of the numerical data either explicitly or implicitly specified in the claim?',
                            None)

    #F39 - Q26
    sub_adf.addDependentBLF("SpecificPurpose","MathematicalMethod",
                            'Does the technical contribution have a specific technical purpose i.e. produces a technical effect serving a technical purpose. Not merely a `generic\' purpose i.e. "controlling a technical system".',
                            None)

    #F40 - Q27
    sub_adf.addDependentBLF("FunctionallyLimited","MathematicalMethod",
                    'Is the claim functionally limited to the technical purpose stated either explicitly or implicitly?',
                    None)

    #F56 - Q28
    sub_adf.addDependentBLF("UnexpectedEffect","FeatureTechnicalContribution",
                            'Is the technical effect unexpected or surprising?',
                            None)

    #F57 - Q29
    sub_adf.addDependentBLF("PreciseTerms",["FeatureTechnicalContribution","UnexpectedEffect"],
                            'Is this unexpected effect described in precise, measurable terms?',
                            None)

    #F58 - Q30
    sub_adf.addDependentBLF("OneWayStreet",["FeatureTechnicalContribution","UnexpectedEffect"],
                            'Is the unexpected effect a result of a lack of alternatives creating a \'one-way street\' situation? i.e. for the skilled person to achieve the technical effect in question from the closest prior art, they would not have to choose from a range of possibilities, because there is only one-way to do x thing, and that would result in unexpected property y.',
                            None)

    #F42,F43
    sub_adf.addQuestionInstantiator(
    "Are the technical effects credible and/or reproducible?",
    {
        "Credible": "Credible",
        "Reproducible": "Reproducible",
        "Both": ["Credible","Reproducible"],
        "Neither": ""
    },
    None,
    "cred_repro_questions")

    sub_adf.addNodes("NonReproducible",["reject Reproducible","accept"],["the technical effect is not reproducible","the technical effect is reproducible",""])
    #F44 - Q32
    sub_adf.addDependentBLF("ClaimContainsEffect","NonReproducible",
                            'Does the claim contain the non-reproducible effect i.e. if the claim says the invention achieve effect E, but this is not reproducible.',
                            None)

    #abstract factors
    sub_adf.addNodes("AppliedInField",["SpecificPurpose and FunctionallyLimited"],["the technical contribution is applied in the field","the technical contribution is not applied in the field"])
    sub_adf.addNodes("MathematicalContribution",["MathematicalMethod and AppliedInField","MathematicalMethod and TechnicalAdaptation"],["the technical contribution is a mathematical contribution applied in the field","the technical contribution is a mathematical contribution with a specific technical adaptation","the technical contribution is not a mathematical contribution"])
    sub_adf.addNodes("ComputationalContribution",["ComputerSimulation and TechnicalAdaptation","ComputerSimulation and IntendedTechnicalUse","NumericalData and IntendedTechnicalUse","NumericalData and TechUseSpecified"],["the technical contribution is a computational contribution with a specific technical adaptation","the technical contribution is a computational contribution with an intended technical use","the technical contribution is a numerical method with an intended technical use","the technical contribution is a numerical method with a specified technical use","there is no computational or numerical technical contribution"])
    sub_adf.addNodes("ExcludedField",["ComputerSimulation","NumericalData","MathematicalMethod","OtherExclusions"],["Computer simulations are typically excluded from being inventive","Numerical data is typically excluded from being inventive","Mathematical methods are typically excluded from being inventive","The feature is part of another excluded field","The feature is not part of an excluded field"])
    sub_adf.addNodes("NormalTechnicalContribution",["reject CircumventTechProblem","reject ExcludedField","IndependentContribution","CombinationContribution"],["The feature is not a technical contribution as it circumvents a technical problem","The feature is not a normal technical contribution as it is part of an excluded field","The feature is an independent technical contribution","The feature is a technical contribution in combination with other features","the feature is not a technical contribution"])
    sub_adf.addNodes("FeatureTechnicalContribution",["NormalTechnicalContribution","ComputationalContribution","MathematicalContribution"],["there is a technical contribution","there is a technical computational or numerical contribution","there is a technical mathematical contribution","there is no technical contribution"])
    sub_adf.addNodes("BonusEffect",["FeatureTechnicalContribution and UnexpectedEffect and OneWayStreet"],["there is a bonus effect","there is no bonus effect"])
    sub_adf.addNodes("SufficiencyOfDisclosureIssue",["reject Reproducible","ClaimContainsEffect"],["there is no issue with sufficiency of disclosure regarding this feature","there is an issue of sufficiency of disclosure as the claim states an effect which is not reproducible","there is no issue with sufficiency of disclosure regarding this feature"])
    sub_adf.addNodes("ImpreciseUnexpectedEffect",["reject PreciseTerms","UnexpectedEffect"],["the unexpected effect is clearly and precisely described","the unexpected effect is not clearly and precisely described","there is no unexpected effect"])
    sub_adf.addNodes("FeatureReliableTechnicalEffect",["reject SufficiencyOfDisclosureIssue","reject BonusEffect","reject ImpreciseUnexpectedEffect", "FeatureTechnicalContribution and Credible and Reproducible"],["An issue with sufficiency of disclosure precludes us relying on this feature","The feature is a bonus effect which precludes us relying on this feature","The feature is a unexpected effect which is not clearly described precluding us relying on this feature","The feature is a credible, reproducible and reliable technical contribution","The feature is not a reliable technical contribution due to a lack of credibility or reproducibility"])
    
    #The fact the sub-adm is running means there are distinguishing features so to more easily resolve this we just auto add it to eval later
    sub_adf.case = ["DistinguishingFeatures"]
    
    sub_adf.questionOrder = ["IndependentContribution","CombinationContribution","nature_feat","CircumventTechProblem","TechnicalAdaptation","IntendedTechnicalUse","TechUseSpecified","SpecificPurpose","FunctionallyLimited","UnexpectedEffect","PreciseTerms","OneWayStreet","cred_repro_questions","ClaimContainsEffect"]
    return sub_adf

    # Add Sub-ADM 2 algorithm

#Sub-ADM 1 algorithm
def collect_features(ui_instance, key_facts=None):
        """Function to collect prior art items from user input"""
        # Use key facts to populate placeholders in questions
        cpa_info = ""
        invention_info = ""
        
        if key_facts:
            # Get CPA information from key facts
            if 'CPA' in key_facts:
                cpa_info = f"\n\nClosest Prior Art: {key_facts['CPA']}"
            elif 'INFORMATION' in key_facts and 'CPA' in key_facts['INFORMATION']:
                cpa_info = f"\n\nClosest Prior Art: {key_facts['INFORMATION']['CPA']}"
            
            # Get invention information from key facts
            if 'INVENTION_TITLE' in key_facts:
                invention_info = f"\n\nInvention: {key_facts['INVENTION_TITLE']}"
            elif 'INFORMATION' in key_facts and 'INVENTION_TITLE' in key_facts['INFORMATION']:
                invention_info = f"\n\nInvention: {key_facts['INFORMATION']['INVENTION_TITLE']}"
        
        available_items = input(f"What features does the closest prior art have?{cpa_info}\n\n(comma-separated list): ").strip()
        needed_items = input(f"What features does the invention have?{invention_info}\n\n(comma-separated list): ").strip()
        available_list = [item.strip() for item in available_items.split(',') if item.strip()]
        needed_list = [item.strip() for item in needed_items.split(',') if item.strip()]
        
        missing_items = [item for item in needed_list if item not in available_list]
        return missing_items

#Sub-ADM 2
def create_sub_adm_2(item_name, key_facts=None):
    """Create sub-ADM for evaluating objective technical problems"""
    sub_adf = SubADM("Sub-Model 2", item_name)

      # Store key facts in the sub-ADM if provided
    if key_facts:
        sub_adf.facts = key_facts.copy()
        print(f"Sub-ADM for {item_name} initialized with {len(key_facts)} key facts")
    
    #AF32
    sub_adf.addNodes("BasicFormulation", ['Encompassed and Embodied and ScopeOfClaim'], 
                    ['We have a valid basic formulation of the objective technical problem', 'We do not have a valid basic formulation of the objective technical problem'])
    
    #AF31
    sub_adf.addNodes("WellFormed", ['reject Hindsight','WrittenFormulation and BasicFormulation'], 
                    ['There is a written objective technical problem which has been formed without hindsight', 'There is no written objective technical problem which has been formed without hindsight'])

    #AF30
    sub_adf.addNodes("ConstrainedProblem", ['WellFormed and NonTechnicalContribution',], 
                    ['There are non-technical contributions constraining the objective technical problem', 'There are no non-technical contributions constraining the objective technical problem'])    

    #AF29            
    sub_adf.addNodes("ObjectiveTechnicalProblemFormulation", ['ConstrainedProblem','WellFormed'], 
                    ['There is a valid objective technical problem formulation constrained by non-technical contributions', 'There is a valid objective technical problem formulation', 'There is no valid objective technical problem formulation'])     
    
    #ROOT ISSUE 
    sub_adf.addNodes("WouldHaveArrived", ['WouldModify and  ObjectiveTechnicalProblemFormulation', 'WouldAdapt and ObjectiveTechnicalProblemFormulation'],
                    ['The skilled person would have arrived at the proposed invention by modifying the closest prior art', 'The skilled person would have arrived at the proposed invention by adapting the closest prior art'])

    #BLFs
    #F48
    sub_adf.addNodes("Encompassed",question='Would the skilled person, consider the the technical effects identified to be encompassed by the technical teaching?')

    #F49
    sub_adf.addNodes("Embodied",question='Would the skilled person, consider the the technical effects identified to be embodied by the same originally disclosed invention?')

    #F50
    sub_adf.addNodes("ScopeOfClaim",question='Are the technical effects achieved across the whole scope of the claim, and is this claim limited in such a way that substantially all embodiments encompassed by the claim show these effects?')

    #F51
    sub_adf.addDependentBLF("WrittenFormulation","BasicFormulation", 
                            'Can we construct a written formulation of the objective technical problem?',
                            None)

    #F52
    sub_adf.addDependentBLF("Hindsight","BasicFormulation", 
                            'Has the objective technical problem been formulated in such a way as to refer to matters of which the skilled person would only have become aware by knowledge of the solution claimed?',
                            None)

    #F53/F54
    sub_adf.addQuestionInstantiator(
    "Would the skilled person have arrived at the proposed invention by adapting or modifying the closest prior art, not simply because they could, but because they the prior art would have provided motivation to do so in the expectation of some improvement or advantage?",
    {
        "Would have adapted from the prior art": "WouldAdapt",
        "Would have modified from the prior art": "WouldModify",
        "Neither":""
    },
    None,
    "modify_adapt",
    dependency_node="ObjectiveTechnicalProblemFormulation")

    #The fact the sub-adm is running means there are distinguishing features so to more easily resolve this we just auto add it to eval later
    # Check if NonTechnicalContribution is in the main ad case, if so add it to sub_adf case
    if key_facts and 'main_case' in key_facts:
        main_case = key_facts['main_case']
        if 'NonTechnicalContribution' in main_case:
            sub_adf.case = ['NonTechnicalContribution']
        else:
            sub_adf.case = []
    else:
        sub_adf.case = []
    
    sub_adf.questionOrder = ["Encompassed","Embodied","ScopeOfClaim","WrittenFormulation","Hindsight","modify_adapt"]
    return sub_adf

# Add Sub-ADM 2 algorithm
def collect_obj(ui_instance, key_facts=None):
    """Function to collect objective technical problems from user input based on sub-ADM results"""
    # Get the ADF instance
    adf = ui_instance.adf
    print('DEBUG: HERE')
    # Get sub-ADM results from ReliableTechnicalEffect
    sub_adm_results = adf.getFact("ReliableTechnicalEffect", "results")
    if not sub_adm_results:
        print("No sub-ADM results found. Cannot determine technical contributions.")
        return []
    
    # Get the current main ADM case to check for Combination/PartialProblems
    current_case = adf.case if hasattr(adf, 'case') else []
    
    # Get the distinguished features list using _get_source_items
    distinguished_features_list = []
    try:
        distinguished_features_list = adf.getFact("ReliableTechnicalEffect", "items") or []

    except Exception as e:
        print(f"Warning: Could not retrieve distinguished features list: {e}")
        distinguished_features_list = []
    
    # Extract technical and non-technical contributions from sub-ADM results
    technical_contributions = []
    non_technical_contributions = []
    
    for i, case in enumerate(sub_adm_results):
        if isinstance(case, list):
            # Check if FeatureTechnicalContribution is in this case (technical contribution)
            if "FeatureTechnicalContribution" in case:
                # Get the corresponding distinguished feature from the list
                if i < len(distinguished_features_list):
                    feature_name = distinguished_features_list[i]
                    technical_contributions.append(f"Case {i+1}: {feature_name}")
                else:
                    technical_contributions.append(f"Case {i+1}: DistinguishingFeatures")
            
            # Check if FeatureTechnicalContribution is not in this case (non-technical contribution)
            if "FeatureTechnicalContribution" not in case:
                # Get the corresponding distinguished feature from the list
                if i < len(distinguished_features_list):
                    feature_name = distinguished_features_list[i]
                    non_technical_contributions.append(f"Case {i+1}: {feature_name}")
                else:
                    non_technical_contributions.append(f"Case {i+1}: NormalTechnicalContribution")
    
    # Present the features to the user
    print("\n" + "="*60)
    print("OBJECTIVE TECHNICAL PROBLEM COLLECTION")
    print("="*60)
    
    if technical_contributions:
        print(f"\nTechnical Contributions:")
        for contrib in technical_contributions:
            print(f"  • {contrib}")
    else:
        print(f"\nTechnical Contributions: None found")
        
    if non_technical_contributions:
        print(f"\nNon-Technical Contributions:")
        for contrib in non_technical_contributions:
            print(f"  • {contrib}")
    else:
        print(f"\nNon-Technical Contributions: None found")
    
    print("\n" + "="*60)
    
    # Check conditions and collect problems
    objective_problems = []
    
    if "Combination" in current_case:
        print("\nCombination detected in case - creating 1 objective technical problem:")
        problem_desc = input("Please provide a short description of the objective technical problem: ").strip()
        if problem_desc:
            objective_problems.append(problem_desc)
            print(f"✓ Added problem: {problem_desc}")
    
    if "PartialProblems" in current_case:
        print("\nPartialProblems detected in case - creating multiple problems:")
        print("Enter problems one by one. Type 'done' when finished.")
        
        problem_count = 0
        while True:
            problem_desc = input(f"Problem {problem_count + 1} description (or 'done' to finish): ").strip()
            if problem_desc.lower() == 'done':
                break
            if problem_desc:
                objective_problems.append(problem_desc)
                problem_count += 1
                print(f"✓ Added problem {problem_count}: {problem_desc}")
    
    # Store the problems as facts in the ADF
    if objective_problems:
        adf.setFact("ObjectiveTechnicalProblem", "objective_technical_problems", objective_problems)
        print(f"\n✓ Stored {len(objective_problems)} objective technical problem(s)")
    else:
        print("\nNo objective technical problems created")
    
    return objective_problems

#ADM definition
def adf():
    """
    Creates and returns an ADF for the Inventive Step domain
    """
    adf = ADF("Inventive Step")

    # Add information questions before the logic questions
    adf.addInformationQuestion("INVENTION_TITLE", "\n\nWhat is the title of your invention?")
    adf.addInformationQuestion("INVENTION_DESCRIPTION", "\n\nPlease provide a brief description of your invention")
    adf.addInformationQuestion("INVENTION_TECHNICAL_FIELD", "\n\nWhat is the technical field of the invention?")
    adf.addInformationQuestion("REL_PRIOR_ART", "\n\nPlease briefly describe the relevant prior art")
    
    #F13
    adf.addQuestionInstantiator(
    "\n\nDo the candidate relevant prior art documents have a similar purpose to the invention?",
    {
        "They have the same or a very similar purpose.": "SimilarPurpose",
        "They have a different purpose.": ""
    },None,
    "field_questions")

    #F14
    adf.addQuestionInstantiator(
    "\n\nAre there similar technical effects between the candidate relevant prior art documents and the invention?",
    {
        "It produces a similar technical effect.": "SimilarEffect",
        "It produces a different technical effect.": ""
    },None,
    "field_questions_2")

    #F15/F16
    adf.addQuestionInstantiator(
    "\n\nWhat is the relationship between the candidate relevant prior art documents and the invention\'s technical field? \n\nInvention Technical Field: {INVENTION_TECHNICAL_FIELD} \n\n",
    {
        "It is from the exact same technical field.": "SameField",
        "It is from a closely related or analogous technical field.": "SimilarField",
        "It is from an unrelated technical field.": ""
    },
    None,
    "field_questions_3")

    adf.addInformationQuestion("CGK", "\n\nBriefly describe the common general knowledge")

    #F8
    adf.addNodes("Contested", question="\n\nIs the assertion of what constitutes Common General Knowledge being contested? \n\n Common General Knowledge: {CGK} \n\n")
    
    #F9/F10/F11
    adf.addQuestionInstantiator(
        "\n\nWhat is the primary source of evidence cited for the CGK? \n\n Common General Knowledge: {CGK} \n\n",
        {
            "A standard textbook": "Textbook",
            "A broad technical survey": "TechnicalSurvey",
            "A single publication in a very new or rapidly evolving field.":"PublicationNewField",
            "A single publication in an established field.": "SinglePublication",
            "No documentary evidence is provided.": '' ,
            "Other":''
        },None,
        question_order_name="field_questions_4",
        #TEST
        dependency_node= 'Contested'
    )

    #F1
    adf.addDependentBLF("SkilledIn", 
                        "RelevantPriorArt",  
                        "\n\nIs the practitioner skilled in the relevant technical field of the prior art?\n\nRelevant Prior Art: {REL_PRIOR_ART}\n\n",
                        None)

    #F2    
    adf.addNodes("Average", question="\nDoes the practitioner possess average knowledge and ability for that field?\n\n")

    #F3
    adf.addDependentBLF("Aware", 
                        "CommonKnowledge",  
                        "\n\nIs the practitioner presumed to be aware of the common general knowledge in the field?\n\nCommon General Knowledge: {CGK}\n\n",
                        None)
    #F4
    adf.addDependentBLF("Access", 
                        "CommonKnowledge", 
                        "\n\nDoes the practitioner have access to all documents comprising the state of the art?\n\nCommon General Knowledge: {CGK}\n\n",
                        None)

    #F5/F6/F7
    adf.addQuestionInstantiator(
    "\n\nWhat is the nature of this practitioner?",
    {
        "An individual practitioner": "Individual",
        "A research team": "ResearchTeam",
        "A production or manufacturing team": "ProductionTeam",
        "Other": ''
    }, {
        "Individual": {"SkilledPerson": "Please describe the individual practitioner"},
        "ResearchTeam": {"SkilledPerson": "Please describe the research team"},
        "ProductionTeam": {"SkilledPerson": "Please describe the production or manufacturing team"}
    },
    question_order_name="skilled_person",
    )

    #F19
    adf.addQuestionInstantiator(
    "\n\nIs the closest prior art document itself a single reference?",
    {
        "Yes": "SingleReference",
        "No": ''
    }, 
    {
        "SingleReference": {"CPA": "Please describe the candidate for the closest prior art"},
    },
    question_order_name="SingleReference"
    )
    #
    #F20/F21
    adf.addQuestionInstantiator(
    "\n\nDoes the closest prior art document require minimal modifications to the invention as assessed from the perspective of the skilled person? \n\n The skilled person: {SkilledPerson}",
    {
        "Yes": ["MinModifications","AssessedBy"],
        "No": ''
    }, None,
    question_order_name="cpa_min_mod",
    dependency_node='SkilledPerson'
    )
    #F22
    adf.addDependentBLF("CombinationAttempt", 
                        "ClosestPriorArt", 
                        "\n\nIs there a reason to combine other documents with the CPA to attempt to demonstrate obviousness?\n\nClosest Prior: {CPA}\n\n",
                        None)
    #F17/F18
    adf.addQuestionInstantiator(
    "\n\nHow are the other documents to be combined related to the CPA's technical field \n\n Closest Prior Art: {CPA}\n\n",
    {
        "They are from the same technical field": "SameFieldCPA",
        "They are from a similar technical field": "SimilarFieldCPA",
        "They are from an unrelated field": ""
    }, None,
    question_order_name="combined_docs",
    dependency_node=['ClosestPriorArt','CombinationAttempt']
    )
    #F23
    adf.addDependentBLF("CombinationMotive", 
                        ["ClosestPriorArt",'SkilledPerson','CombinationAttempt'], 
                        "\n\nWould the skilled person have a clear and direct motive to combine these specific documents?\n\n The skilled person: {SkilledPerson}\n\nClosest Prior: {CPA}\n\n",
                        None)

    adf.addDependentBLF("BasisToAssociate", 
                        ["ClosestPriorArt",'SkilledPerson','CombinationAttempt'],
                        "\n\nIs there a reasonable basis for the skilled person to associate these specific documents with one another?\n\n The skilled person: {SkilledPerson}\n\nClosest Prior: {CPA}\n\n",
                        None)

    #Abstract factors
    #AF5
    adf.addNodes("RelevantPriorArt", ['SameField','SimilarField','SimilarPurpose','SimilarEffect'], ['the relevant prior art is from the same field','the relevant prior art is from a similar field','the relevant prior art has a similar purpose','the relevant prior art has a similar effect','a relevant prior art cannot be established'])
    #AF4
    adf.addNodes("DocumentaryEvidence", ['reject SinglePublication','Textbook','TechnicalSurvey','PublicationNewField'], ['a single publication is not documentary evidence','a textbook is the documentary evidence','a technical survey is the documentary evidence','a publication in a new or emerging field is the documentary evidence', 'no documentary evidence for common knowledge provided'])
    #AF3
    adf.addNodes("CommonKnowledge", ['DocumentaryEvidence','reject Contested','accept'], ['common knowledge evidenced', 'no common knowledge established', 'common knowledge not disputed'])
    #AF1
    adf.addNodes("Person", ['Individual','ResearchTeam','ProductionTeam'], ['the skilled practitioner is an individual','the skilled practitioner is a research team','the skilled practitioner is a production team','the skilled practitioner does not fall within a vaild category'])
    #AF2
    adf.addNodes("SkilledPerson", ['SkilledIn and Average and Aware and Access and Person'], ['there is a defined skilled person','there is not a skilled person'])
    #AF6
    adf.addNodes("ClosestPriorArt", ['RelevantPriorArt and SingleReference and MinModifications and AssessedBy'], ['the closest prior art has been established','the closest prior art cannot be identified'])
    #AF7
    adf.addNodes("CombinationDocuments", ['CombinationAttempt and SameFieldCPA and CombinationMotive and BasisToAssociate','CombinationAttempt and SimilarFieldCPA and CombinationMotive and BasisToAssociate'], ['the combination of documents relevant to the closest prior art come from the same field','the combination of documents relevant to the closest prior art come from a similar field','no combination of documents relevant to the closest prior art'])
    #AF8
    adf.addNodes("ClosestPriorArtDocuments", ['CombinationDocuments','ClosestPriorArt',''], ['the closest prior art consists of a combination of documents','the closest prior art consists of a document of a single reference','no set of closest prior documents could be determined'])
    
    #AF9
    adf.addNodes("Combination",['ReliableTechnicalEffect and FunctionalInteraction and Synergy'],['There is a synergy between all the technical effects', 'There is no synergy between all the technical effects'])

    #AF10    
    adf.addNodes("PartialProblems",['reject Combination','ReliableTechnicalEffect'],['There are not an aggregate of technical effects', 'There are an aggregate of technical effects', ""])

    #AF11
    adf.addNodes("CandidateOTP",['Combination','PartialProblems'],['There is a single objective technical problem','There are multiple partial problems which form the objective technical problem'])    
    
    #F28
    adf.addSubADMBLF("ReliableTechnicalEffect", create_sub_adm_1, collect_features, dependency_node=['SkilledPerson','ClosestPriorArt'])

    #F25
    adf.addEvaluationBLF("DistinguishingFeatures", "ReliableTechnicalEffect", "DistinguishingFeatures", ['there are distinguishing features','there are no distinguishing features'])

    #F26
    adf.addEvaluationBLF("NonTechnicalContribution", "ReliableTechnicalEffect", "FeatureTechnicalContribution", ['there is a non-technical contribution','there is no non-technical contribution'], rejection_condition=True)

    #F27
    adf.addEvaluationBLF("TechnicalContribution", "ReliableTechnicalEffect", "FeatureTechnicalContribution", ['the features contain a technical contribution','The features do not contain a technical contribution'])

    #F29
    adf.addEvaluationBLF("SufficiencyOfDisclosure", "ReliableTechnicalEffect", "SufficiencyOfDisclosureIssue", ['there is an issue with sufficiency of disclosure','there is no issue with sufficiency of disclosure'])

    #F62
    adf.addEvaluationBLF("InventionUnexpectedEffect", "ReliableTechnicalEffect", "UnexpectedEffect", ['there is an unexpected effect within the invention','there is not an unexpected effect within the invention'])
    #Next BLFs
    #F46
    adf.addQuestionInstantiator(
    "How do the invention's features create the technical effect?",
    {
        "As a synergistic combination (effect is greater than the sum of parts).": "Synergy",
        "As a simple aggregation of independent effects.": "",
        "Neither":""
    },
    None,
    "synergy_question",
    dependency_node= "ReliableTechnicalEffect")    

    #F45
    adf.addDependentBLF("FunctionalInteraction",["ReliableTechnicalEffect","Synergy"],
                        "Is the synergistic combination achieved through a functional interaction between features?",
                        None)

    
    #F47 - DO OTHER DEPENDENCY NODES
    adf.addSubADMBLF("OTPObvious", create_sub_adm_2, collect_obj, dependency_node=["CandidateOTP",'SkilledPerson','RelevantPriorArt','ClosestPriorArt'], rejection_condition=True)

    adf.addEvaluationBLF("ObjectiveTechnicalProblem", "OTPObvious", "ObjectiveTechnicalProblemFormulation", ['there is a valid objective technical problem','there is not a valid objective technical problem'])

    # Set question order to ask information questions first
    adf.questionOrder = ["INVENTION_TITLE", "INVENTION_DESCRIPTION", "INVENTION_TECHNICAL_FIELD", "REL_PRIOR_ART", "field_questions",
    "field_questions_2","field_questions_3",'CGK',"Contested",'field_questions_4','SkilledIn','Average','Aware','Access','skilled_person',
    'SingleReference','cpa_min_mod',"CombinationAttempt",'combined_docs','CombinationMotive','BasisToAssociate','ReliableTechnicalEffect','DistinguishingFeatures','NonTechnicalContribution','TechnicalContribution','SufficiencyOfDisclosure',"InventionUnexpectedEffect",
    "synergy_question","FunctionalInteraction","OTPObvious","ObjectiveTechnicalProblem"
    
    ]





  
    # 
    
    # # Add EvaluationBLF for valid prior art
    # adf.addEvaluationBLF("VALID_PRIOR_ART_PRESENT", 
    #                      "PRIOR_ART_ITEMS", 
    #                      "VALID_PRIOR_ART", 
    #                      ["VALID_PRIOR_ART_PRESENT is accepted - valid prior art found", 
    #                       "VALID_PRIOR_ART_PRESENT is rejected - no valid prior art found"])
    
    # # Add DependentBLF for obviousness assessment
    # adf.addDependentBLF("OBVIOUSNESS_ASSESSMENT", 
    #                     "PRIOR_ART_EVALUATION", 
    #                     "Is the invention obvious to a person skilled in the art given {obviousness_method}?",
    #                     ["OBVIOUSNESS_ASSESSMENT is accepted - invention is obvious", 
    #                      "OBVIOUSNESS_ASSESSMENT is rejected - invention is not obvious"])
    
    # # Add DependentBLF for non-obviousness assessment
    # adf.addDependentBLF("NON_OBVIOUSNESS_ASSESSMENT", 
    #                     "PRIOR_ART_EVALUATION", 
    #                     "Is the invention non-obvious to a person skilled in the art given {non_obviousness_method}?",
    #                     ["NON_OBVIOUSNESS_ASSESSMENT is accepted - invention is non-obvious", 
    #                      "NON_OBVIOUSNESS_ASSESSMENT is rejected - invention is obvious"])
    
    # # Add final inventive step conclusion
    # adf.addNodes("INVENTIVE_STEP_CONCLUSION", 
    #              ["OBVIOUSNESS_ASSESSMENT or NON_OBVIOUSNESS_ASSESSMENT"], 
    #              ["INVENTIVE_STEP_CONCLUSION is accepted - inventive step assessment completed", 
    #               "INVENTIVE_STEP_CONCLUSION is rejected - assessment incomplete"])
    
    # Set question order

    
    return adf


def cases():
    """
    Returns predefined cases for testing
    """
    return {
        "test_case": ["PRIOR_ART_ANALYSIS", "SKILLED_PERSON_ANALYSIS", "OBVIOUSNESS"]
    }
