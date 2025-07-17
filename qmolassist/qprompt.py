# backend/qprompt.py
"""
Module to build VQE circuits from either SMILES or direct geometry strings.
"""
import numpy as np

# RDKit imports
from rdkit import Chem
from rdkit.Chem import AllChem

# Qiskit primitives and algorithms
from qiskit.primitives import Estimator
from qiskit_algorithms.minimum_eigensolvers import VQE
from qiskit_algorithms.optimizers import COBYLA

# Qiskit Nature for quantum chemistry problem setup
try:
    from qiskit_nature.second_q.drivers import PySCFDriver
    from qiskit_nature.units import DistanceUnit
    from qiskit_nature.second_q.mappers import JordanWignerMapper
    from qiskit_nature.second_q.circuit.library.ansatzes.uccsd import UCCSD
except ImportError:
    from qiskit_nature.drivers.second_quantization import PySCFDriver
    from qiskit_nature.units import DistanceUnit
    from qiskit_nature.mappers.second_quantization import JordanWignerMapper
    from qiskit_nature.circuit.library.second_quantization.ansatzes.uccsd import UCCSD

# Convert SMILES to XYZ

def smiles_to_xyz(smiles: str, random_seed: int = 42) -> str:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Invalid SMILES: {smiles}")
    mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol, randomSeed=random_seed)
    AllChem.UFFOptimizeMolecule(mol)
    conf = mol.GetConformer()
    coords = []
    for atom in mol.GetAtoms():
        pos = conf.GetAtomPosition(atom.GetIdx())
        coords.append(f"{atom.GetSymbol()} {pos.x:.6f} {pos.y:.6f} {pos.z:.6f}")
    return "; ".join(coords)

# Build VQE circuit

def build_vqe_circuit(molecule: str, basis: str = "sto3g"):
    geometry = molecule
    if Chem.MolFromSmiles(molecule):
        geometry = smiles_to_xyz(molecule)

    driver = PySCFDriver(atom=geometry, unit=DistanceUnit.ANGSTROM, basis=basis)
    es_problem = driver.run()

    mapper = JordanWignerMapper()
    second_q_op = es_problem.second_q_ops()[0]
    qubit_op = mapper.map(second_q_op)

    ansatz = UCCSD(
        qubit_mapper=mapper,
        num_spatial_orbitals=es_problem.num_spatial_orbitals,
        num_particles=es_problem.num_particles,
    )

    optimizer = COBYLA(maxiter=1)
    estimator = Estimator()
    vqe = VQE(ansatz=ansatz, optimizer=optimizer, estimator=estimator)
    _ = vqe.compute_minimum_eigenvalue(qubit_op)

    return ansatz, qubit_op.num_qubits, {
        "hamiltonian": qubit_op,
        "num_spatial_orbitals": es_problem.num_spatial_orbitals,
        "num_particles": es_problem.num_particles,
        "geometry": geometry,
    }