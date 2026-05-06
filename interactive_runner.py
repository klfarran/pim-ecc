# interactive_runner.py
from config import *
from model.state_component import StateComponent
from model.pim_unit import PIMUnit
from protection.schemes import NONE, PARITY, SECDED, STRONG, ProtectionScheme
from protection.policy import ProtectionPolicy
from plots.plot_results import plot_breakdown, plot_sdc_only, plot_cost_vs_reliability
from experiments import run_experiment

def choose_scheme(name):
    print(f"\nChoose protection for {name}:")
    print("  1. none")
    print("  2. parity (detects: 1 bit, correct: 0 bits)")
    print("  3. secded (detects: 2 bits, correct: 1 bit)")
    print("  4. strong (detects: 4 bits, correct: 2 bits)")
    print("  5. custom ECC")

    while True:
        choice = input("> ").strip()

        scheme = {
            "1": NONE,
            "2": PARITY,
            "3": SECDED,
            "4": STRONG
        }.get(choice)

        if scheme is not None:
            return scheme

        if choice == "5":
            try:
                name = input("Scheme name: ").strip()
                overhead = float(input("Overhead factor: ").strip())
                latency = float(input("Latency penalty: ").strip())
                correctable = int(input("Correctable bits: ").strip())
                detectable = int(input("Detectable bits: ").strip())

                return ProtectionScheme(
                    name,
                    overhead,
                    latency,
                    correctable,
                    detectable
                )
            except ValueError:
                print("Invalid input, try again.")
        else:
            print("Invalid choice. Please enter 1-5.")


def choose_fit(name):
    print(f"\nChoose FIT rate for {name}:")
    print("  1. LOW_FIT (hardened)")
    print("  2. MED_FIT (standard)")
    print("  3. HIGH_FIT (vulnerable)")
    print("  4. custom value")

    while True:
        choice = input("> ").strip()

        if choice == "1":
            return LOW_FIT
        elif choice == "2":
            return MED_FIT
        elif choice == "3":
            return HIGH_FIT
        elif choice == "4":
            try:
                val = float(input("Enter custom FIT (e.g. 1e-9): ").strip())
                return val
            except ValueError:
                print("Invalid number.")
        else:
            print("Invalid choice. Please enter 1-4.")
            

def build_pim():
    global USE_CACHE
    while True:
        try:
            rf_size = int(input("Input register file size (bits): ").strip())
            spm_size = int(input("Input scratchpad memory size (bits): ").strip())
            rf_fit = choose_fit("RF")
            spm_fit = choose_fit("SPM")
            break
        except ValueError:
            print("Please enter valid integer sizes.")

    while True:
        USE_CACHE = input("Add cache? (y/n): ").strip().lower()
        if USE_CACHE in ("y", "n"):
            break
        print("Invalid input. Please enter 'y' or 'n'.")

    cache = None
    if USE_CACHE == "y":
        while True:
            try:
                cache_size = int(input("Input cache size (bits): ").strip())
                cache_fit = choose_fit("Cache")
                cache = StateComponent("Cache", cache_size, 0.5, cache_fit)
                break
            except ValueError:
                print("Please enter a valid integer for cache size.")

    rf = StateComponent("RF", rf_size, 1.0, rf_fit)
    spm = StateComponent("SPM", spm_size, 0.2, spm_fit)

    return PIMUnit(rf, spm, cache)


def build_policy():
    rf = choose_scheme("RF")
    spm = choose_scheme("SPM")

    cache = None

    if USE_CACHE == "y":
        cache = choose_scheme("Cache")
        #print(f"Selected cache scheme overhead: {cache.overhead_factor}")

    return ProtectionPolicy(rf, spm, cache)


def main():
    pim = build_pim()
    user_policy = build_policy()

    baseline_cache_scheme = NONE if pim.cache is not None else None

    policies = {
        "Baseline": ProtectionPolicy(NONE, NONE, baseline_cache_scheme),
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
    
    