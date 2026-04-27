from analysis.metrics import compute_system_metrics
from analysis.cost_model import compute_cost
from analysis.simulation import simulate_system, normalize_results
from analysis.simulation import inject_fixed_system


def run_experiment(pim, policies, baseline_name, trials=100000, runs=50):
    """
    policies: dict[name -> policy]
    baseline_name: key in policies dict
    """

    num_components = len(pim.components())
    results = {}

    baseline_policy = policies[baseline_name]
    baseline_cost = compute_cost(pim, baseline_policy)
    baseline_area = baseline_cost["area"]

    # --- ANALYTICAL ---
    analytical = {}

    for name, policy in policies.items():
        metrics = compute_system_metrics(pim, policy)
        cost = compute_cost(pim, policy)

        analytical[name] = {
            "metrics": {
                "corrected": metrics["corrected"] / num_components,
                "due": metrics["due"] / num_components,
                "sdc": metrics["sdc"] / num_components
            },
            "cost": cost
        }

    # --- MONTE CARLO ---
    for name, policy in policies.items():
        agg = {"corrected": 0, "due": 0, "sdc": 0}

        for _ in range(runs):
            sim_results = simulate_system(pim, policy, trials)
            for k in agg:
                agg[k] += sim_results[k]

        norm = normalize_results(agg, trials * runs, num_components)

        results[name] = {
            "sim": norm,
            "cost": compute_cost(pim, policy)
        }

        results[name]["cost"]["normalized_area"] = (
            results[name]["cost"]["area"] / baseline_area
        )

    return {
        "analytical": analytical,
        "simulation": results
    }