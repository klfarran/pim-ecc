import matplotlib.pyplot as plt

from config import small_pim, no_protection, balanced, strong
from analysis.simulation import simulate_system, normalize_results
from analysis import compute_system_metrics, compute_cost


TRIALS = 100000  # increase for smoother curves


def run_all_policies():
    pim = small_pim()

    policies = {
        "None": no_protection(),
        "Balanced": balanced(),
        "Strong": strong()
    }

    results = {}

    for name, policy in policies.items():
        sim = simulate_system(pim, policy, TRIALS)
        norm = normalize_results(sim, TRIALS, len(pim.components()))
        cost = compute_cost(pim, policy)
        analytic = compute_system_metrics(pim, policy)

        results[name] = {
            "sim": norm,
            "analytic": analytic,
            "cost": cost
        }

    return results


def plot_breakdown(results):
    policies = list(results.keys())

    sdc = [results[p]["sim"]["sdc_rate"] for p in policies]
    due = [results[p]["sim"]["due_rate"] for p in policies]
    corr = [results[p]["sim"]["corrected_rate"] for p in policies]

    x = range(len(policies))

    plt.figure()

    plt.bar(x, sdc, label="SDC")
    plt.bar(x, due, bottom=sdc, label="DUE")
    plt.bar(x, corr, bottom=[s + d for s, d in zip(sdc, due)], label="Corrected")

    plt.xticks(x, policies)
    plt.yscale("log")
    plt.xlabel("Policy")
    plt.ylabel("Rate")
    plt.title("Fault Outcome Breakdown by Policy")
    plt.legend()

    plt.show()
    
    
    
def plot_sdc_only(results):
    policies = list(results.keys())
    sdc = [results[p]["sim"]["sdc_rate"] for p in policies]

    plt.figure()

    plt.bar(policies, sdc)
    plt.yscale("log")
    plt.xlabel("Policy")
    plt.ylabel("SDC Rate")
    plt.title("Silent Data Corruption Across Policies")

    plt.show()
    
    
def plot_cost_vs_reliability(results):
    policies = list(results.keys())

    sdc = [results[p]["sim"]["sdc_rate"] for p in policies]
    cost = [results[p]["cost"]["area"] for p in policies]

    plt.figure()

    plt.scatter(cost, sdc)

    for i, p in enumerate(policies):
        plt.annotate(p, (cost[i], sdc[i]))

    plt.xlabel("Area Cost (relative)")
    plt.ylabel("SDC Rate")
    plt.yscale("log")
    plt.title("Reliability vs Cost Tradeoff")

    plt.show()
    
    
