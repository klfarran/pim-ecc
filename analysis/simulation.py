import random
from .error_model import effective_error_rate


# simulate system behavior under many trials (10,000) to estimate averages
# this is probabilistic fault modelling, not fixed error injection
def simulate_component(component, scheme, trials=10000):
    """
    Simulate fault injection for a single component.

    Returns:
        dict with counts of corrected, due, sdc
    """
    corrected = 0
    due = 0
    sdc = 0

    error_prob = effective_error_rate(component)

    for _ in range(trials):
        # does an error occur? 
        # e.g., if error_prob = 0.001, then ~0.1% of iterations will enter this block 
        if random.random() < error_prob:

            r = random.random()

            # classify outcome
            if r < scheme.correct_prob:
                corrected += 1
            elif r < scheme.detect_prob:
                due += 1
            else:
                sdc += 1

    return {
        "corrected": corrected,
        "due": due,
        "sdc": sdc
    }
    
    
def simulate_system(pim_unit, policy, trials=10000):
    """
    Simulate entire PIM unit.
    """
    total = {
        "corrected": 0,
        "due": 0,
        "sdc": 0
    }

    for comp in pim_unit.components():
        scheme = policy.get_scheme(comp.name)

        results = simulate_component(comp, scheme, trials)

        total["corrected"] += results["corrected"]
        total["due"] += results["due"]
        total["sdc"] += results["sdc"]

    return total


def normalize_results(results, trials, num_components):
    total_trials = trials * num_components

    return {
        "corrected_rate": results["corrected"] / total_trials,
        "due_rate": results["due"] / total_trials,
        "sdc_rate": results["sdc"] / total_trials
    }
    
    
    
# fixed error injection for sanity-checking
# fixed error injection for one component: 
def inject_fixed_errors(scheme, num_errors):
    corrected = 0
    due = 0
    sdc = 0

    for _ in range(num_errors):
        r = random.random()

        if r < scheme.correct_prob:
            corrected += 1
        elif r < scheme.detect_prob:
            due += 1
        else:
            sdc += 1

    return {
        "corrected": corrected,
        "due": due,
        "sdc": sdc
    }


# fixed error injection for the system of n components:
def inject_fixed_system(pim_unit, policy, num_errors_per_component=1000):
    total = {"corrected": 0, "due": 0, "sdc": 0}

    for comp in pim_unit.components():
        scheme = policy.get_scheme(comp.name)

        results = inject_fixed_errors(scheme, num_errors_per_component)

        total["corrected"] += results["corrected"]
        total["due"] += results["due"]
        total["sdc"] += results["sdc"]

    return total