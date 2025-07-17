# tests/test_vqe_explorer.py

import pandas as pd
import os
import tempfile

from backend.vqe_explorer import parse_vqe_results, analyze_convergence


def test_parse_vqe_results(tmp_path):
    # Create a temporary CSV file with iteration and energy columns
    data = """
iteration,energy
0,-1.0
1,-1.1
2,-1.15
"""
    file_path = tmp_path / "vqe.csv"
    file_path.write_text(data)

    df = parse_vqe_results(str(file_path))
    # Check that DataFrame has correct shape and columns
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["iteration", "energy"]
    assert len(df) == 3
    assert df.iloc[1]["energy"] == -1.1


def test_analyze_convergence_converged():
    # Data with small delta should be marked converged
    df = pd.DataFrame({
        'iteration': [0, 1, 2],
        'energy': [-1.0, -1.0005, -1.0009]
    })
    result = analyze_convergence(df, threshold=1e-3)
    assert result['final_energy'] == -1.0009
    assert abs(result['energy_delta'] - ( -1.0005 - -1.0009 )) < 1e-8
    assert bool(result['converged']) is True


def test_analyze_convergence_not_converged():
    # Data with large delta is not converged
    df = pd.DataFrame({
        'iteration': [0, 1],
        'energy': [-1.0, -1.1]
    })
    result = analyze_convergence(df, threshold=1e-3)
    assert result['final_energy'] == -1.1
    assert result['energy_delta'] == -1.0 - -1.1
    assert bool(result['converged']) is False


def test_analyze_convergence_single_point():
    # Single-row DataFrame yields nan delta and not converged
    df = pd.DataFrame({'iteration': [0], 'energy': [-1.0]})
    result = analyze_convergence(df, threshold=1e-3)
    assert result['final_energy'] == -1.0
    assert pd.isna(result['energy_delta'])
    assert result['converged'] is False
