class ProtectionScheme:
    def __init__(self, name, overhead_factor, latency_penalty,
                 detect_prob, correct_prob):
        self.name = name
        self.overhead_factor = overhead_factor
        self.latency_penalty = latency_penalty
        self.detect_prob = detect_prob     # probability the error is detected
        self.correct_prob = correct_prob   # probability the error is corrected


# Predefined schemes
NONE = ProtectionScheme("None", 1.0, 0.0, detect_prob=0.0, correct_prob=0.0)
PARITY = ProtectionScheme("Parity", 1.1, 0.01, detect_prob=0.99, correct_prob=0.0)
SECDED = ProtectionScheme("SECDED", 1.2, 0.05, detect_prob=0.999, correct_prob=0.99)
STRONG = ProtectionScheme("StrongECC", 1.5, 0.1, detect_prob=0.9999, correct_prob=0.999)