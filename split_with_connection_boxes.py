#!/usr/bin/env python3
"""
Split ADM Visualization with Connection Boxes
Creates separate images with connection boxes showing where sub-ADMs connect
"""

import sys
import os
from MainClasses import *
import inventive_step_ADM

def create_main_adm_with_connection_boxes(adf):
    """
    Create the main ADM visualization with connection boxes showing where sub-ADMs connect
    """
    # Create main graph using the same method
    main_graph = adf.visualiseNetwork()
    
    # Create a new combined graph with the same settings as visualiseNetworkWithSubADMs
    combined_graph = pydot.Dot(f'{adf.name}_with_connection_boxes', graph_type='graph')
    combined_graph.set_rankdir('TB')  # Top to bottom for vertical layout
    
    # Add main ADM as a subgraph at the top (same as original)
    main_subgraph = pydot.Subgraph('cluster_main')
    main_subgraph.set_label(f'Main ADM: {adf.name}')
    
    # Copy all nodes and edges from main graph to main subgraph (same as original)
    for node in main_graph.get_node_list():
        main_subgraph.add_node(node)
    for edge in main_graph.get_edge_list():
        main_subgraph.add_edge(edge)
    
    # Add connection boxes for sub-ADMs (like in the original visualiseNetworkWithSubADMs)
    sub_adm_count = 0
    sub_adm_mapping = {}
    node_to_sub_model = {}
    
    # First pass: identify all sub-ADM creators and create connection boxes
    for node_name, node in adf.nodes.items():
        if hasattr(node, 'sub_adf_creator'):
            sub_adm_key = str(node.sub_adf_creator)
            if sub_adm_key not in sub_adm_mapping:
                sub_adm_count += 1
                sub_adm_mapping[sub_adm_key] = sub_adm_count
            
            current_sub_adm_num = sub_adm_mapping[sub_adm_key]
            node_to_sub_model[node_name] = current_sub_adm_num
            
            # Create connection box (like in original)
            label_node = pydot.Node(f"sub_model_label_{current_sub_adm_num}", 
                                   label=f"SUB-MODEL {current_sub_adm_num}",
                                   shape="box",
                                   style="filled",
                                   fillcolor="lightgreen",
                                   width="1.5",
                                   height="0.5")
            
            # Add the label node to the main subgraph
            main_subgraph.add_node(label_node)
    
    # Second pass: identify EvaluationBLF nodes that should link to the same sub-models
    for node_name, node in adf.nodes.items():
        if hasattr(node, 'source_blf') and node.source_blf in node_to_sub_model:
            source_sub_model = node_to_sub_model[node.source_blf]
            node_to_sub_model[node_name] = source_sub_model
    
    # Third pass: create all connection edges
    for node_name, sub_model_num in node_to_sub_model.items():
        connection_edge = pydot.Edge(
            node_name,
            f"sub_model_label_{sub_model_num}",
            style='dashed',
            color='red',
            penwidth='0.5',
        )
        combined_graph.add_edge(connection_edge)
    
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

def create_inventive_step_split_with_connection_boxes():
    """
    Create split visualizations for Inventive Step ADM with connection boxes
    """
    print("=" * 60)
    print("INVENTIVE STEP ADM - SPLIT WITH CONNECTION BOXES")
    print("=" * 60)
    
    # Load the ADM
    adf = inventive_step_ADM.adf()
    
    # 1. Create main ADM with connection boxes
    print("Creating main ADM with connection boxes...")
    main_graph = create_main_adm_with_connection_boxes(adf)
    
    # Save main ADM
    main_png = "inventive_step_main_with_boxes.png"
    main_svg = "inventive_step_main_with_boxes.svg"
    main_graph.write_png(main_png)
    main_graph.write_svg(main_svg)
    print(f"✓ Saved main ADM with connection boxes: {main_png}, {main_svg}")
    
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
                    sub_png = f"inventive_step_sub_adm_{sub_adm_count}.png"
                    sub_svg = f"inventive_step_sub_adm_{sub_adm_count}.svg"
                    sub_graph.write_png(sub_png)
                    sub_graph.write_svg(sub_svg)
                    print(f"✓ Saved Sub-ADM {sub_adm_count}: {sub_png}, {sub_svg}")
                    
                except Exception as e:
                    print(f"❌ Error creating Sub-ADM {sub_adm_count}: {e}")
    
    print(f"\n✅ Generated {1 + sub_adm_count} separate visualizations:")
    print(f"  • 1 main ADM image (with connection boxes)")
    print(f"  • {sub_adm_count} sub-ADM images")
    
    return sub_adm_count

def main():
    """
    Generate split visualizations for Inventive Step ADM with connection boxes
    """
    print("Creating split Inventive Step ADM visualizations...")
    print("Main ADM includes connection boxes showing where sub-ADMs connect")
    
    try:
        sub_adm_count = create_inventive_step_split_with_connection_boxes()
        
        print("\n" + "=" * 60)
        print("✅ SPLIT VISUALIZATIONS COMPLETED!")
        print(f"Total images generated: {1 + sub_adm_count}")
        print("\nMain ADM includes:")
        print("• All main ADM nodes and connections")
        print("• Connection boxes showing where sub-ADMs connect")
        print("• Dashed red lines from BLF nodes to connection boxes")
        print("\nFiles generated:")
        print("• inventive_step_main_with_boxes.png/svg")
        print("• inventive_step_sub_adm_1.png/svg")
        print("• inventive_step_sub_adm_2.png/svg")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
