#!/usr/bin/env python3
"""
Inventive Step ADM - Argumentation Decision Framework
Simple example with 2 BLFs and 1 abstract factor
"""

from MainClasses import *

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
            "QUANTITATIVE": {"method": "What specific quantitative method will you use?"},
            "QUALITATIVE": {"method": "What specific qualitative method will you use?"}
        },
        "question_1"
    )
    
    # Add ETHICS_APPROVAL BLF
    adf.addNodes("ETHICS_APPROVAL", None, [
        "ETHICS_APPROVAL is accepted", 
        "ETHICS_APPROVAL is rejected"
    ], "Do you need ethics approval for your research?")
    
    # Add SOURCES algorithmic question
    sources_algorithm_config = {
        'input_questions': [
            "What sources do you have access to? (comma-separated list)",
            "What sources do you need for your research? (comma-separated list)"
        ],
        'algorithm': lambda inputs: [
            item.strip() for item in inputs[1].split(',') 
            if item.strip() not in [i.strip() for i in inputs[0].split(',')]
        ],
        'acceptance_condition': ">= 1"  # Accept if missing sources list has 1 or more items
    }
    
    adf.addAlgorithmicQuestion("SOURCES", sources_algorithm_config, [
        "SOURCES is accepted - you need to acquire missing sources for your research",
        "SOURCES is rejected - you have all the sources needed for your research"
    ])
    
    # Add PRIMARY_SOURCES BLF that evaluates sub-ADMs for each source
    def create_source_sub_adm():
        """Creates a sub-ADM for evaluating individual sources"""
        sub_adf = ADF("SourceEvaluation")
        
        # Add BLFs for the sub-ADM
        sub_adf.addNodes("PRIMARY_DATA", None, ["PRIMARY_DATA is accepted", "PRIMARY_DATA is rejected"], "Is {INGREDIENT_name} primary data (collected directly)?")
        sub_adf.addNodes("SECONDARY_DATA", None, ["SECONDARY_DATA is accepted", "SECONDARY_DATA is rejected"], "Is {INGREDIENT_name} secondary data (from existing sources)?")
        
        # Add abstract factors
        sub_adf.addNodes("PRIMARY_RESOURCE", ["PRIMARY_DATA and not SECONDARY_DATA"], ["PRIMARY_RESOURCE is accepted - primary source", "PRIMARY_RESOURCE is rejected - not primary"])
        sub_adf.addNodes("SECONDARY_RESOURCE", ["SECONDARY_DATA and not PRIMARY_DATA"], ["SECONDARY_RESOURCE is accepted - secondary source", "SECONDARY_RESOURCE is rejected - not secondary"])
        
        return sub_adf
    
    adf.addSubADMBLF("PRIMARY_SOURCES", create_source_sub_adm, "SOURCES", [
        "PRIMARY_SOURCES is accepted - you have primary sources for your research",
        "PRIMARY_SOURCES is rejected - no primary sources available"
    ])
    
    # Add SECONDARY_SOURCES BLF
    adf.addNodes("SECONDARY_SOURCES", None, [
        "SECONDARY_SOURCES is accepted", 
        "SECONDARY_SOURCES is rejected"
    ], "Do you have access to secondary sources?")
    
    # Add root node RESEARCH_QUALITY with acceptance condition PRIMARY_SOURCES and not SECONDARY_SOURCES and DATA_ANALYSIS
    # Note: DATA_ANALYSIS is inherited from QUANTITATIVE/QUALITATIVE (the method fact)
    adf.addNodes("RESEARCH_QUALITY", ["PRIMARY_SOURCES and not SECONDARY_SOURCES and QUANTITATIVE or PRIMARY_SOURCES and not SECONDARY_SOURCES and QUALITATIVE"], [
        "RESEARCH_QUALITY is accepted - your research has high quality with primary sources, no secondary sources, and appropriate data analysis methods",
        "RESEARCH_QUALITY is rejected - your research may not meet quality standards"
    ])
    
    # Set the question order to include all questions
    adf.questionOrder = ["question_1", "ETHICS_APPROVAL", "SOURCES", "PRIMARY_SOURCES", "SECONDARY_SOURCES"]
    
    return adf





