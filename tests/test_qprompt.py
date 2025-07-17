from qmolassist.qprompt import build_vqe_circuit


def test_h2_vqe_circuit_build():
    circuit, num_qubits, info = build_vqe_circuit("H 0 0 0; H 0 0 0.74")

    assert circuit is not None
    assert num_qubits == 4  # H₂ in STO-3G → 2 orbitals × 2 spin = 4 qubits
    assert "hamiltonian" in info
    assert info["num_particles"] == (1, 1)  # spin-up and spin-down electrons
