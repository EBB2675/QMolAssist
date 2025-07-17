# QMolAssist

**Your LLM-Powered Quantum Chemistry Copilot**

---

## 🚀 Core Functionalities

1. **QPrompt**: *Natural Language → Quantum Circuit*

   * Describe your molecule in plain English or SMILES.
   * Instantly generate a VQE‑ready circuit (UCCSD ansatz) via Qiskit Nature & OpenFermion.
   * Returns circuit object, qubit count, and Hamiltonian details.

2. **Molecule Selector**: *Resource‑Aware Candidate Picker*

   * Estimate qubit requirements (spin orbitals) for any molecule.
   * Filter candidate lists under a user‑defined qubit budget.
   * Ideal for NISQ hardware feasibility checks.

3. **VQExplorer**: *VQE Convergence Analyst*

   * Parse iteration vs. energy CSV logs.
   * Compute final energy, energy delta, and convergence flag.
   * Generate actionable insights on optimizer settings and ansatz depth.

4. **PySCF Comparator**: *Classical Benchmarking*

   * Compute RHF and FCI reference energies using PySCF.
   * Compare classical and quantum (VQE) energies to quantify NISQ performance.
   * Helps you decide when quantum advantage is within reach.

5. **LLM Copilot**: *Natural‑Language Guide*

   * Wraps OpenAI’s ChatCompletion for context‑aware explanations.
   * Suggests ansatz choices, qubit mappings, and optimizer settings.
   * Interprets molecule selection rationale, VQE convergence reports, and energy comparisons.

---

## 🧰 Technology Stack

* **Language & Environment**: Python 3.10, Conda
* **Quantum Chemistry & Computing**:

  * [Qiskit](https://qiskit.org) & [Qiskit Nature](https://qiskit.org/nature)
  * [OpenFermion](https://github.com/quantumlib/OpenFermion)
  * [PySCF](https://pyscf.org) for RHF & FCI
  * RDKit for SMILES→geometry (future)
* **Machine Learning & LLM**:

  * [OpenAI API](https://openai.com/docs/api)
  * Custom prompt templates for domain‑specific reasoning
* **Data & Analysis**:

  * pandas, matplotlib for results processing & plotting
* **Testing & QA**:

  * pytest with fixtures for all modules
* **UI (Future)**:

  * Streamlit / Gradio for interactive demos (stub in `frontend/app.py`)

---

## ⚙️ Installation & Setup

```bash
# 1. Clone the repo
git clone https://github.com/your-org/quantum-llm-assistant.git
cd quantum-llm-assistant

# 2. Create Conda environment
conda create -n qlla python=3.10 -y
conda activate qlla

# 3. Install dependencies
conda install -c conda-forge pyscf rdkit pandas matplotlib -y
pip install qiskit qiskit-nature openfermion openai streamlit pytest

# 4. (Optional) Export environment
conda env export > environment.yml
pip freeze > requirements.txt
```

---

## ▶️ Quickstart Examples

1. **Circuit Generation**

   ```bash
   python examples/example_selector.py
   ```

2. **Classical Benchmark**

   ```bash
   python examples/example_comparator.py
   ```

3. **VQE Convergence Analysis**

   ```bash
   # TODO: add example script for vqe_explorer
   ```

4. **LLM Explanations**

   ```bash
   # TODO: add example scripts under examples/
   ```

---

## ✅ Testing

Run the full test suite:

```bash
pytest --maxfail=1 --disable-warnings -q
```



