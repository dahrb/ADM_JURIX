#!/usr/bin/env python3
"""
Enhanced Inventive Step ADM Visualization
Creates a publication-ready visualization specifically for the Inventive Step ADM
"""

import sys
import os
from MainClasses import *
import inventive_step_ADM

def create_enhanced_inventive_step_visualization():
    """
    Create an enhanced visualization of the Inventive Step ADM for publication
    """
    print("Creating enhanced Inventive Step ADM visualization...")
    
    # Load the ADM
    adf = inventive_step_ADM.adf()
    
    # Create the main graph
    main_graph = adf.visualiseNetwork()
    
    # Create enhanced combined graph
    combined_graph = pydot.Dot('Inventive_Step_Enhanced', graph_type='digraph')
    combined_graph.set_rankdir('TB')  # Top to bottom
    combined_graph.set('ranksep', '3.0')  # More space between ranks
    combined_graph.set('nodesep', '1.5')  # Space between nodes
    combined_graph.set('margin', '1.0')   # Margin around graph
    combined_graph.set('bgcolor', 'white')
    combined_graph.set('dpi', '300')  # High DPI for publication
    
    # Add main ADM as a subgraph
    main_subgraph = pydot.Subgraph('cluster_main')
    main_subgraph.set_label('Main ADM: Inventive Step Analysis')
    main_subgraph.set('style', 'filled')
    main_subgraph.set('fillcolor', 'lightgray')
    main_subgraph.set('color', 'black')
    main_subgraph.set('fontname', 'Arial')
    main_subgraph.set('fontsize', '16')
    main_subgraph.set('fontcolor', 'black')
    main_subgraph.set('penwidth', '2')
    
    # Process main ADM nodes with enhanced styling
    for node in main_graph.get_node_list():
        node_name = node.get_name()
        
        # Remove labels for clean minimal look
        node.set_label('')
        node.set_width('0.4')
        node.set_height('0.3')
        node.set_fontsize('0')
        
        # Enhanced color coding based on node type
        if node_name in adf.nodes:
            node_obj = adf.nodes[node_name]
            
            # Determine node type and apply appropriate styling
            if hasattr(node_obj, 'children') and node_obj.children:
                # Abstract factors - blue with stronger contrast
                node.set_color('darkblue')
                node.set_fillcolor('lightblue')
                node.set_style('filled')
                node.set_penwidth('2')
            elif hasattr(node_obj, 'question') and node_obj.question:
                # Base level factors - green
                node.set_color('darkgreen')
                node.set_fillcolor('lightgreen')
                node.set_style('filled')
                node.set_penwidth('2')
            elif hasattr(node_obj, 'sub_adf_creator'):
                # Sub-ADM BLF - orange/red
                node.set_color('darkred')
                node.set_fillcolor('orange')
                node.set_style('filled')
                node.set_penwidth('3')
            elif hasattr(node_obj, 'source_blf'):
                # Evaluation BLF - purple
                node.set_color('purple')
                node.set_fillcolor('plum')
                node.set_style('filled')
                node.set_penwidth('2')
            else:
                # Other nodes - gray
                node.set_color('gray')
                node.set_fillcolor('lightgray')
                node.set_style('filled')
                node.set_penwidth('1')
        
        main_subgraph.add_node(node)
    
    # Process main ADM edges with enhanced styling
    for edge in main_graph.get_edge_list():
        edge.set_penwidth('1.5')
        edge.set_color('black')
        edge.set_arrowsize('1.2')
        main_subgraph.add_edge(edge)
    
    combined_graph.add_subgraph(main_subgraph)
    
    # Add sub-ADMs with enhanced styling
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
                    
                    # Create sub-ADM subgraph with enhanced styling
                    sub_subgraph = pydot.Subgraph(f'cluster_sub_{current_sub_adm_num}')
                    sub_subgraph.set_label(f'Sub-ADM {current_sub_adm_num}')
                    sub_subgraph.set('style', 'filled')
                    sub_subgraph.set('fillcolor', 'lightyellow')
                    sub_subgraph.set('color', 'black')
                    sub_subgraph.set('fontname', 'Arial')
                    sub_subgraph.set('fontsize', '14')
                    sub_subgraph.set('penwidth', '2')
                    
                    # Process sub-ADM nodes
                    for sub_node in sub_graph.get_node_list():
                        sub_node.set_label('')
                        sub_node.set_width('0.3')
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
                            sub_node.set_penwidth('1.5')
                        
                        sub_subgraph.add_node(sub_node)
                    
                    # Process sub-ADM edges
                    for sub_edge in sub_graph.get_edge_list():
                        sub_edge.set_penwidth('1.0')
                        sub_edge.set_color('black')
                        sub_edge.set_arrowsize('1.0')
                        sub_subgraph.add_edge(sub_edge)
                    
                    combined_graph.add_subgraph(sub_subgraph)
                    
                except Exception as e:
                    print(f"Error creating sub-ADM {current_sub_adm_num}: {e}")
    
    # Add enhanced connection edges
    for node_name, sub_model_num in node_to_sub_model.items():
        connection_edge = pydot.Edge(
            node_name,
            f"cluster_sub_{sub_model_num}",
            style='dashed',
            color='red',
            penwidth='2.0',
            arrowhead='open',
            arrowsize='1.5'
        )
        combined_graph.add_edge(connection_edge)
    
    # Add a legend
    add_legend(combined_graph)
    
    return combined_graph

def add_legend(graph):
    """
    Add a legend to the graph
    """
    # Create legend subgraph
    legend = pydot.Subgraph('cluster_legend')
    legend.set_label('Legend')
    legend.set('style', 'filled')
    legend.set('fillcolor', 'white')
    legend.set('color', 'black')
    legend.set('fontname', 'Arial')
    legend.set('fontsize', '12')
    legend.set('penwidth', '1')
    
    # Legend items
    legend_items = [
        ('red', 'Root/Decision Node'),
        ('blue', 'Abstract Factor'),
        ('green', 'Base Level Factor'),
        ('orange', 'Sub-ADM BLF'),
        ('purple', 'Evaluation BLF'),
        ('gray', 'Other Node')
    ]
    
    for i, (color, label) in enumerate(legend_items):
        legend_node = pydot.Node(f'legend_{i}', 
                                label=label,
                                shape='box',
                                style='filled',
                                fillcolor=color,
                                color='black',
                                width='0.3',
                                height='0.2',
                                fontname='Arial',
                                fontsize='10')
        legend.add_node(legend_node)
    
    graph.add_subgraph(legend)

def main():
    """
    Generate the enhanced Inventive Step visualization
    """
    print("=" * 60)
    print("ENHANCED INVENTIVE STEP ADM VISUALIZATION")
    print("=" * 60)
    
    # Create the enhanced visualization
    graph = create_enhanced_inventive_step_visualization()
    
    # Save as high-quality PNG
    png_filename = "Inventive_Step_Enhanced.png"
    graph.write_png(png_filename)
    print(f"✓ Saved PNG: {png_filename}")
    
    # Save as SVG for vector graphics
    svg_filename = "Inventive_Step_Enhanced.svg"
    graph.write_svg(svg_filename)
    print(f"✓ Saved SVG: {svg_filename}")
    
    # Save as PDF for publication
    pdf_filename = "Inventive_Step_Enhanced.pdf"
    graph.write_pdf(pdf_filename)
    print(f"✓ Saved PDF: {pdf_filename}")
    
    print("\n" + "=" * 60)
    print("✅ Enhanced visualization generated successfully!")
    print("\nPublication recommendations:")
    print("• Use SVG for best scalability and quality")
    print("• Use PDF for direct inclusion in documents")
    print("• PNG is suitable for web or low-resolution needs")
    print("\nThe visualization includes:")
    print("• Clean minimal design with color-coded node types")
    print("• Proper spacing and layout for readability")
    print("• Sub-ADMs clearly separated and connected")
    print("• Legend for easy interpretation")
    print("• High DPI for publication quality")

if __name__ == "__main__":
    main()
