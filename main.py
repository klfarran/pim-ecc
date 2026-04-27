from config import small_pim, no_protection, spm_only, minimal, balanced, strong
from analysis.metrics import compute_system_metrics
from analysis.cost_model import compute_cost
from analysis.simulation import simulate_system, normalize_results, inject_fixed_system
from plots.plot_results import plot_breakdown, plot_sdc_only, plot_cost_vs_reliability

pim = small_pim()

policies = {
    "None": no_protection(),
    "Minimal": minimal(),
    "SPM Only": spm_only(),
    "Balanced": balanced(),
    "Strong": strong()
}

# baseline (no protection) for normalization
baseline_area = compute_cost(pim, policies["None"])["area"]

print("=== ANALYTICAL RESULTS ===")

for name, policy in policies.items():
    metrics = compute_system_metrics(pim, policy)
    cost = compute_cost(pim, policy)
    num_components = len(pim.components())

    # normalize analytical metrics to per-component rate
    metrics_norm = {
        "corrected": metrics["corrected"] / num_components,
        "due": metrics["due"] / num_components,
        "sdc": metrics["sdc"] / num_components
    }

    print(f"{name}:")
    print(f"  SDC (analytic): {metrics_norm['sdc']}")
    print(f"  DUE (analytic): {metrics_norm['due']}")
    print(f"  Corrected (analytic): {metrics_norm['corrected']}")
    print(f"  Area: {cost['area']}")
    print(f"  Latency: {cost['latency']}")
    
    
print("\n=== MONTE CARLO SIMULATION ===")

TRIALS = 1000000
RUNS = 50

results = {}

for name, policy in policies.items():
    agg = {"corrected": 0, "due": 0, "sdc": 0}
    
    for _ in range(RUNS):
        sim_results = simulate_system(pim, policy, TRIALS)
        for k in agg:
            agg[k] += sim_results[k]
            
    norm = normalize_results(agg, TRIALS * RUNS, len(pim.components())) 

    results[name] = {
        "sim": norm,
        "cost": compute_cost(pim, policy)
    }
    
    # calculate normalized area (relative to baseline)
    results[name]["cost"]["normalized_area"] = results[name]["cost"]["area"] / baseline_area
    
    print(f"{name} (Simulation):")
    print(f"  SDC rate: {norm['sdc_rate']}")
    print(f"  DUE rate: {norm['due_rate']}")
    print(f"  Corrected rate: {norm['corrected_rate']}")
    
    
print("\n=== FIXED ERROR INJECTION RESULTS ===")

FIXED_ERRORS = 1000000  # per component

for name, policy in policies.items():
    fixed_results = inject_fixed_system(pim, policy, FIXED_ERRORS)

    total_errors = FIXED_ERRORS * len(pim.components())

    corrected_rate = fixed_results["corrected"] / total_errors
    due_rate = fixed_results["due"] / total_errors
    sdc_rate = fixed_results["sdc"] / total_errors

    print(f"{name} (Fixed Injection):")
    print(f"  SDC rate: {sdc_rate}")
    print(f"  DUE rate: {due_rate}")
    print(f"  Corrected rate: {corrected_rate}")
    
    
# testing plotting: 
plot_breakdown(results)
plot_sdc_only(results)
plot_cost_vs_reliability(results)