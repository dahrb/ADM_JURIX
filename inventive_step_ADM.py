"""
Inventive Step ADM 
"""

from MainClasses import *


def adf():
    """
    Creates and returns an ADF for the Inventive Step domain
    """
    adf = ADF("Inventive Step")

    # Create trad blf
    #adf.addNodes("NOVELTY", None, None, "Is your research novel?")

    # Create abstract factor
    #adf.addNodes("MIXED_METHODS", ["QUANTITATIVE and QUALITATIVE"], ["MIXED_METHODS is accepted", "MIXED_METHODS is rejected"])
    
    # Associate a factual ascription with the answer to a question
    # adf.addQuestionInstantiator(
    #     "What type of research are you conducting?",
    #     {
    #         "quantitative": "QUANTITATIVE",
    #         "qualitative": "QUALITATIVE",
    #         "both": ["QUANTITATIVE", "QUALITATIVE"]
    #     },
    #     {
    #         "QUANTITATIVE": {"QUANTITATIVE_method": "What specific quantitative method will you use?"},
    #         "QUALITATIVE": {"QUALITATIVE_method": "What specific qualitative method will you use?"}
    #     },
    #     "question_1"
    # )
   
    # Create a dependent blf that depends on another factor
    # adf.addDependentBLF("DATA_ANALYSIS", 
    #                     "MIXED_METHODS",  # Dependency on MIXED_METHODS
    #                     "Are {QUANTITATIVE_method}, {QUALITATIVE_method} appropriate for your data type?",
    #                     ["DATA_ANALYSIS is accepted - methods are appropriate", "DATA_ANALYSIS is rejected - methods are not appropriate"])
    
    # Add a sub-ADM blf
    # PATTERN FOR OTHER DOMAINS:
    # 1. Create a function that returns the list of items to evaluate
    # 2. Create a sub-ADM creator function
    # 3. Use adf.addSubADMBLF(name, sub_adf_creator, items_function, statements, questions)
    #
    # def collect_sources(ui_instance):
    #     """Function to collect sources from user input"""
    #     # Ask the user for sources
    #     available_sources = input("What sources do you have access to? (comma-separated list): ").strip()
    #     needed_sources = input("What sources do you need for your research? (comma-separated list): ").strip()
        
    #     # Calculate missing sources
    #     available_list = [item.strip() for item in available_sources.split(',') if item.strip()]
    #     needed_list = [item.strip() for item in needed_sources.split(',') if item.strip()]
        
    #     missing_sources = [item for item in needed_list if item not in available_list]
        
    #     return missing_sources
    
    # adf.addSubADMBLF("PRIMARY_SOURCES", create_source_sub_adm, collect_sources, [
    #     "PRIMARY_SOURCES is accepted - you have primary sources for your research",
    #     "PRIMARY_SOURCES is rejected - no primary sources available"
    # ], {
    #     'positive': 'Is {item} primary data (collected directly)?',
    #     'negative': 'Is {item} secondary data (from existing sources)?'
    # })
    
    # # Add SECONDARY_SOURCES as an EvaluationBLF that evaluates sub-ADM results
    # adf.addEvaluationBLF("SECONDARY_SOURCES_EVALUATION", 
    #                      "PRIMARY_SOURCES",  # Source BLF to check
    #                      "NEGATIVE_RESOURCE",  # Condition to look for
    #                      ["SECONDARY_SOURCES is accepted - you have secondary sources", 
    #                       "SECONDARY_SOURCES is rejected - no secondary sources"])  

    # Set the question order to include all questions (SOURCES removed)
    adf.questionOrder = []
    
    return adf