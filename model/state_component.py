
# core abstraction of state component in a pim unit
# FIT = failure in time rate, which is the probability of failure of a component in a given time period
class StateComponent:
    def __init__(self, name, size_bits, access_rate, fit_rate):
        self.name = name
        self.size_bits = size_bits
        self.access_rate = access_rate
        self.fit_rate = fit_rate