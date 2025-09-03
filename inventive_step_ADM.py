"""
Inventive Step ADM 
"""

from MainClasses import *


def create_sub_adm_prior_art(item_name, key_facts=None):
    """Creates a sub-ADM for evaluating individual prior art items"""
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

    #F41 - Q22 -hmmm
    sub_adf.addNodes("TechnicalAdaptation",question='Is the feature a specific technical adaptation which is specific for that implementation in that its design is motivated by technical considerations relating to the internal functioning of the computer system or network.')

    #bridge node to make things easier
    sub_adf.addNodes("NumOrComp",["NumericalData or ComputerSimulation"],["NumericalData or ComputerSimulation","reject"])

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

    sub_adf.addNodes("NonReproducible",["not Reproducible"],["the technical effect is not reproducible","the technical effect is reproducible"])
    #F44 - Q32
    sub_adf.addDependentBLF("ClaimContainsEffect","NonReproducible",
                            'Does the claim contain the non-reproducible effect i.e. if the claim says the invention achieve effect E, but this is not reproducible.',
                            None)

    #abstract factors
    sub_adf.addNodes("AppliedInField",["SpecificPurpose and FunctionallyLimited"],["the technical contribution is applied in the field","the technical contribution is not applied in the field"])
    sub_adf.addNodes("MathematicalContribution",["MathematicalMethod and AppliedInField","MathematicalMethod and TechnicalAdaptation"],["the technical contribution is a mathematical contribution","","the technical contribution is not a mathematical contribution"])
    sub_adf.addNodes("ComputationalContribution",["ComputerSimulation and TechnicalAdaptation","ComputerSimulation and IntendedTechnicalUse","NumericalData and IntendedTechnicalUse","ComputerSimulation and TechUseSpecified"],["ComputerSimulation and TechnicalAdaptation","ComputerSimulation and IntendedTechnicalUse","NumericalData and IntendedTechnicalUse","ComputerSimulation and TechUseSpecified","reject"])
    sub_adf.addNodes("ExcludedField",["ComputerSimulation","NumericalData","MathematicalMethod","OtherExclusions"],["ComputerSimulation","NumericalData","MathematicalMethod","OtherExclusions","reject"])
    sub_adf.addNodes("NormalTechnicalContribution",["reject CircumventTechProblem","reject ExcludedField","IndependentContribution","CombinationContribution"],["reject CircumventTechProblem","reject ExcludedField","IndependentContribution","CombinationContribution","reject"])
    sub_adf.addNodes("FeatureTechnicalContribution",["NormalTechnicalContribution","ComputationalContribution","MathematicalContribution"],["there is a technical contribution","there is a technical computational contribution","there is a technical mathematical contribution","there is no technical contribution"])
    sub_adf.addNodes("BonusEffect",["FeatureTechnicalContribution and UnexpectedEffect and OneWayStreet"],["there is a bonus effect","there is no bonus effect"])
    sub_adf.addNodes("SufficiencyOfDisclosureIssue",["reject Reproducible","ClaimContainsEffect"],["reject cus Reproducible","reject ClaimContainsEffect","reject"])
    sub_adf.addNodes("ImpreciseUnexpectedEffect",["reject PreciseTerms","UnexpectedEffect"],["reject PreciseTerms","UnexpectedEffect","reject"])
    sub_adf.addNodes("ReliableTechnicalEffect",["reject SufficiencyOfDisclosureIssue","reject BonusEffect","reject ImpreciseUnexpectedEffect", "FeatureTechnicalContribution and Credible and Reproducible"],["reject SufficiencyOfDisclosureIssue","reject BonusEffect","reject ImpreciseUnexpectedEffect","FeatureTechnicalContribution and Credible and Reproducible","reject reliable"])
    
    #The fact the sub-adm is running means there are distinguishing features so to more easily resolve this we just auto add it to eval later
    sub_adf.case = ["DistinguishingFeatures"]
    
    sub_adf.questionOrder = [ "IndependentContribution","CombinationContribution","nature_feat","CircumventTechProblem","TechnicalAdaptation","IntendedTechnicalUse","TechUseSpecified","SpecificPurpose","FunctionallyLimited","UnexpectedEffect","PreciseTerms","OneWayStreet","cred_repro_questions","ClaimContainsEffect"]
    return sub_adf


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
    adf.addNodes("CombinationDocuments", ['CombinationAttempt and SameFieldCPA and CominationMotive and BasisToAssociate','CombinationAttempt and SimilarFieldCPA and CombinationMotive and BasisToAssociate'], ['the combination of documents relevant to the closest prior art come from the same field','the combination of documents relevant to the closest prior art come from a similar field','no combination of documents relevant to the closest prior art'])
    #AF8
    adf.addNodes("ClosestPriorArtDocuments", ['CombinationDocuments','ClosestPriorArt',''], ['the closest prior art consists of a combination of documents','the closest prior art consists of a document of a single reference','no set of closest prior documents could be determined'])

    # Add Sub-ADM 1 algorithm
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
    
    #F28
    adf.addSubADMBLF("FeatureReliableTechnicalEffect", create_sub_adm_prior_art, collect_features, dependency_node=['SkilledPerson','ClosestPriorArt'])

    #F25
    adf.addEvaluationBLF("DistinguishingFeatures", "FeatureReliableTechnicalEffect", "DistinguishingFeatures", ['DistinguishingFeatures is accepted - there are distinguishing features','DistinguishingFeatures is rejected - there are no distinguishing features'])


    # Set question order to ask information questions first
    adf.questionOrder = ["INVENTION_TITLE", "INVENTION_DESCRIPTION", "INVENTION_TECHNICAL_FIELD", "REL_PRIOR_ART", "field_questions",
    "field_questions_2","field_questions_3",'CGK',"Contested",'field_questions_4','SkilledIn','Average','Aware','Access','skilled_person',
    'SingleReference','cpa_min_mod',"CombinationAttempt",'combined_docs','CombinationMotive','BasisToAssociate','FeatureReliableTechnicalEffect','DistinguishingFeatures']





  
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
