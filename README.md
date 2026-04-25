# PIM Reliability Framework (State Protection + ECC Modeling)

This project models reliability in (PIM) architectures, focusing specifically on **stateful components (register files, scratchpads, caches)** and how different protection schemes affect system reliability.

It extends prior ECC modeling work in PIMeval by introducing a configurable framework for evaluating **internal state protection + memory interface protection**.

---

## Project Goal

The goal of this project is to:

- Model soft errors in PIM **stateful storage components**
- Evaluate different protection strategies (Parity, SECDED, Strong ECC)
- Measure tradeoffs between:
  - Silent Data Corruption (SDC)
  - Detected Uncorrectable Errors (DUE)
  - Area / latency overhead

We intentionally **do not model compute-unit faults**, focusing instead on state reliability.

---

## Project Structure
```
model/           
├── state_component.py   # Defines RF / SPM / Cache abstractions
├── pim_unit.py          # Groups components into a PIM unit

protection/      
├── schemes.py           # ECC / parity / protection definitions
├── policy.py            # Maps protection schemes to components

analysis/        
├── error_model.py       # Base + effective error rate modeling
├── metrics.py           # System-level SDC / DUE computation
├── simulation.py       # Monte Carlo fault injection model
├── cost_model.py       # Area + latency overhead modeling

plots/           
├── plot_results.py     # Generates evaluation figures

config.py               # Predefined PIM systems and policies
main.py                 # Entry point for running experiments
```



