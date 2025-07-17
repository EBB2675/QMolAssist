# examples/example_comparator.py
"""
Example script for PySCF Comparator: computes and prints RHF vs. FCI energies.
"""
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from qmolassist.pyscf_comparator import compare_energies

# Example molecule: H2
molecule = "H 0 0 0; H 0 0 0.74"
basis = "sto3g"

results = compare_energies(molecule, basis=basis)

print("Classical Energy Comparison for H2 (basis=sto3g):")
for method, energy in results.items():
    print(f" - {method}: {energy:.6f} Ha")
