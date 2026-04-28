import random

def base_error_rate(component, scheme):
    effective_bits = component.size_bits * scheme.overhead_factor
    return effective_bits * component.fit_rate


def effective_error_rate(component, scheme):
    return base_error_rate(component, scheme) * component.access_rate


def sample_bit_flips():
    r = random.random()

    if r < 0.90:
        return 1
    elif r < 0.98:
        return 2
    else:
        return 3
    

def classify_error_bits(num_flips, scheme):
    if num_flips <= scheme.correctable_bits:
        return "corrected"
    elif num_flips <= scheme.detectable_bits:
        return "due"
    else:
        return "sdc"