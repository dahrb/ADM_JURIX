#!/usr/bin/env python3
"""
Toy ADM - Argumentation Decision Framework
"""

from MainClasses import *

# Add PRIMARY_SOURCES BLF that evaluates sub-ADMs for each source
def create_source_sub_adm():
    """Creates a sub-ADM for evaluating individual sources"""
    sub_adf = ADF("SourceEvaluation")
    
    # Add BLFs for the sub-ADM
    sub_adf.addNodes("POSITIVE_DATA", None, None, "Is {item} primary data (collected directly)?")
    sub_adf.addNodes("NEGATIVE_DATA", None, None, "Is {item} secondary data (from existing sources)?")
    
    # Add abstract factors
    sub_adf.addNodes("POSITIVE_RESOURCE", ["POSITIVE_DATA and not NEGATIVE_DATA"], ["POSITIVE_RESOURCE is accepted - primary source", "POSITIVE_RESOURCE is rejected - not primary"])
    sub_adf.addNodes("NEGATIVE_RESOURCE", ["NEGATIVE_DATA and not POSITIVE_DATA"], ["NEGATIVE_RESOURCE is accepted - secondary source", "NEGATIVE_RESOURCE is rejected - not secondary"])
    
    return sub_adf

def adf():
    """
    Creates and returns an ADF for the Academic Research Project domain
    """
    adf = ADF("Academic Research Project")
    
    # Add question instantiator for research type
    adf.addQuestionInstantiator(
        "What type of research are you conducting?",
        {
            "quantitative": "QUANTITATIVE",
            "qualitative": "QUALITATIVE",
            "both": ["QUANTITATIVE", "QUALITATIVE"]
        },
        {
            "QUANTITATIVE": {"QUANTITATIVE_method": "What specific quantitative method will you use?"},
            "QUALITATIVE": {"QUALITATIVE_method": "What specific qualitative method will you use?"}
        },
        "question_1"
    )

    # Create MIXED_METHODS as an abstract factor with proper parent-child relationships
    # We need to manually set up the children after the question instantiator creates them
    adf.addNodes("MIXED_METHODS", ["QUANTITATIVE and QUALITATIVE"], ["MIXED_METHODS is accepted", "MIXED_METHODS is rejected"])
    
    adf.addNodes("NOVELTY", None, None, "Is your research novel?")
    
    # Manually add NOVELTY to question order since it has no acceptance condition
    if "NOVELTY" not in adf.questionOrder:
        adf.questionOrder.append("NOVELTY")
    # After the question instantiator runs, we'll need to set up the parent-child relationships
    # This will be done in the UI when the question instantiator creates the nodes
   
    # Add DATA_ANALYSIS BLF that depends on MIXED_METHODS and inherits its facts
    # MIXED_METHODS will inherit properties from QUANTITATIVE and QUALITATIVE children
    adf.addDependentBLF("DATA_ANALYSIS", 
                        "MIXED_METHODS",  # Dependency on MIXED_METHODS
                        "Are {QUANTITATIVE_method}, {QUALITATIVE_method} appropriate for your data type?",
                        ["DATA_ANALYSIS is accepted - methods are appropriate", "DATA_ANALYSIS is rejected - methods are not appropriate"])
    
    # Add PRIMARY_SOURCES BLF that evaluates sub-ADMs for each source
    # Uses a function to collect sources dynamically
    # 
    # PATTERN FOR OTHER DOMAINS:
    # 1. Create a function that returns the list of items to evaluate
    # 2. Create a sub-ADM creator function
    # 3. Use adf.addSubADMBLF(name, sub_adf_creator, items_function, statements, questions)
    #
    def collect_sources(ui_instance):
        """Function to collect sources from user input"""
        # Ask the user for sources
        available_sources = input("What sources do you have access to? (comma-separated list): ").strip()
        needed_sources = input("What sources do you need for your research? (comma-separated list): ").strip()
        
        # Calculate missing sources
        available_list = [item.strip() for item in available_sources.split(',') if item.strip()]
        needed_list = [item.strip() for item in needed_sources.split(',') if item.strip()]
        
        missing_sources = [item for item in needed_list if item not in available_list]
        
        return missing_sources
    
    adf.addSubADMBLF("PRIMARY_SOURCES", create_source_sub_adm, collect_sources, [
        "PRIMARY_SOURCES is accepted - you have primary sources for your research",
        "PRIMARY_SOURCES is rejected - no primary sources available"
    ], {
        'positive': 'Is {item} primary data (collected directly)?',
        'negative': 'Is {item} secondary data (from existing sources)?',
        'positive_factor_name': 'POSITIVE_DATA',
        'negative_factor_name': 'NEGATIVE_DATA',
        'accepted_factor_name': 'POSITIVE_RESOURCE',
        'rejected_factor_name': 'NEGATIVE_RESOURCE'
    })
    
    # Add SECONDARY_SOURCES as an EvaluationBLF that evaluates sub-ADM results
    adf.addEvaluationBLF("SECONDARY_SOURCES_EVALUATION", 
                         "PRIMARY_SOURCES",  # Source BLF to check
                         "NEGATIVE_RESOURCE",  # Condition to look for
                         ["SECONDARY_SOURCES is accepted - you have secondary sources", 
                          "SECONDARY_SOURCES is rejected - no secondary sources"])
    
    # Set the question order to include all questions (SOURCES removed)
    adf.questionOrder = ["question_1", "MIXED_METHODS", "DATA_ANALYSIS", "NOVELTY", "PRIMARY_SOURCES", "SECONDARY_SOURCES_EVALUATION"]
    
    # Add root node RESEARCH_QUALITY with acceptance condition that includes all research types
    # Now includes MIXED_METHODS as a valid research approach
    adf.addNodes("RESEARCH_QUALITY", [
        "PRIMARY_SOURCES and not SECONDARY_SOURCES_EVALUATION and DATA_ANALYSIS"
    ], [
        "RESEARCH_QUALITY is accepted - your research has high quality with primary sources, no secondary sources, and appropriate methodology",
        "RESEARCH_QUALITY is rejected - your research may not meet quality standards"
    ])
    
    return adf

def cases():
    """
    Returns predefined cases for the Academic Research Project domain
    """
    return {
        "Quantitative Research": ["QUANTITATIVE", "QUANTITATIVE_method", "DATA_ANALYSIS", "PRIMARY_SOURCES"],
        "Qualitative Research": ["QUALITATIVE", "QUALITATIVE_method", "DATA_ANALYSIS", "PRIMARY_SOURCES"],
        "Mixed Methods Research": ["QUANTITATIVE", "QUALITATIVE", "MIXED_METHODS", "DATA_ANALYSIS", "PRIMARY_SOURCES"],
        "Secondary Sources Only": ["QUANTITATIVE", "QUALITATIVE", "MIXED_METHODS", "DATA_ANALYSIS", "PRIMARY_SOURCES", "SECONDARY_SOURCES_EVALUATION"]
    }

