def base_error_rate(component):
    return component.size_bits * component.fit_rate

# access rate factored into error rate 
def effective_error_rate(component):
    return base_error_rate(component) * component.access_rate

# error rate after applying protection scheme 
def residual_error_rate(component, scheme):
    eff = effective_error_rate(component)
    return eff * (1 - scheme.coverage)

# copmute useful metrics like due and sdc
def classify_error(num_errors, scheme):
    corrected = num_errors * scheme.correct_prob
    detected = num_errors * scheme.detect_prob

    due = detected - corrected
    sdc = num_errors - detected

    return corrected, due, sdc