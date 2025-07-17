import os
import sys

# ensure project root is on path
topdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, topdir)

from backend.llm_copilot import explain_simulation_protocol

# Verify API key
if not os.getenv('OPENAI_API_KEY'):
    raise RuntimeError('Please set the OPENAI_API_KEY environment variable')

# Example run
result = explain_simulation_protocol("H 0 0 0; H 0 0 0.74", "sto3g", 4)
print("LLM response:\n", result)