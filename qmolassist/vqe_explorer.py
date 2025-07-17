# backend/vqe_explorer.py
"""
Module to parse VQE convergence results and provide analysis and suggestions.
"""
from typing import Dict

import pandas as pd


def parse_vqe_results(csv_path: str) -> pd.DataFrame:
    """
    Reads a CSV file containing VQE iteration results.

    The CSV must have columns:
    - 'iteration': iteration number
    - 'energy': computed energy at each iteration

    Parameters:
        csv_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame with the convergence data.
    """
    df = pd.read_csv(csv_path)
    return df


def analyze_convergence(df: pd.DataFrame, threshold: float = 1e-3) -> Dict[str, float]:
    """
    Analyzes convergence data from a VQE run and returns key metrics.

    Parameters:
        df (pd.DataFrame): DataFrame from parse_vqe_results.
        threshold (float): Energy change threshold for convergence.

    Returns:
        Dict[str, float]: Dictionary with:
            - 'final_energy': last energy value
            - 'energy_delta': difference between last two iterations
            - 'converged': whether |energy_delta| < threshold
    """
    final_energy = df["energy"].iloc[-1]
    if len(df) >= 2:
        energy_delta = df["energy"].iloc[-2] - final_energy
    else:
        energy_delta = float("nan")
    converged = abs(energy_delta) < threshold if not pd.isna(energy_delta) else False
    return {
        "final_energy": final_energy,
        "energy_delta": energy_delta,
        "converged": converged,
    }
