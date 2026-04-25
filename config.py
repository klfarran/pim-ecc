from model.state_component import StateComponent
from model.pim_unit import PIMUnit
from protection.schemes import NONE, PARITY, SECDED, STRONG
from protection.policy import ProtectionPolicy

# Example system
def small_pim():
    rf = StateComponent("RF", size_bits=1024, access_rate=1.0, fit_rate=1e-9)
    spm = StateComponent("SPM", size_bits=65536, access_rate=0.2, fit_rate=1e-9)
    return PIMUnit(rf, spm)


# Example policies
def no_protection():
    return ProtectionPolicy(NONE, NONE)

def balanced():
    return ProtectionPolicy(PARITY, SECDED)

def strong():
    return ProtectionPolicy(SECDED, STRONG)