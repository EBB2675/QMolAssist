# examples/example_selector.py
"""
Example usage of the Molecule Selector module.
Runs suggest_molecules on a predefined set of candidates and prints the results.
"""
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from qmolassist.molecule_selector import suggest_molecules

# Define a candidate list of molecules (name: geometry)
candidates = {
    "H2": "H 0 0 0; H 0 0 0.74",
    "LiH": "Li 0 0 0; H 0 0 1.6",
    "H2O": "O 0 0 0; H 0 0 0.96; H 0 0.76 -0.24",
    "NH3": "N 0 0 0; H 0 0.94 0.0; H 0.82 -0.47 0.0; H -0.82 -0.47 0.0",
    "CH4": "C 0 0 0; H 0 0 1.09; H 1.02 0 0; H -0.51 0.88 0; H -0.51 -0.88 0",
}

# Set qubit limit and basis
qubit_limit = 10
basis = "sto3g"

# Get suggestions
suggestions = suggest_molecules(candidates, qubit_limit=qubit_limit, basis=basis)

# Print results
print(f"Molecules fitting under {qubit_limit} qubits (basis={basis}):")
for name, qubits in suggestions.items():
    print(f" - {name}: {qubits} qubits")
