#!/usr/bin/env python3
"""
Split ADM Visualization Script
Creates separate images for main ADM and each sub-ADM
"""

import sys
import os
from MainClasses import *
import academic_research_ADM
import inventive_step_ADM

def create_split_visualizations(adf, adf_name):
    """
    Create separate visualizations for main ADM and each sub-ADM
    
    Parameters:
    -----------
    adf : ADF
        The ADM instance to visualize
    adf_name : str
        Name for the ADM (used in filenames)
    """
    print(f"\n📊 Creating split visualizations for {adf_name}")
    print("-" * 50)
    
    # 1. Create main ADM visualization
    print("Creating main ADM visualization...")
    main_graph = adf.visualiseNetwork()
    
    # Save main ADM
    main_png = f"{adf_name}_main.png"
    main_svg = f"{adf_name}_main.svg"
    main_graph.write_png(main_png)
    main_graph.write_svg(main_svg)
    print(f"✓ Saved main ADM: {main_png}, {main_svg}")
    
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
                    
                    # Create sub-ADM graph
                    sub_graph = sub_adf.visualiseNetwork()
                    
                    # Save sub-ADM
                    sub_png = f"{adf_name}_sub_adm_{sub_adm_count}.png"
                    sub_svg = f"{adf_name}_sub_adm_{sub_adm_count}.svg"
                    sub_graph.write_png(sub_png)
                    sub_graph.write_svg(sub_svg)
                    print(f"✓ Saved Sub-ADM {sub_adm_count}: {sub_png}, {sub_svg}")
                    
                except Exception as e:
                    print(f"❌ Error creating Sub-ADM {sub_adm_count}: {e}")
    
    return sub_adm_count

def create_inventive_step_split():
    """
    Create split visualizations for Inventive Step ADM
    """
    print("=" * 60)
    print("INVENTIVE STEP ADM - SPLIT VISUALIZATIONS")
    print("=" * 60)
    
    # Load the ADM
    adf = inventive_step_ADM.adf()
    
    # Create split visualizations
    sub_adm_count = create_split_visualizations(adf, "inventive_step")
    
    print(f"\n✅ Generated {1 + sub_adm_count} separate visualizations:")
    print(f"  • 1 main ADM image")
    print(f"  • {sub_adm_count} sub-ADM images")
    
    return sub_adm_count

def create_academic_research_split():
    """
    Create split visualizations for Academic Research ADM
    """
    print("=" * 60)
    print("ACADEMIC RESEARCH ADM - SPLIT VISUALIZATIONS")
    print("=" * 60)
    
    # Load the ADM
    adf = academic_research_ADM.adf()
    
    # Create split visualizations
    sub_adm_count = create_split_visualizations(adf, "academic_research")
    
    print(f"\n✅ Generated {1 + sub_adm_count} separate visualizations:")
    print(f"  • 1 main ADM image")
    print(f"  • {sub_adm_count} sub-ADM images")
    
    return sub_adm_count

def main():
    """
    Generate split visualizations for all ADMs
    """
    print("Creating split ADM visualizations...")
    print("Each ADM and sub-ADM will be saved as separate images")
    
    total_images = 0
    
    # Inventive Step ADM
    try:
        inventive_count = create_inventive_step_split()
        total_images += 1 + inventive_count
    except Exception as e:
        print(f"Error with Inventive Step ADM: {e}")
    
    # Academic Research ADM
    try:
        academic_count = create_academic_research_split()
        total_images += 1 + academic_count
    except Exception as e:
        print(f"Error with Academic Research ADM: {e}")
    
    print("\n" + "=" * 60)
    print(f"✅ ALL SPLIT VISUALIZATIONS COMPLETED!")
    print(f"Total images generated: {total_images}")
    print("\nEach image is saved in both PNG and SVG formats:")
    print("• PNG: High-resolution raster images")
    print("• SVG: Vector graphics for scaling")
    print("\nYou can now use these individual images as needed!")

if __name__ == "__main__":
    main()
