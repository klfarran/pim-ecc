
# assign protection schemes to components
class ProtectionPolicy:
    def __init__(self, rf_scheme, spm_scheme, cache_scheme=None):
        self.rf = rf_scheme
        self.spm = spm_scheme
        self.cache = cache_scheme

    def get_scheme(self, component_name):
        if component_name == "RF":
            return self.rf
        elif component_name == "SPM":
            return self.spm
        elif component_name == "Cache":
            return self.cache
        else:
            return None