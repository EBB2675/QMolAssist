# backend/molecule_selector.py
"""
Module to estimate qubit requirements for a given molecule and suggest runnable molecules under qubit constraints.
"""
from typing import Dict

from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.units import DistanceUnit


def estimate_qubits(molecule: str, basis: str = "sto3g") -> int:
    """
    Estimate the number of qubits required for a VQE simulation of the given molecule.

    Parameters:
        molecule (str): Atom string (e.g., "H 0 0 0; H 0 0 0.74").
        basis (str): Basis set (default: 'sto3g').

    Returns:
        int: Number of spin orbitals (equal to qubit count).
    """
    # init driver to build electronic structure problem
    driver = PySCFDriver(atom=molecule, unit=DistanceUnit.ANGSTROM, basis=basis)
    es_problem = driver.run()
    # number of spin orbitals corresponds to required qubits
    return es_problem.num_spin_orbitals


def suggest_molecules(
    candidates: Dict[str, str], qubit_limit: int, basis: str = "sto3g"
) -> Dict[str, int]:
    """
    Suggest molecules from a candidate list that fit within a qubit limit.

    Parameters:
        candidates (Dict[str, str]): Mapping from molecule name to atom string.
        qubit_limit (int): Maximum allowable qubit count.
        basis (str): Basis set to use for estimation.

    Returns:
        Dict[str, int]: Subset of candidates with their qubit counts <= qubit_limit.
    """
    suggestions: Dict[str, int] = {}
    for name, geom in candidates.items():
        qubits = estimate_qubits(geom, basis)
        if qubits <= qubit_limit:
            suggestions[name] = qubits
    return suggestions
