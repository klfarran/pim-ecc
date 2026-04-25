class PIMUnit:
    # rf = register file, spm = scratchpad memory, cache = cache memory
    def __init__(self, rf, spm, cache=None):
        self.rf = rf
        self.spm = spm
        self.cache = cache


    # cache is an optional component
    def components(self):
        comps = [self.rf, self.spm]
        if self.cache:
            comps.append(self.cache)
        return comps