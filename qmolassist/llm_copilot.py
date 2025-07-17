# backend/llm_copilot.py
"""
LLM Copilot module: wrap OpenAI calls and generate natural-language explanations and suggestions
"""
import os
import openai
from typing import Dict, Any

openai.api_key = os.getenv('OPENAI_API_KEY')


def call_llm(prompt: str, model: str = 'gpt-4o-mini', temperature: float = 0.7) -> str:
    """
    Send a prompt to the LLM and return the response text using OpenAI v1 client interface.

    Parameters:
        prompt (str): The prompt text to send.
        model (str): Model name.
        temperature (float): Sampling temperature.

    Returns:
        str: The LLM's response.
    """
    response = openai.chat.completions.create(
        model=model,
        messages=[{'role': 'user', 'content': prompt}],
        temperature=temperature
    )
    return response.choices[0].message.content.strip()


def explain_simulation_protocol(molecule: str, basis: str, qubit_count: int) -> str:
    """
    Generate an NL explanation of the simulation protocol.

    Parameters:
        molecule (str): Molecule cartesian coords or SMILES.
        basis (str): Basis set used.
        qubit_count (int): Number of qubits estimated.

    Returns:
        str: Explanation of choices (ansatz, encoding, optimizer).
    """
    prompt = (
        f"I want to run a VQE simulation on the molecule '{molecule}' with the {basis} basis set, "
        f"which requires {qubit_count} qubits. "
        "Suggest an appropriate ansatz, qubit mapping, optimizer, and any resource considerations. "
        "Explain why each choice is appropriate for NISQ hardware."
    )
    return call_llm(prompt)


def suggest_molecule_selection_rationale(suggestions: Dict[str, int], qubit_limit: int) -> str:
    """
    Explain why certain molecules fit under a given qubit limit.

    Parameters:
        suggestions (Dict[str, int]): Mapping from molecule names to qubit counts.
        qubit_limit (int): Qubit budget.

    Returns:
        str: Explanation of selection rationale.
    """
    entries = ', '.join([f"{name} ({count} qubits)" for name, count in suggestions.items()])
    prompt = (
        f"Given a qubit limit of {qubit_limit}, the following molecules fit: {entries}. "
        "Explain why these molecules are appropriate for NISQ experiments, and what trade-offs "
        "in size or complexity influenced this selection."
    )
    return call_llm(prompt)


def analyze_vqe_run(df: Any) -> str:
    """
    Provide natural-language suggestions based on VQE convergence data.

    Parameters:
        df (pd.DataFrame): DataFrame with 'iteration' and 'energy'.

    Returns:
        str: Suggestions to improve convergence.
    """
    last = df['energy'].iloc[-1]
    delta = df['energy'].iloc[-2] - last if len(df) >= 2 else None
    prompt = (
        f"A VQE run produced a final energy of {last:.6f} Ha with an energy change of {delta:.6f} Ha "
        "on the last iteration. "
        "Recommend how to improve convergence: consider ansatz depth, optimizer settings, or hardware adjustments."
    )
    return call_llm(prompt)


def interpret_classical_comparison(results: Dict[str, float]) -> str:
    """
    Interpret the comparison between classical (RHF/FCI) and quantum (VQE) energies.

    Parameters:
        results (Dict[str, float]): Dictionary with 'RHF', 'FCI', and optionally 'VQE'.

    Returns:
        str: Natural-language interpretation of the energy differences and recommendations.
    """
    entries = ', '.join([f"{k}: {v:.6f}" for k, v in results.items()])
    prompt = (
        f"Here are the computed energies: {entries} Ha. "
        "Explain the significance of the differences, and whether the quantum result "
        "is within an acceptable error margin. Suggest next steps."
    )
    return call_llm(prompt)
