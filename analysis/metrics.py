from analysis.error_model import residual_error_rate, effective_error_rate, classify_error

def compute_system_error(pim_unit, policy):
    total = 0.0

    for comp in pim_unit.components():
        scheme = policy.get_scheme(comp.name)
        total += residual_error_rate(comp, scheme)

    return total

def compute_system_metrics(pim_unit, policy):
    total_corrected = 0.0
    total_due = 0.0
    total_sdc = 0.0

    for comp in pim_unit.components():
        scheme = policy.get_scheme(comp.name)

        errors = effective_error_rate(comp)

        corrected, due, sdc = classify_error(errors, scheme)

        total_corrected += corrected
        total_due += due
        total_sdc += sdc

    return {
        "corrected": total_corrected,
        "due": total_due,
        "sdc": total_sdc
    }