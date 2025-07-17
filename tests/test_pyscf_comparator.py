# tests/test_pyscf_comparator.py

import pytest
from backend.pyscf_comparator import compute_rhf_energy, compute_fci_energy, compare_energies


def test_rhf_energy_h2():
    energy = compute_rhf_energy("H 0 0 0; H 0 0 0.74", basis="sto3g")
    assert isinstance(energy, float)
    assert energy < 0


def test_fci_energy_h2():
    rhf = compute_rhf_energy("H 0 0 0; H 0 0 0.74", basis="sto3g")
    fci_e = compute_fci_energy("H 0 0 0; H 0 0 0.74", basis="sto3g")
    assert isinstance(fci_e, float)
    assert fci_e <= rhf


def test_compare_energies_keys_and_values():
    results = compare_energies("H 0 0 0; H 0 0 0.74", basis="sto3g")
    assert set(results.keys()) == {"RHF", "FCI"}
    assert results["FCI"] <= results["RHF"]
