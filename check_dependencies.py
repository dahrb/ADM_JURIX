#!/usr/bin/env python3
from inventive_step_ADM import adf

adm_instance = adf()
print("Looking for DependentBLF nodes...")
for name, node in adm_instance.nodes.items():
    if hasattr(node, 'dependency_node'):
        print(f"  {name}: dependency={node.dependency_node}")

print("\nQuestion order:")
print(adm_instance.questionOrder)

print("\nTesting dependency evaluation...")
adm_instance.case = ['SimilarEffect', 'SameField', 'Average', 'Individual']

print(f"Current case: {adm_instance.case}")

# Test each DependentBLF
for name, node in adm_instance.nodes.items():
    if hasattr(node, 'dependency_node'):
        dependency_met = node.checkDependency(adm_instance, adm_instance.case)
        print(f"  {name}: dependency {node.dependency_node} met = {dependency_met}")
