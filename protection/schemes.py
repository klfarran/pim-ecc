class ProtectionScheme:
    def __init__(self, name, overhead_factor, latency_penalty,
                 correctable_bits, detectable_bits):
        self.name = name
        self.overhead_factor = overhead_factor
        self.latency_penalty = latency_penalty
        self.correctable_bits = correctable_bits
        self.detectable_bits = detectable_bits

# Predefined schemes
NONE = ProtectionScheme("None", 1.0, 0.0, 0, 0)
PARITY = ProtectionScheme("Parity", 1.1, 0.01, correctable_bits=0, detectable_bits=1)
SECDED = ProtectionScheme("SECDED", 1.2, 0.05, correctable_bits=1, detectable_bits=2)
STRONG = ProtectionScheme("StrongECC", 1.5, 0.1, correctable_bits=2, detectable_bits=4)