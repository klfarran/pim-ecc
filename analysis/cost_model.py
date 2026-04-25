def compute_cost(pim_unit, policy):
    total_area = 0.0
    total_latency = 0.0

    for comp in pim_unit.components():
        scheme = policy.get_scheme(comp.name)

        total_area += comp.size_bits * scheme.overhead_factor
        total_latency += scheme.latency_penalty

    return {
        "area": total_area,
        "latency": total_latency
    }