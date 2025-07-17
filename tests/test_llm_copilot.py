# tests/test_llm_copilot.py
import pandas as pd
import pytest

import backend.llm_copilot as lc

class DummyResponse:
    def __init__(self, text):
        self.choices = [type('Choice', (), {'message': type('Msg', (), {'content': text})})]

@pytest.fixture(autouse=True)
def dummy_call_llm(monkeypatch):
    # Patch call_llm to capture the prompt and return a fixed response
    def fake_call_llm(prompt, model='gpt-4o-mini', temperature=0.7):
        # Attach prompt to module for inspection if needed
        lc._last_prompt = prompt
        return "DUMMY_RESPONSE"
    monkeypatch.setattr(lc, 'call_llm', fake_call_llm)
    return fake_call_llm


def test_explain_simulation_protocol_includes_parameters():
    result = lc.explain_simulation_protocol('H2', 'sto3g', 4)
    assert result == "DUMMY_RESPONSE"
    assert 'H2' in lc._last_prompt
    assert 'sto3g' in lc._last_prompt
    assert '4 qubits' in lc._last_prompt
    assert 'ansatz' in lc._last_prompt.lower()


def test_suggest_molecule_selection_rationale_format():
    suggestions = {'H2': 4, 'LiH': 8}
    result = lc.suggest_molecule_selection_rationale(suggestions, 10)
    assert result == "DUMMY_RESPONSE"
    assert 'qubit limit of 10' in lc._last_prompt
    assert 'H2 (4 qubits)' in lc._last_prompt
    assert 'LiH (8 qubits)' in lc._last_prompt


def test_analyze_vqe_run_prompts_with_energy_and_delta():
    df = pd.DataFrame({'iteration': [0, 1], 'energy': [-1.0, -1.05]})
    result = lc.analyze_vqe_run(df)
    assert result == "DUMMY_RESPONSE"
    prompt = lc._last_prompt
    assert 'final energy of -1.050000 Ha' in prompt
    assert 'energy change of 0.050000 Ha' in prompt
    

def test_interpret_classical_comparison_includes_all_methods():
    results = {'RHF': -1.1, 'FCI': -1.15, 'VQE': -1.13}
    result = lc.interpret_classical_comparison(results)
    assert result == "DUMMY_RESPONSE"
    prompt = lc._last_prompt
    # Check that keys and values are represented
    assert 'RHF: -1.100000' in prompt
    assert 'FCI: -1.150000' in prompt
    assert 'VQE: -1.130000' in prompt
    assert 'differences' in prompt
