#!/usr/bin/env python3
"""
Split ADM Visualization with Correct Dependencies
Creates separate images with SkilledPerson as dependency of Hindsight and NonTechnicalContribution colored red
"""

import sys
import os
from MainClasses import *
import inventive_step_ADM

def create_main_adm_with_all_dependencies(adf):
    """
    Create the main ADM visualization with connection boxes and all sub-ADM dependencies
    """
    # Create main graph using the same method
    main_graph = adf.visualiseNetwork()
    
    # Create a new combined graph with the same settings as visualiseNetworkWithSubADMs
    combined_graph = pydot.Dot(f'{adf.name}_with_all_dependencies', graph_type='graph')
    combined_graph.set_rankdir('TB')  # Top to bottom for vertical layout
    
    # Add main ADM as a subgraph at the top (same as original)
    main_subgraph = pydot.Subgraph('cluster_main')
    main_subgraph.set_label(f'Main ADM: {adf.name}')
    
    # Copy all nodes and edges from main graph to main subgraph (same as original)
    for node in main_graph.get_node_list():
        main_subgraph.add_node(node)
    for edge in main_graph.get_edge_list():
        main_subgraph.add_edge(edge)
    
    # Add connection boxes for sub-ADMs and their dependencies
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
            
            # Add dependency edges for this sub-ADM
            if hasattr(node, 'dependency_node') and node.dependency_node:
                dependency_nodes = node.dependency_node
                if isinstance(dependency_nodes, str):
                    dependency_nodes = [dependency_nodes]
                
                for dep_node in dependency_nodes:
                    if dep_node in adf.nodes:
                        # Create dependency edge from dependency node to sub-ADM BLF
                        dep_edge = pydot.Edge(
                            dep_node,
                            node_name,
                            style='solid',
                            color='blue',
                            penwidth='1.0',
                            arrowhead='open'
                        )
                        combined_graph.add_edge(dep_edge)
    
    # Second pass: identify EvaluationBLF nodes that should link to the same sub-models
    for node_name, node in adf.nodes.items():
        if hasattr(node, 'source_blf') and node.source_blf in node_to_sub_model:
            source_sub_model = node_to_sub_model[node.source_blf]
            node_to_sub_model[node_name] = source_sub_model
            
            # Add dependency edge from source BLF to evaluation BLF
            eval_edge = pydot.Edge(
                node.source_blf,
                node_name,
                style='solid',
                color='purple',
                penwidth='1.0',
                arrowhead='open'
            )
            combined_graph.add_edge(eval_edge)
    
    # Third pass: create all connection edges from BLF nodes to connection boxes
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

def create_sub_adm_1_with_subadm_style(adf, sub_adf, sub_adm_num):
    """
    Create Sub-ADM 1 visualization using the exact same style as visualiseNetworkWithSubADMs
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

def create_sub_adm_2_with_correct_dependencies(adf, sub_adf, sub_adm_num):
    """
    Create Sub-ADM 2 visualization with SkilledPerson as dependency of Hindsight and NonTechnicalContribution colored red
    """
    # Create sub-ADM graph using the same method
    sub_graph = sub_adf.visualiseNetwork()
    
    # Create a new combined graph with the same settings
    combined_graph = pydot.Dot(f'Sub-Model_{sub_adm_num}', graph_type='graph')
    combined_graph.set_rankdir('TB')  # Top to bottom for vertical layout
    
    # Create a subgraph to position the sub-model
    sub_subgraph = pydot.Subgraph(f'cluster_sub_{sub_adm_num}')
    sub_subgraph.set_label(f'Sub-Model {sub_adm_num}')
    
    # Add all nodes and edges from the sub-ADM to the subgraph
    for sub_node in sub_graph.get_node_list():
        # Check if this is NonTechnicalContribution and color it red (outer ring only)
        if sub_node.get_name() == "NonTechnicalContribution":
            sub_node.set_color('red')  # Outer ring color
            sub_node.set_penwidth('3')  # Thicker border
            # Keep the original fill color (inner bit)
        
        sub_subgraph.add_node(sub_node)
    
    for sub_edge in sub_graph.get_edge_list():
        sub_subgraph.add_edge(sub_edge)
    
    # Add SkilledPerson dependency node (colored red outer ring only)
    skilled_person_node = pydot.Node("SkilledPerson",
                                   label="SkilledPerson",
                                   shape="ellipse",
                                   style="filled",
                                   fillcolor="white",  # White background
                                   color="red",  # Outer ring color (red)
                                   fontcolor="black",
                                   fontname="Arial",
                                   fontsize="10",  # Match other nodes
                                   penwidth="3")  # Thicker red border
    
    sub_subgraph.add_node(skilled_person_node)
    
    # Add dotted dependency edge from SkilledPerson to Hindsight
    if "Hindsight" in sub_adf.nodes:
        dependency_edge = pydot.Edge(
            "SkilledPerson",
            "Hindsight",
            style='dotted',
            color='black',
            penwidth='2.0',
            arrowhead='open'
        )
        combined_graph.add_edge(dependency_edge)
        
        # Add rank constraint to position SkilledPerson below Hindsight
        rank_constraint = pydot.Edge(
            "Hindsight",
            "SkilledPerson",
            style='invis'  # Invisible edge for ranking only
        )
        combined_graph.add_edge(rank_constraint)
    else:
        print("Warning: Hindsight node not found in Sub-ADM 2")
    
    combined_graph.add_subgraph(sub_subgraph)
    
    return combined_graph

def create_inventive_step_split_with_correct_dependencies():
    """
    Create split visualizations for Inventive Step ADM with correct dependencies
    """
    print("=" * 60)
    print("INVENTIVE STEP ADM - SPLIT WITH CORRECT DEPENDENCIES")
    print("=" * 60)
    
    # Load the ADM
    adf = inventive_step_ADM.adf()
    
    # 1. Create main ADM with all dependencies
    print("Creating main ADM with all dependencies...")
    main_graph = create_main_adm_with_all_dependencies(adf)
    
    # Save main ADM
    main_png = "inventive_step_main_with_dependencies.png"
    main_svg = "inventive_step_main_with_dependencies.svg"
    main_graph.write_png(main_png)
    main_graph.write_svg(main_svg)
    print(f"✓ Saved main ADM with all dependencies: {main_png}, {main_svg}")
    
    # 2. Find and create sub-ADM visualizations
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
                    
                    # Create sub-ADM graph with special handling for Sub-ADM 2
                    if sub_adm_count == 2:
                        sub_graph = create_sub_adm_2_with_correct_dependencies(adf, sub_adf, sub_adm_count)
                        print(f"✓ Created Sub-ADM {sub_adm_count} with SkilledPerson dependency of Hindsight and NonTechnicalContribution colored red")
                    else:
                        sub_graph = create_sub_adm_1_with_subadm_style(adf, sub_adf, sub_adm_count)
                    
                    # Save sub-ADM
                    sub_png = f"inventive_step_sub_adm_{sub_adm_count}.png"
                    sub_svg = f"inventive_step_sub_adm_{sub_adm_count}.svg"
                    sub_graph.write_png(sub_png)
                    sub_graph.write_svg(sub_svg)
                    print(f"✓ Saved Sub-ADM {sub_adm_count}: {sub_png}, {sub_svg}")
                    
                except Exception as e:
                    print(f"❌ Error creating Sub-ADM {sub_adm_count}: {e}")
    
    print(f"\n✅ Generated {1 + sub_adm_count} separate visualizations:")
    print(f"  • 1 main ADM image (with all dependencies)")
    print(f"  • {sub_adm_count} sub-ADM images")
    print(f"  • Sub-ADM 2 includes SkilledPerson dependency of Hindsight (dotted black line)")
    print(f"  • Sub-ADM 2 includes NonTechnicalContribution with red outer ring")
    
    return sub_adm_count

def main():
    """
    Generate split visualizations for Inventive Step ADM with correct dependencies
    """
    print("Creating split Inventive Step ADM visualizations...")
    print("Sub-ADM 2 will include SkilledPerson as dependency of Hindsight and NonTechnicalContribution colored red")
    
    try:
        sub_adm_count = create_inventive_step_split_with_correct_dependencies()
        
        print("\n" + "=" * 60)
        print("✅ SPLIT VISUALIZATIONS COMPLETED!")
        print(f"Total images generated: {1 + sub_adm_count}")
        print("\nMain ADM includes:")
        print("• All main ADM nodes and connections")
        print("• Connection boxes showing where sub-ADMs connect")
        print("• Blue dependency edges: Sub-ADM BLFs depend on other nodes")
        print("• Purple evaluation edges: EvaluationBLFs depend on Sub-ADM results")
        print("• Red dashed lines: From BLF nodes to connection boxes")
        print("\nSub-ADM 2 includes:")
        print("• SkilledPerson dependency node (red outer ring only)")
        print("• Dotted black line from SkilledPerson to Hindsight")
        print("• NonTechnicalContribution node with red outer ring")
        print("\nFiles generated:")
        print("• inventive_step_main_with_dependencies.png/svg")
        print("• inventive_step_sub_adm_1.png/svg")
        print("• inventive_step_sub_adm_2.png/svg (with correct dependencies)")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
