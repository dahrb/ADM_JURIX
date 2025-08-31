#!/usr/bin/env python3
"""
Toy ADM - Argumentation Decision Framework
"""

from MainClasses import *

# Add PRIMARY_SOURCES BLF that evaluates sub-ADMs for each source
def create_sub_adm_1(item_name):
    """Creates a sub-ADM for evaluating individual sources"""
    sub_adf = SubADM("Sub-ADM 1", item_name)
    
    # Add BLFs for the sub-ADM - {item} will be automatically resolved
    sub_adf.addNodes("POSITIVE_DATA", question="Is {item} primary data (collected directly)?")
    sub_adf.addNodes("NEGATIVE_DATA", question="Is {item} secondary data (from existing sources)?")
    
    # Add abstract factors
    sub_adf.addNodes("POSITIVE_RESOURCE", ["POSITIVE_DATA and not NEGATIVE_DATA"], ["POSITIVE_RESOURCE is accepted - primary source", "POSITIVE_RESOURCE is rejected - not primary"])
    sub_adf.addNodes("NEGATIVE_RESOURCE", ["NEGATIVE_DATA and not POSITIVE_DATA"], ["NEGATIVE_RESOURCE is accepted - secondary source", "NEGATIVE_RESOURCE is rejected - not secondary"])
    
    sub_adf.questionOrder = ["POSITIVE_DATA", "NEGATIVE_DATA"]
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
        "research_type"
    )

    adf.addNodes("MIXED_METHODS", ["QUANTITATIVE and QUALITATIVE"], ["MIXED_METHODS is accepted", "MIXED_METHODS is rejected"])
    adf.addNodes("NOVELTY",question="Is your research novel?")

    # Add DATA_ANALYSIS BLF that depends on MIXED_METHODS and inherits its facts
    adf.addDependentBLF("DATA_ANALYSIS", 
                        "MIXED_METHODS",  # Dependency on MIXED_METHODS
                        "Are {QUANTITATIVE_method}, {QUALITATIVE_method} appropriate for your data type?",
                        ["DATA_ANALYSIS is accepted - methods are appropriate", "DATA_ANALYSIS is rejected - methods are not appropriate"])
    
    # Uses a function to collect sources dynamically
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
    
    adf.addSubADMBLF("PRIMARY_SOURCES", create_sub_adm_1, collect_sources)
    
    # Add SECONDARY_SOURCES as an EvaluationBLF that evaluates sub-ADM results
    adf.addEvaluationBLF("SECONDARY_SOURCES_EVALUATION", 
                         "PRIMARY_SOURCES",  # Source BLF to check
                         "NEGATIVE_RESOURCE",  # Condition to look for
                         ["SECONDARY_SOURCES is accepted - you have secondary sources", 
                          "SECONDARY_SOURCES is rejected - no secondary sources"])
    
    adf.addNodes("RESEARCH_QUALITY", [
        "PRIMARY_SOURCES and not SECONDARY_SOURCES_EVALUATION and DATA_ANALYSIS"
    ], [
        "RESEARCH_QUALITY is accepted - your research has high quality with primary sources, no secondary sources, and appropriate methodology",
        "RESEARCH_QUALITY is rejected - your research may not meet quality standards"
    ])

    # Set question order
    adf.questionOrder = ["research_type", "NOVELTY", "DATA_ANALYSIS", "PRIMARY_SOURCES", "SECONDARY_SOURCES_EVALUATION"]
    
    return adf

def cases():
    """
    Returns predefined cases for testing
    """
    return {
        "test_case": ["QUANTITATIVE", "QUALITATIVE", "MIXED_METHODS", "DATA_ANALYSIS"]
    }

# Create an instance for direct import
adf = adf()
