from config import small_pim, no_protection, spm_only, minimal, balanced, strong
from experiments import run_experiment
from plots.plot_results import plot_breakdown, plot_sdc_only, plot_cost_vs_reliability

pim = small_pim()

policies = {
    "None": no_protection(),
    "Minimal": minimal(),
    "SPM Only": spm_only(),
    "Balanced": balanced(),
    "Strong": strong()
}

exp = run_experiment(pim, policies, baseline_name="None", trials=1_000_000, runs=50)

analytical = exp["analytical"]
simulation = exp["simulation"]

print("=== ANALYTICAL RESULTS ===")
for name in policies.keys():
    metrics = analytical[name]["metrics"]
    cost = analytical[name]["cost"]

    print(f"\n{name}:")
    print(f"  SDC (analytic): {metrics['sdc']}")
    print(f"  DUE (analytic): {metrics['due']}")
    print(f"  Corrected (analytic): {metrics['corrected']}")
    print(f"  Area: {cost['area']}")
    print(f"  Latency: {cost['latency']}")

print("\n=== SIMULATION RESULTS ===")
for name in policies.keys():
    sim = simulation[name]["sim"]
    cost = simulation[name]["cost"]

    print(f"\n{name}:")
    print(f"  SDC rate: {sim['sdc_rate']}")
    print(f"  DUE rate: {sim['due_rate']}")
    print(f"  Corrected rate: {sim['corrected_rate']}")
    print(f"  Normalized Area: {cost['normalized_area']}")


# plotting uses simulation results
plot_breakdown(exp["simulation"])
plot_sdc_only(exp["simulation"])
plot_cost_vs_reliability(exp["simulation"])