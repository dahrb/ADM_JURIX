#!/usr/bin/env python3

# Test script to test sub-ADM visualization
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from MainClasses import ADF
from academic_research_ADM import adf

def test_subadm_visualization():
    """Test the sub-ADM visualization functionality"""
    
    # Create the ADM
    test_adf = adf()
    
    print(f"ADM created with {len(test_adf.nodes)} nodes")
    print("Nodes:", list(test_adf.nodes.keys()))
    
    # Check if PRIMARY_SOURCES has sub_adf_creator
    if "PRIMARY_SOURCES" in test_adf.nodes:
        primary_sources = test_adf.nodes["PRIMARY_SOURCES"]
        print(f"\nPRIMARY_SOURCES node type: {type(primary_sources)}")
        print(f"Has sub_adf_creator: {hasattr(primary_sources, 'sub_adf_creator')}")
        
        if hasattr(primary_sources, 'sub_adf_creator'):
            print("sub_adf_creator type:", type(primary_sources.sub_adf_creator))
            
            # Try to create the sub-ADM
            try:
                print("\nTrying to create sub-ADM...")
                sub_adf = primary_sources.sub_adf_creator()
                print(f"Sub-ADM created successfully: {type(sub_adf)}")
                print(f"Sub-ADM name: {sub_adf.name}")
                print(f"Sub-ADM nodes: {list(sub_adf.nodes.keys())}")
                
                # Try to visualize the sub-ADM
                print("\nTrying to visualize sub-ADM...")
                sub_graph = sub_adf.visualiseNetwork()
                print(f"Sub-ADM graph created: {type(sub_graph)}")
                
            except Exception as e:
                print(f"Error creating sub-ADM: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("PRIMARY_SOURCES does not have sub_adf_creator attribute")
    else:
        print("PRIMARY_SOURCES not found in ADM nodes")
    
    # Test the main visualization method
    print("\nTesting main visualization...")
    try:
        main_graph = test_adf.visualiseNetwork()
        print(f"Main graph created: {type(main_graph)}")
        
        # Test the sub-ADM visualization method
        print("\nTesting sub-ADM visualization...")
        combined_graph = test_adf.visualiseNetworkWithSubADMs()
        print(f"Combined graph created: {type(combined_graph)}")
        
        # Check if it's the same as main graph (meaning no sub-ADMs found)
        if combined_graph == main_graph:
            print("WARNING: Combined graph is same as main graph - no sub-ADMs were found!")
        else:
            print("SUCCESS: Combined graph includes sub-ADMs!")
            
    except Exception as e:
        print(f"Error in visualization: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_subadm_visualization()
