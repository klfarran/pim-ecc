# interactive_runner.py
from config import *
from model.state_component import StateComponent
from model.pim_unit import PIMUnit
from protection.schemes import NONE, PARITY, SECDED, STRONG
from protection.policy import ProtectionPolicy

from analysis.metrics import compute_system_metrics
from analysis.cost_model import compute_cost
from analysis.simulation import simulate_system, normalize_results
from plots.plot_results import plot_breakdown, plot_sdc_only, plot_cost_vs_reliability
from experiments import run_experiment

def choose_scheme(name):
    print(f"\nChoose protection for {name}:")
    print("  1. none")
    print("  2. parity")
    print("  3. secded")
    print("  4. strong")

    while True:
        choice = input("> ").strip()

        scheme = {
            "1": NONE,
            "2": PARITY,
            "3": SECDED,
            "4": STRONG ()
        }.get(choice)

        if scheme is not None:
            return scheme

        print("Invalid choice. Please enter 1, 2, 3, or 4.")


def build_pim():
    while True:
        try:
            rf_size = int(input("RF size (bits): ").strip())
            spm_size = int(input("SPM size (bits): ").strip())
            break
        except ValueError:
            print("Please enter valid integer sizes.")

    use_cache = input("Add cache? (y/n): ").strip().lower()

    cache = None
    if use_cache == "y":
        while True:
            try:
                cache_size = int(input("Cache size (bits): ").strip())
                cache = StateComponent("Cache", cache_size, 0.5, 1e-9)
                break
            except ValueError:
                print("Please enter a valid integer for cache size.")

    rf = StateComponent("RF", rf_size, 1.0, 1e-9)
    spm = StateComponent("SPM", spm_size, 0.2, 1e-9)

    return PIMUnit(rf, spm, cache)


def build_policy():
    rf = choose_scheme("RF")
    spm = choose_scheme("SPM")

    cache = None
    has_cache = input("Is cache present in system? (y/n): ").strip().lower()

    if has_cache == "y":
        cache = choose_scheme("Cache")

    return ProtectionPolicy(rf, spm, cache)


def main():
    pim = build_pim()
    user_policy = build_policy()

    policies = {
        "Baseline": ProtectionPolicy(NONE, NONE),
        "User Configuration": user_policy
    }

    exp = run_experiment(
        pim,
        policies,
        baseline_name="Baseline",
        trials=100000,
        runs=50
    )

    print("\n=== RESULTS ===")
    for name, data in exp["simulation"].items():
        print(f"{name}:")
        print(f"  SDC: {data['sim']['sdc_rate']}")
        print(f"  DUE: {data['sim']['due_rate']}")
        print(f"  Corrected: {data['sim']['corrected_rate']}")

    plot_breakdown(exp["simulation"])
    plot_sdc_only(exp["simulation"])
    plot_cost_vs_reliability(exp["simulation"])


if __name__ == "__main__":
    main()
    
    