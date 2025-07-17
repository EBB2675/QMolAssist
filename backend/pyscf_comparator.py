# backend/pyscf_comparator.py
"""
Module to compute classical reference energies using PySCF and compare to quantum results.
"""
from typing import Dict
from pyscf import gto, scf, fci


def compute_rhf_energy(molecule: str, basis: str = "sto3g") -> float:
    """
    Compute the restricted Hartree-Fock energy for a molecule.

    Parameters:
        molecule (str): Atom string (e.g., "H 0 0 0; H 0 0 0.74").
        basis (str): Basis set (default: 'sto3g').

    Returns:
        float: RHF total energy in Hartree.
    """
    mol = gto.M(atom=molecule, basis=basis, unit="Angstrom")
    mf = scf.RHF(mol)
    energy = mf.kernel()
    return energy


def compute_fci_energy(molecule: str, basis: str = "sto3g") -> float:
    """
    Compute the full configuration interaction (FCI) energy for a molecule.

    Parameters:
        molecule (str): Atom string (e.g., "H 0 0 0; H 0 0 0.74").
        basis (str): Basis set (default: 'sto3g').

    Returns:
        float: FCI total energy in Hartree.
    """
    mol = gto.M(atom=molecule, basis=basis, unit="Angstrom")
    mf = scf.RHF(mol).run()
    cisolver = fci.FCI(mol, mf.mo_coeff)
    energy, _ = cisolver.kernel()
    return energy


def compare_energies(molecule: str, basis: str = "sto3g") -> Dict[str, float]:
    """
    Compare RHF and FCI energies for a molecule.

    Returns:
        Dict[str, float]: Dictionary with keys 'RHF' and 'FCI'.
    """
    rhf_e = compute_rhf_energy(molecule, basis)
    fci_e = compute_fci_energy(molecule, basis)
    return {"RHF": rhf_e, "FCI": fci_e}
