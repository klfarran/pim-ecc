from model.state_component import StateComponent
from model.pim_unit import PIMUnit
from protection.schemes import NONE, PARITY, SECDED, STRONG
from protection.policy import ProtectionPolicy

# failure in time rates for different component types (per bit per hour)
LOW_FIT  = 1e-10   # hardened / small structures
MED_FIT  = 1e-9    # typical SRAM
HIGH_FIT = 1e-8    # large / dense / vulnerable

# lightweight ALU-focused PIM unit
def alu_pim():
    rf = StateComponent("RF", size_bits=512, access_rate=1.0, Lfit_rate=LOW_FIT)
    spm = StateComponent("SPM", size_bits=8192, access_rate=0.3, fit_rate=MED_FIT)
    return PIMUnit(rf, spm)


def small_pim():
    rf = StateComponent("RF", size_bits=1024, access_rate=1.0, fit_rate=LOW_FIT)
    spm = StateComponent("SPM", size_bits=65536, access_rate=0.2, fit_rate=MED_FIT)
    return PIMUnit(rf, spm)

# large scratchpad, memory-heavy PIM unit
def memory_heavy_pim():
    rf = StateComponent("RF", size_bits=2048, access_rate=0.8, fit_rate=LOW_FIT)
    spm = StateComponent("SPM", size_bits=262144, access_rate=0.1, fit_rate=HIGH_FIT)
    return PIMUnit(rf, spm)

# Example policies
# first param = RF protection scheme, second param = SPM protection scheme
def no_protection():
    return ProtectionPolicy(NONE, NONE)

# protect scratchpad only
def spm_only():
    return ProtectionPolicy(NONE, SECDED)

# minimal protection everywhere
def minimal():
    return ProtectionPolicy(PARITY, PARITY)

def balanced():
    return ProtectionPolicy(PARITY, SECDED)

def strong():
    return ProtectionPolicy(SECDED, STRONG)