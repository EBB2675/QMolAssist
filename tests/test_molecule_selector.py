# tests/test_molecule_selector.py

from qmolassist.molecule_selector import estimate_qubits, suggest_molecules


def test_estimate_qubits_h2():
    # H2 in STO-3G should require 4 qubits (2 spatial orbitals × 2 spins)
    geom = "H 0 0 0; H 0 0 0.74"
    qubits = estimate_qubits(geom, basis="sto3g")
    assert qubits == 4


def test_estimate_qubits_lih():
    # LiH in STO-3G yields 6 spatial orbitals × 2 spins = 12 qubits
    geom = "Li 0 0 0; H 0 0 1.6"
    qubits = estimate_qubits(geom, basis="sto3g")
    assert qubits == 12


def test_suggest_molecules():
    candidates = {
        "H2": "H 0 0 0; H 0 0 0.74",
        "LiH": "Li 0 0 0; H 0 0 1.6",
        "H2O": "O 0 0 0; H 0 0 0.96; H 0 0.76 -0.24",
    }
    suggestions = suggest_molecules(candidates, qubit_limit=6, basis="sto3g")
    # Only H2 fits under 6 qubits
    assert suggestions == {"H2": 4}
