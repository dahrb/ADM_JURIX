#!/usr/bin/env python3
"""
Toy ADM - Argumentation Decision Framework
"""

from MainClasses_2 import *


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
    
    adf.questionOrder = ["research_type","NOVELTY","DATA_ANALYSIS"]
    return adf

def cases():
    cases = {}
    return  cases
