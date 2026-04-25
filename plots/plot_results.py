import matplotlib.pyplot as plt
import numpy as np
from config import small_pim, no_protection, balanced, strong
from analysis.simulation import simulate_system, normalize_results
from analysis.metrics import compute_system_metrics
from analysis.cost_model import compute_cost


def plot_breakdown(results):
    import numpy as np
    import matplotlib.pyplot as plt

    policies = list(results.keys())
    x = np.arange(len(policies))
    width = 0.25

    cmap = plt.cm.viridis
    metric_colors = {
        "sdc": cmap(0.15),
        "due": cmap(0.5),
        "corrected": cmap(0.85)
    }

    sdc = [results[p]["sim"]["sdc_rate"] for p in policies]
    due = [results[p]["sim"]["due_rate"] for p in policies]
    corr = [results[p]["sim"]["corrected_rate"] for p in policies]

    plt.figure()

    # bars grouped by policy, colored by metric
    plt.bar(x - width, sdc, width, color=metric_colors["sdc"], label="SDC")
    plt.bar(x, due, width, color=metric_colors["due"], label="DUE")
    plt.bar(x + width, corr, width, color=metric_colors["corrected"], label="Corrected")

    plt.xticks(x, policies)
    plt.yscale("log")
    plt.xlabel("Policy")
    plt.ylabel("Rate")
    plt.title("Fault Outcome Breakdown by Policy")

    plt.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.15),
        ncol=3
    )

    plt.tight_layout()
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
    
    
