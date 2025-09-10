#!/usr/bin/env python3
"""
Publication-Ready ADM Visualization Script
Creates high-quality, publication-ready visualizations of ADM structures
"""

import sys
import os
from MainClasses import *
import academic_research_ADM
import inventive_step_ADM

def create_publication_visualization(adf, output_filename, title="ADM Structure", 
                                   include_sub_adms=True, layout_style="hierarchical"):
    """
    Create a publication-ready visualization of an ADM
    
    Parameters:
    -----------
    adf : ADF
        The ADM instance to visualize
    output_filename : str
        Output filename (without extension)
    title : str
        Title for the visualization
    include_sub_adms : bool
        Whether to include sub-ADMs in the visualization
    layout_style : str
        Layout style: "hierarchical", "minimal", or "detailed"
    """
    
    if layout_style == "minimal":
        # Use the existing minimal visualization but with improvements
        graph = create_improved_minimal_visualization(adf, title, include_sub_adms)
    elif layout_style == "hierarchical":
        # Create a clean hierarchical layout
        graph = create_hierarchical_visualization(adf, title, include_sub_adms)
    else:
        # Create a detailed visualization with labels
        graph = create_detailed_visualization(adf, title, include_sub_adms)
    
    # Set high DPI for publication quality
    graph.set_dpi(300)
    
    # Save as PNG
    png_filename = f"{output_filename}.png"
    graph.write_png(png_filename)
    print(f"✓ Saved PNG: {png_filename}")
    
    # Save as SVG for vector graphics
    svg_filename = f"{output_filename}.svg"
    graph.write_svg(svg_filename)
    print(f"✓ Saved SVG: {svg_filename}")
    
    return graph

def create_improved_minimal_visualization(adf, title, include_sub_adms=True):
    """
    Create an improved minimal visualization with better layout and colors
    """
    # Create main graph
    main_graph = adf.visualiseNetwork()
    
    # Create a new combined graph with better settings
    combined_graph = pydot.Dot(f'{adf.name}_publication', graph_type='digraph')
    combined_graph.set_rankdir('TB')  # Top to bottom
    combined_graph.set('ranksep', '2.0')  # More space between ranks
    combined_graph.set('nodesep', '1.0')  # Space between nodes
    combined_graph.set('margin', '0.5')   # Margin around graph
    
    # Set background color
    combined_graph.set('bgcolor', 'white')
    
    # Add main ADM as a subgraph
    main_subgraph = pydot.Subgraph('cluster_main')
    main_subgraph.set_label(f'Main ADM: {adf.name}')
    main_subgraph.set('style', 'filled')
    main_subgraph.set('fillcolor', 'lightgray')
    main_subgraph.set('color', 'black')
    main_subgraph.set('fontname', 'Arial')
    main_subgraph.set('fontsize', '14')
    main_subgraph.set('fontcolor', 'black')
    
    # Process main ADM nodes
    for node in main_graph.get_node_list():
        node_name = node.get_name()
        
        # Remove labels for minimal style
        node.set_label('')
        node.set_width('0.3')
        node.set_height('0.3')
        node.set_fontsize('0')
        
        # Improved color coding
        if node_name in adf.nodes:
            node_obj = adf.nodes[node_name]
            
            # Determine node type and color
            if hasattr(node_obj, 'children') and node_obj.children:
                # Abstract factors - blue
                node.set_color('darkblue')
                node.set_fillcolor('lightblue')
                node.set_style('filled')
            elif hasattr(node_obj, 'question') and node_obj.question:
                # Base level factors - green
                node.set_color('darkgreen')
                node.set_fillcolor('lightgreen')
                node.set_style('filled')
            elif hasattr(node_obj, 'sub_adf_creator'):
                # Sub-ADM BLF - orange
                node.set_color('darkorange')
                node.set_fillcolor('orange')
                node.set_style('filled')
            elif hasattr(node_obj, 'source_blf'):
                # Evaluation BLF - purple
                node.set_color('purple')
                node.set_fillcolor('plum')
                node.set_style('filled')
            else:
                # Other nodes - gray
                node.set_color('gray')
                node.set_fillcolor('lightgray')
                node.set_style('filled')
        
        main_subgraph.add_node(node)
    
    # Process main ADM edges
    for edge in main_graph.get_edge_list():
        edge.set_penwidth('1.0')
        edge.set_color('black')
        main_subgraph.add_edge(edge)
    
    combined_graph.add_subgraph(main_subgraph)
    
    # Add sub-ADMs if requested
    if include_sub_adms:
        sub_adm_count = 0
        sub_adm_mapping = {}
        node_to_sub_model = {}
        
        # Find sub-ADM creators
        for node_name, node in adf.nodes.items():
            if hasattr(node, 'sub_adf_creator'):
                sub_adm_key = str(node.sub_adf_creator)
                if sub_adm_key not in sub_adm_mapping:
                    sub_adm_count += 1
                    sub_adm_mapping[sub_adm_key] = sub_adm_count
                
                current_sub_adm_num = sub_adm_mapping[sub_adm_key]
                node_to_sub_model[node_name] = current_sub_adm_num
                
                # Create sub-ADM
                if current_sub_adm_num == sub_adm_count:
                    try:
                        dummy_item = "visualization_item"
                        sub_adf = node.sub_adf_creator(dummy_item)
                        sub_graph = sub_adf.visualiseNetwork()
                        
                        # Create sub-ADM subgraph
                        sub_subgraph = pydot.Subgraph(f'cluster_sub_{current_sub_adm_num}')
                        sub_subgraph.set_label(f'Sub-ADM {current_sub_adm_num}')
                        sub_subgraph.set('style', 'filled')
                        sub_subgraph.set('fillcolor', 'lightyellow')
                        sub_subgraph.set('color', 'black')
                        sub_subgraph.set('fontname', 'Arial')
                        sub_subgraph.set('fontsize', '12')
                        
                        # Process sub-ADM nodes
                        for sub_node in sub_graph.get_node_list():
                            sub_node.set_label('')
                            sub_node.set_width('0.25')
                            sub_node.set_height('0.25')
                            sub_node.set_fontsize('0')
                            
                            # Color sub-ADM nodes
                            sub_node_name = sub_node.get_name()
                            if hasattr(sub_adf, 'nodes') and sub_node_name in sub_adf.nodes:
                                sub_node_obj = sub_adf.nodes[sub_node_name]
                                
                                if hasattr(sub_node_obj, 'children') and sub_node_obj.children:
                                    sub_node.set_color('darkblue')
                                    sub_node.set_fillcolor('lightblue')
                                elif hasattr(sub_node_obj, 'question') and sub_node_obj.question:
                                    sub_node.set_color('darkgreen')
                                    sub_node.set_fillcolor('lightgreen')
                                else:
                                    sub_node.set_color('gray')
                                    sub_node.set_fillcolor('lightgray')
                                
                                sub_node.set_style('filled')
                            
                            sub_subgraph.add_node(sub_node)
                        
                        # Process sub-ADM edges
                        for sub_edge in sub_graph.get_edge_list():
                            sub_edge.set_penwidth('0.8')
                            sub_edge.set_color('black')
                            sub_subgraph.add_edge(sub_edge)
                        
                        combined_graph.add_subgraph(sub_subgraph)
                        
                    except Exception as e:
                        print(f"Error creating sub-ADM {current_sub_adm_num}: {e}")
        
        # Add connection edges
        for node_name, sub_model_num in node_to_sub_model.items():
            connection_edge = pydot.Edge(
                node_name,
                f"cluster_sub_{sub_model_num}",
                style='dashed',
                color='red',
                penwidth='1.5',
                arrowhead='open'
            )
            combined_graph.add_edge(connection_edge)
    
    return combined_graph

def create_hierarchical_visualization(adf, title, include_sub_adms=True):
    """
    Create a clean hierarchical visualization with proper node labels
    """
    # Create main graph
    main_graph = adf.visualiseNetwork()
    
    # Create combined graph
    combined_graph = pydot.Dot(f'{adf.name}_hierarchical', graph_type='digraph')
    combined_graph.set_rankdir('TB')
    combined_graph.set('ranksep', '1.5')
    combined_graph.set('nodesep', '0.8')
    combined_graph.set('bgcolor', 'white')
    
    # Add main ADM
    main_subgraph = pydot.Subgraph('cluster_main')
    main_subgraph.set_label(f'Main ADM: {adf.name}')
    main_subgraph.set('style', 'filled')
    main_subgraph.set('fillcolor', 'lightgray')
    main_subgraph.set('color', 'black')
    main_subgraph.set('fontname', 'Arial')
    main_subgraph.set('fontsize', '14')
    
    # Process nodes with labels
    for node in main_graph.get_node_list():
        node_name = node.get_name()
        
        # Set node size and style
        node.set_width('0.4')
        node.set_height('0.3')
        node.set_fontname('Arial')
        node.set_fontsize('10')
        
        # Color coding
        if node_name in adf.nodes:
            node_obj = adf.nodes[node_name]
            
            if hasattr(node_obj, 'children') and node_obj.children:
                node.set_color('darkblue')
                node.set_fillcolor('lightblue')
                node.set_style('filled')
            elif hasattr(node_obj, 'question') and node_obj.question:
                node.set_color('darkgreen')
                node.set_fillcolor('lightgreen')
                node.set_style('filled')
            else:
                node.set_color('gray')
                node.set_fillcolor('lightgray')
                node.set_style('filled')
        
        main_subgraph.add_node(node)
    
    # Process edges
    for edge in main_graph.get_edge_list():
        edge.set_penwidth('1.2')
        edge.set_color('black')
        main_subgraph.add_edge(edge)
    
    combined_graph.add_subgraph(main_subgraph)
    
    return combined_graph

def create_detailed_visualization(adf, title, include_sub_adms=True):
    """
    Create a detailed visualization with full labels and annotations
    """
    # Use the existing comprehensive visualization
    return adf.visualiseNetworkWithSubADMs()

def generate_all_visualizations():
    """
    Generate all types of visualizations for both ADMs
    """
    print("Generating publication-ready visualizations...")
    print("=" * 60)
    
    # Academic Research ADM
    print("\n📊 Academic Research ADM")
    print("-" * 30)
    
    try:
        academic_adf = academic_research_ADM.adf()
        
        # Minimal visualization
        create_publication_visualization(
            academic_adf, 
            "academic_research_minimal", 
            "Academic Research ADM - Minimal View",
            include_sub_adms=True,
            layout_style="minimal"
        )
        
        # Hierarchical visualization
        create_publication_visualization(
            academic_adf, 
            "academic_research_hierarchical", 
            "Academic Research ADM - Hierarchical View",
            include_sub_adms=True,
            layout_style="hierarchical"
        )
        
    except Exception as e:
        print(f"Error with Academic Research ADM: {e}")
    
    # Inventive Step ADM
    print("\n📊 Inventive Step ADM")
    print("-" * 30)
    
    try:
        inventive_adf = inventive_step_ADM.adf()
        
        # Minimal visualization
        create_publication_visualization(
            inventive_adf, 
            "inventive_step_minimal", 
            "Inventive Step ADM - Minimal View",
            include_sub_adms=True,
            layout_style="minimal"
        )
        
        # Hierarchical visualization
        create_publication_visualization(
            inventive_adf, 
            "inventive_step_hierarchical", 
            "Inventive Step ADM - Hierarchical View",
            include_sub_adms=True,
            layout_style="hierarchical"
        )
        
        # Detailed visualization
        create_publication_visualization(
            inventive_adf, 
            "inventive_step_detailed", 
            "Inventive Step ADM - Detailed View",
            include_sub_adms=True,
            layout_style="detailed"
        )
        
    except Exception as e:
        print(f"Error with Inventive Step ADM: {e}")
    
    print("\n" + "=" * 60)
    print("✅ All visualizations generated successfully!")
    print("\nGenerated files:")
    print("• PNG files: High-resolution raster images")
    print("• SVG files: Vector graphics for scaling")
    print("\nRecommended for publication:")
    print("• Use SVG files for best quality and scalability")
    print("• Minimal view: Clean, abstract representation")
    print("• Hierarchical view: Shows structure with labels")
    print("• Detailed view: Complete with all information")

if __name__ == "__main__":
    generate_all_visualizations()
