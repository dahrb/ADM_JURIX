"""
Inventive Step ADM 
"""

from MainClasses import *


def create_sub_adm_prior_art(item_name):
    """Creates a sub-ADM for evaluating individual prior art items"""
    sub_adf = SubADM("Prior Art Sub-ADM", item_name)
    
    # Add BLFs for the sub-ADM - {item} will be automatically resolved
    sub_adf.addNodes("KNOWN_PRIOR_ART", question="Is {item} known prior art?")
    sub_adf.addNodes("PUBLICLY_AVAILABLE", question="Is {item} publicly available?")
    sub_adf.addNodes("ENABLING_DISCLOSURE", question="Does {item} provide an enabling disclosure?")
    
    # Add abstract factors
    sub_adf.addNodes("VALID_PRIOR_ART", 
                     ["KNOWN_PRIOR_ART and PUBLICLY_AVAILABLE and ENABLING_DISCLOSURE"], 
                     ["VALID_PRIOR_ART is accepted - {item} is valid prior art", 
                      "VALID_PRIOR_ART is rejected - {item} is not valid prior art"])
    
    sub_adf.questionOrder = ["KNOWN_PRIOR_ART", "PUBLICLY_AVAILABLE", "ENABLING_DISCLOSURE"]
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
    "\n\n Does the closest prior art document require minimal modifications to the invention as assessed from the perspective of the skilled person? \n\n The skilled person: {SkilledPerson}",
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




    # Set question order to ask information questions first
    adf.questionOrder = ["INVENTION_TITLE", "INVENTION_DESCRIPTION", "INVENTION_TECHNICAL_FIELD", "REL_PRIOR_ART", "field_questions",
    "field_questions_2","field_questions_3",'CGK',"Contested",'field_questions_4','SkilledIn','Average','Aware','Access','skilled_person',
    'SingleReference','cpa_min_mod']





    # # Add SubADMBLF for prior art items
    # def collect_prior_art_items(ui_instance):
    #     """Function to collect prior art items from user input"""
    #     available_items = input("What prior art items do you have? (comma-separated list): ").strip()
    #     needed_items = input("What prior art items do you need to evaluate? (comma-separated list): ").strip()
        
    #     available_list = [item.strip() for item in available_items.split(',') if item.strip()]
    #     needed_list = [item.strip() for item in needed_items.split(',') if item.strip()]
        
    #     missing_items = [item for item in needed_list if item not in available_list]
    #     return missing_items
    
    # adf.addSubADMBLF("PRIOR_ART_ITEMS", create_sub_adm_prior_art, collect_prior_art_items)
    
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
