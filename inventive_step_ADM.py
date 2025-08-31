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

    #F13
    adf.addQuestionInstantiator(
    "Do the candidate relevant prior art documents have a similar purpose to the invention?",
    {
        "They have the same or a very similar purpose.": "SimilarPurpose",
        "They have a different purpose.": ""
    },None,
    "field_questions")

    #F14
    adf.addQuestionInstantiator(
    "Are there similar technical effects between the candidate relevant prior art documents and the invention?",
    {
        "It produces a similar technical effect.": "SimilarEffect",
        "It produces a different technical effect.": ""
    },None,
    "field_questions_2")

    #F15/F16
    adf.addQuestionInstantiator(
    "What is the relationship between the candidate relevant prior art documents and the invention/'s technical field? \n\n Invention Technical Field: {INVENTION_TECHNICAL_FIELD} \n\n",
    {
        "It is from the exact same technical field.": "SameField",
        "It is from a closely related or analogous technical field.": "SimilarField",
        "It is from an unrelated technical field.": ""
    },
    None,
    "field_questions_3")

    adf.addInformationQuestion("CGK", "\n\nBriefly describe the common general knowledge")

    #F8
    adf.addNodes("Contested", question="Is the assertion of what constitutes Common General Knowledge being contested?  \n\n Common General Knowledge: {CGK} \n\n")
    
    #F9
    adf.addQuestionInstantiator(
        "",
        {
            "same field": "SinglePublication",
            "similar field": "Textbook",
            "tech surv":"TechnicalSurvey",
            "pub new": "PublicationNewField",
            "both": ["", ""]
        },
        {
            "": {"obviousness_method": "What specific obviousness test will you use?"},
            "": {"non_obviousness_method": "What specific non-obviousness test will you use?"}
        },
        "field_questions"
    )
    

    # Set question order to ask information questions first
    adf.questionOrder = ["INVENTION_TITLE", "INVENTION_DESCRIPTION", "REL_PRIOR_ART", "field_questions",
    "field_questions_2","field_questions_3"]






    # # Add question instantiator for inventive step assessment
    # adf.addQuestionInstantiator(
    #     "What type of inventive step assessment are you conducting?",
    #     {
    #         "obviousness": "OBVIOUSNESS",
    #         "non-obviousness": "NON_OBVIOUSNESS",
    #         "both": ["OBVIOUSNESS", "NON_OBVIOUSNESS"]
    #     },
    #     {
    #         "OBVIOUSNESS": {"obviousness_method": "What specific obviousness test will you use?"},
    #         "NON_OBVIOUSNESS": {"non_obviousness_method": "What specific non-obviousness test will you use?"}
    #     },
    #     "inventive_step_type"
    # )

    # # Add basic BLFs
    # adf.addNodes("PRIOR_ART_ANALYSIS", question="Have you conducted a comprehensive prior art analysis?")
    # adf.addNodes("SKILLED_PERSON_ANALYSIS", question="Have you identified the person skilled in the art?")
    # adf.addNodes("PROBLEM_SOLUTION_APPROACH", question="Are you using the problem-solution approach?")
    
    # # Add abstract factors
    # adf.addNodes("PRIOR_ART_EVALUATION", 
    #              ["PRIOR_ART_ANALYSIS and SKILLED_PERSON_ANALYSIS"], 
    #              ["PRIOR_ART_EVALUATION is accepted - comprehensive analysis completed", 
    #               "PRIOR_ART_EVALUATION is rejected - analysis incomplete"])
    
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
