from config import small_pim, no_protection, balanced, strong
from protection import schemes, policy
from analysis.metrics import compute_system_metrics
from analysis.cost_model import compute_cost
from analysis.simulation import simulate_system, normalize_results, inject_fixed_system
from plots.plot_results import plot_breakdown, plot_sdc_only, plot_cost_vs_reliability

pim = small_pim()

policies = {
    "None": no_protection(),
    "Balanced": balanced(),
    "Strong": strong()
}

for name, policy in policies.items():
    metrics = compute_system_metrics(pim, policy)
    cost = compute_cost(pim, policy)

    print(f"{name}:")
    print(f"  SDC: {metrics['sdc']}")
    print(f"  DUE: {metrics['due']}")
    print(f"  Corrected: {metrics['corrected']}")
    print(f"  Area: {cost['area']}")
    print(f"  Latency: {cost['latency']}")
    
    
TRIALS = 1000000
results = {}

for name, policy in policies.items():
    #sim_results = simulate_system(pim, policy, TRIALS)
    #norm = normalize_results(sim_results, TRIALS, len(pim.components()))
    
    RUNS = 50
    agg = {"corrected": 0, "due": 0, "sdc": 0}
    for _ in range(RUNS):
        sim_results = simulate_system(pim, policy, TRIALS)
        for k in agg:
            agg[k] += sim_results[k]
    norm = normalize_results(agg, TRIALS * RUNS, len(pim.components())) 

    results[name] = {
        "sim": norm
    }

    print(f"{name} (Simulation):")
    print(f"  SDC rate: {norm['sdc_rate']}")
    print(f"  DUE rate: {norm['due_rate']}")
    print(f"  Corrected rate: {norm['corrected_rate']}")
    
    
print("\n=== FIXED ERROR INJECTION SANITY CHECK ===")

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
print(results)
plot_breakdown(results)