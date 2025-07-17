import click

from qmolassist.qprompt import build_plan


@click.command()
@click.argument("smiles")
@click.option("--budget", type=int, default=16, help="Max qubits")
@click.option("--accuracy", type=float, default=1e-3, help="Target energy error (Ha)")
def run(smiles: str, budget: int, accuracy: float):
    plan = build_plan(smiles, budget, accuracy)
    print(plan)


if __name__ == "__main__":
    run()
