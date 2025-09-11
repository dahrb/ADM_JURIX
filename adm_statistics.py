#!/usr/bin/env python3
"""
ADM Statistics Script
Provides descriptive statistics for ADM structures including main ADM and sub-ADMs
"""

import sys
import os
from MainClasses import *
import inventive_step_ADM

def analyze_adm_structure(adf, adm_name="Main ADM"):
    """
    Analyze an ADM structure and return statistics about leaf and non-leaf nodes
    
    Parameters:
    -----------
    adf : ADF
        The ADM instance to analyze
    adm_name : str
        Name of the ADM for reporting
        
    Returns:
    --------
    dict : Statistics about the ADM structure
    """
    # Generate non-leaf nodes first
    adf.nonLeafGen()
    
    # Count total nodes
    total_nodes = len(adf.nodes)
    
    # Count leaf nodes (nodes without children)
    leaf_nodes = 0
    non_leaf_nodes = 0
    
    for node_name, node in adf.nodes.items():
        if hasattr(node, 'children') and node.children is not None and len(node.children) > 0:
            non_leaf_nodes += 1
        else:
            leaf_nodes += 1
    
    # Count different node types
    blf_nodes = 0  # Base Level Factors (nodes with questions)
    abstract_nodes = 0  # Abstract factors (nodes with acceptance conditions)
    other_nodes = 0  # Other types
    
    for node_name, node in adf.nodes.items():
        if hasattr(node, 'question') and node.question is not None:
            blf_nodes += 1
        elif hasattr(node, 'acceptance') and node.acceptance is not None:
            abstract_nodes += 1
        else:
            other_nodes += 1
    
    # Count sub-ADM related nodes
    sub_adm_blf_nodes = 0
    evaluation_blf_nodes = 0
    
    for node_name, node in adf.nodes.items():
        if hasattr(node, 'source_blf') and hasattr(node, 'sub_adm_creator'):
            sub_adm_blf_nodes += 1
        elif hasattr(node, 'source_blf') and hasattr(node, 'condition_to_check'):
            evaluation_blf_nodes += 1
    
    return {
        'adm_name': adm_name,
        'total_nodes': total_nodes,
        'leaf_nodes': leaf_nodes,
        'non_leaf_nodes': non_leaf_nodes,
        'blf_nodes': blf_nodes,
        'abstract_nodes': abstract_nodes,
        'other_nodes': other_nodes,
        'sub_adm_blf_nodes': sub_adm_blf_nodes,
        'evaluation_blf_nodes': evaluation_blf_nodes
    }

def analyze_sub_adm_structure(sub_adm_creator, sub_adm_name, item_name="test_item"):
    """
    Analyze a sub-ADM structure by creating an instance and analyzing it
    
    Parameters:
    -----------
    sub_adm_creator : function
        Function that creates a sub-ADM instance
    sub_adm_name : str
        Name of the sub-ADM for reporting
    item_name : str
        Item name to pass to the sub-ADM creator
        
    Returns:
    --------
    dict : Statistics about the sub-ADM structure
    """
    try:
        # Create sub-ADM instance
        sub_adf = sub_adm_creator(item_name)
        
        # Analyze the structure
        stats = analyze_adm_structure(sub_adf, sub_adm_name)
        return stats
    except Exception as e:
        print(f"Error analyzing {sub_adm_name}: {e}")
        return {
            'adm_name': sub_adm_name,
            'total_nodes': 0,
            'leaf_nodes': 0,
            'non_leaf_nodes': 0,
            'blf_nodes': 0,
            'abstract_nodes': 0,
            'other_nodes': 0,
            'sub_adm_blf_nodes': 0,
            'evaluation_blf_nodes': 0,
            'error': str(e)
        }

def print_statistics(stats_list):
    """
    Print formatted statistics for all ADMs and sub-ADMs
    
    Parameters:
    -----------
    stats_list : list
        List of statistics dictionaries
    """
    print("=" * 80)
    print("ADM DESCRIPTIVE STATISTICS")
    print("=" * 80)
    print()
    
    # Print individual ADM statistics
    for stats in stats_list:
        print(f"📊 {stats['adm_name']}")
        print("-" * 50)
        
        if 'error' in stats:
            print(f"❌ Error: {stats['error']}")
            print()
            continue
            
        print(f"Total Nodes: {stats['total_nodes']}")
        print(f"  ├─ Leaf Nodes: {stats['leaf_nodes']}")
        print(f"  └─ Non-Leaf Nodes: {stats['non_leaf_nodes']}")
        print()
        print(f"Node Types:")
        print(f"  ├─ Base Level Factors (BLF): {stats['blf_nodes']}")
        print(f"  ├─ Abstract Factors: {stats['abstract_nodes']}")
        print(f"  ├─ Other Nodes: {stats['other_nodes']}")
        print(f"  ├─ Sub-ADM BLF Nodes: {stats['sub_adm_blf_nodes']}")
        print(f"  └─ Evaluation BLF Nodes: {stats['evaluation_blf_nodes']}")
        print()
    
    # Print summary statistics
    print("=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    
    # Separate main ADMs from sub-ADMs
    main_adms = [s for s in stats_list if not s['adm_name'].startswith('Sub-') and 'error' not in s]
    sub_adms = [s for s in stats_list if s['adm_name'].startswith('Sub-') and 'error' not in s]
    
    if main_adms:
        print(f"\n📈 Main ADMs ({len(main_adms)} total):")
        total_main_nodes = sum(s['total_nodes'] for s in main_adms)
        total_main_leaf = sum(s['leaf_nodes'] for s in main_adms)
        total_main_non_leaf = sum(s['non_leaf_nodes'] for s in main_adms)
        
        print(f"  Total Nodes: {total_main_nodes}")
        print(f"  Leaf Nodes: {total_main_leaf} ({total_main_leaf/total_main_nodes*100:.1f}%)")
        print(f"  Non-Leaf Nodes: {total_main_non_leaf} ({total_main_non_leaf/total_main_nodes*100:.1f}%)")
    
    if sub_adms:
        print(f"\n📈 Sub-ADMs ({len(sub_adms)} total):")
        total_sub_nodes = sum(s['total_nodes'] for s in sub_adms)
        total_sub_leaf = sum(s['leaf_nodes'] for s in sub_adms)
        total_sub_non_leaf = sum(s['non_leaf_nodes'] for s in sub_adms)
        
        print(f"  Total Nodes: {total_sub_nodes}")
        print(f"  Leaf Nodes: {total_sub_leaf} ({total_sub_leaf/total_sub_nodes*100:.1f}%)")
        print(f"  Non-Leaf Nodes: {total_sub_non_leaf} ({total_sub_non_leaf/total_sub_nodes*100:.1f}%)")
    
    # Overall totals
    all_valid_stats = [s for s in stats_list if 'error' not in s]
    if all_valid_stats:
        total_all_nodes = sum(s['total_nodes'] for s in all_valid_stats)
        total_all_leaf = sum(s['leaf_nodes'] for s in all_valid_stats)
        total_all_non_leaf = sum(s['non_leaf_nodes'] for s in all_valid_stats)
        
        print(f"\n📈 Overall Totals ({len(all_valid_stats)} ADMs total):")
        print(f"  Total Nodes: {total_all_nodes}")
        print(f"  Leaf Nodes: {total_all_leaf} ({total_all_leaf/total_all_nodes*100:.1f}%)")
        print(f"  Non-Leaf Nodes: {total_all_non_leaf} ({total_all_non_leaf/total_all_nodes*100:.1f}%)")

def main():
    """Main function to analyze Inventive Step ADM only"""
    print("Loading and analyzing Inventive Step ADM structure...")
    print()
    
    stats_list = []
    
    # Analyze Inventive Step ADM
    try:
        print("Analyzing Inventive Step ADM...")
        inventive_adf = inventive_step_ADM.adf()
        inventive_stats = analyze_adm_structure(inventive_adf, "Inventive Step ADM")
        stats_list.append(inventive_stats)
        
        # Analyze its sub-ADMs
        sub_adm_1_stats = analyze_sub_adm_structure(
            inventive_step_ADM.create_sub_adm_1, 
            "Sub-ADM 1 (Inventive Step)"
        )
        stats_list.append(sub_adm_1_stats)
        
        sub_adm_2_stats = analyze_sub_adm_structure(
            inventive_step_ADM.create_sub_adm_2, 
            "Sub-ADM 2 (Inventive Step)"
        )
        stats_list.append(sub_adm_2_stats)
        
    except Exception as e:
        print(f"Error analyzing Inventive Step ADM: {e}")
    
    # Print all statistics
    print_statistics(stats_list)

if __name__ == "__main__":
    main()
