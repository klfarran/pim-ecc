from analysis.error_model import effective_error_rate

BIT_FLIP_DISTRIBUTION = {
    1: 0.90,
    2: 0.08,
    3: 0.02
}

def classify_expected(errors, scheme):
    corrected = 0.0
    due = 0.0
    sdc = 0.0

    for flips, prob in BIT_FLIP_DISTRIBUTION.items():
        if flips <= scheme.correctable_bits:
            corrected += errors * prob
        elif flips <= scheme.detectable_bits:
            due += errors * prob
        else:
            sdc += errors * prob

    return corrected, due, sdc

def compute_system_metrics(pim_unit, policy):
    total_corrected = 0.0
    total_due = 0.0
    total_sdc = 0.0

    for comp in pim_unit.components():
        scheme = policy.get_scheme(comp.name)
        errors = effective_error_rate(comp, scheme)

        corrected, due, sdc = classify_expected(errors, scheme)

        total_corrected += corrected
        total_due += due
        total_sdc += sdc

    return {
        "corrected": total_corrected,
        "due": total_due,
        "sdc": total_sdc
    }