#!/usr/bin/env python3
"""
Split ADM Visualization with Sub-ADMs Style
Creates separate images using the exact same style as visualiseNetworkWithSubADMs
"""

import sys
import os
from MainClasses import *
import inventive_step_ADM

def create_main_adm_with_subadm_style(adf):
    """
    Create the main ADM visualization using the exact same style as visualiseNetworkWithSubADMs
    but without the sub-ADMs (just the main ADM part)
    """
    # Create main graph using the same method
    main_graph = adf.visualiseNetwork()
    
    # Create a new combined graph with the same settings as visualiseNetworkWithSubADMs
    combined_graph = pydot.Dot(f'{adf.name}_with_subADMs', graph_type='graph')
    combined_graph.set_rankdir('TB')  # Top to bottom for vertical layout
    
    # Add main ADM as a subgraph at the top (same as original)
    main_subgraph = pydot.Subgraph('cluster_main')
    main_subgraph.set_label(f'Main ADM: {adf.name}')
    
    # Copy all nodes and edges from main graph to main subgraph (same as original)
    for node in main_graph.get_node_list():
        main_subgraph.add_node(node)
    for edge in main_graph.get_edge_list():
        main_subgraph.add_edge(edge)
    
    combined_graph.add_subgraph(main_subgraph)
    
    return combined_graph

def create_sub_adm_with_subadm_style(adf, sub_adf, sub_adm_num):
    """
    Create a sub-ADM visualization using the exact same style as visualiseNetworkWithSubADMs
    """
    # Create sub-ADM graph using the same method
    sub_graph = sub_adf.visualiseNetwork()
    
    # Create a new combined graph with the same settings
    combined_graph = pydot.Dot(f'Sub-Model_{sub_adm_num}', graph_type='graph')
    combined_graph.set_rankdir('TB')  # Top to bottom for vertical layout
    
    # Create a subgraph to position the sub-model (same as original)
    sub_subgraph = pydot.Subgraph(f'cluster_sub_{sub_adm_num}')
    sub_subgraph.set_label(f'Sub-Model {sub_adm_num}')
    
    # Add all nodes and edges from the sub-ADM to the subgraph (same as original)
    for sub_node in sub_graph.get_node_list():
        sub_subgraph.add_node(sub_node)
    for sub_edge in sub_graph.get_edge_list():
        sub_subgraph.add_edge(sub_edge)
    
    combined_graph.add_subgraph(sub_subgraph)
    
    return combined_graph

def create_inventive_step_split_with_subadm_style():
    """
    Create split visualizations for Inventive Step ADM using the exact sub-ADM style
    """
    print("=" * 60)
    print("INVENTIVE STEP ADM - SPLIT WITH SUB-ADM STYLE")
    print("=" * 60)
    
    # Load the ADM
    adf = inventive_step_ADM.adf()
    
    # 1. Create main ADM with sub-ADM style
    print("Creating main ADM with sub-ADM style...")
    main_graph = create_main_adm_with_subadm_style(adf)
    
    # Save main ADM
    main_png = "inventive_step_main_subadm_style.png"
    main_svg = "inventive_step_main_subadm_style.svg"
    main_graph.write_png(main_png)
    main_graph.write_svg(main_svg)
    print(f"✓ Saved main ADM: {main_png}, {main_svg}")
    
    # 2. Find and create sub-ADM visualizations with sub-ADM style
    sub_adm_count = 0
    sub_adm_mapping = {}
    
    # Find all sub-ADM creators
    for node_name, node in adf.nodes.items():
        if hasattr(node, 'sub_adf_creator'):
            sub_adm_key = str(node.sub_adf_creator)
            if sub_adm_key not in sub_adm_mapping:
                sub_adm_count += 1
                sub_adm_mapping[sub_adm_key] = sub_adm_count
                
                # Create sub-ADM instance
                try:
                    dummy_item = "visualization_item"
                    sub_adf = node.sub_adf_creator(dummy_item)
                    
                    # Create sub-ADM graph with sub-ADM style
                    sub_graph = create_sub_adm_with_subadm_style(adf, sub_adf, sub_adm_count)
                    
                    # Save sub-ADM
                    sub_png = f"inventive_step_sub_adm_{sub_adm_count}_subadm_style.png"
                    sub_svg = f"inventive_step_sub_adm_{sub_adm_count}_subadm_style.svg"
                    sub_graph.write_png(sub_png)
                    sub_graph.write_svg(sub_svg)
                    print(f"✓ Saved Sub-ADM {sub_adm_count}: {sub_png}, {sub_svg}")
                    
                except Exception as e:
                    print(f"❌ Error creating Sub-ADM {sub_adm_count}: {e}")
    
    print(f"\n✅ Generated {1 + sub_adm_count} separate visualizations:")
    print(f"  • 1 main ADM image (with sub-ADM styling)")
    print(f"  • {sub_adm_count} sub-ADM images (with sub-ADM styling)")
    
    return sub_adm_count

def main():
    """
    Generate split visualizations for Inventive Step ADM using sub-ADM style
    """
    print("Creating split Inventive Step ADM visualizations...")
    print("Using the exact same style as visualiseNetworkWithSubADMs")
    
    try:
        sub_adm_count = create_inventive_step_split_with_subadm_style()
        
        print("\n" + "=" * 60)
        print("✅ SPLIT VISUALIZATIONS COMPLETED!")
        print(f"Total images generated: {1 + sub_adm_count}")
        print("\nEach image uses the exact same styling as visualiseNetworkWithSubADMs:")
        print("• Same colors, fonts, and layout")
        print("• Same node styling and edge appearance")
        print("• Same subgraph organization")
        print("\nFiles generated:")
        print("• inventive_step_main_subadm_style.png/svg")
        print("• inventive_step_sub_adm_1_subadm_style.png/svg")
        print("• inventive_step_sub_adm_2_subadm_style.png/svg")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
