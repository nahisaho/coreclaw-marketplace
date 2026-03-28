---
name: scientific-quantum-computing
description: |
 Quantum computing skill. Qiskit/Cirq quantum circuit design, VQE/QAOA algorithms, quantum chemistry simulation, and quantum machine learning experiments.
---

# Scientific Quantum Computing

amountcalculationforanalysissimulationskill。
keyamountframework（Qiskit, Cirq, PennyLane, QuTiP）utilizing、
amountdesignfromto/until is supported。

## When to Use

- amounttimes's designsimulation
- variationalamountvalue (VQE) by/viamoleculeenergycalculation
- QAOA (Quantum Approximate Optimization Algorithm) by/viaoptimization
- amountmachine learning (QML) 's timesdesign
- amounterror
- quantum chemistrycalculation（moleculeconstruction）

## Quick Start

### amountcalculationpipeline

```
Phase 1: Problem Formulation
 - problem's / number/countdefinition
 - amountnumber/countencodingdesign
 - /amount
 ↓
Phase 2: Circuit Design
 - Ansatz selection (EfficientSU2, UCCSD, HEA, etc.)
 - timesconstruction
 - degradation
 ↓
Phase 3: Simulation / Execution
 - 
 - simulation
 - (IBM Quantum, Google QCS)
 ↓
Phase 4: Optimization
 - (COBYLA, SPSA, L-BFGS-B)
 - Gradient calculation (Parameter Shift Rule)
 - convergence
 ↓
Phase 5: Error Mitigation
 - Zero Noise Extrapolation (ZNE)
 - Probabilistic Error Cancellation (PEC)
 - Measurement Error Mitigation
 ↓
Phase 6: Analysis & Reporting
 - energyconvergenceplot
 - amountstatusgraph
 - results'scomparison
```

## Workflow

### 1. Qiskit: amounttimesdesign

```python
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, plot_bloch_multivector

# === basicamounttimes ===
qc = QuantumCircuit(2, 2)

# Bell State generation
qc.h(0) # Hadamard on qubit 0
qc.cx(0, 1) # CNOT: qubit 0 → qubit 1
qc.measure([0, 1], [0, 1])

# simulation
simulator = AerSimulator
compiled = transpile(qc, simulator)
result = simulator.run(compiled, shots=10000).result
counts = result.get_counts
print(f"Bell state measurement: {counts}") # {'00': ~5000, '11': ~5000}

# timesvisualization
print(qc.draw("text"))
```

### 2. VQE (Variational Quantum Eigensolver)

```python
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import JordanWignerMapper
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import COBYLA, SPSA
from qiskit.circuit.library import EfficientSU2
from qiskit.primitives import Estimator

# === H2 molecule'senergy ===
# Step 1: moleculeconstruction
driver = PySCFDriver(atom="H 0 0 0; H 0 0 0.735", basis="sto-3g")
problem = driver.run

# Step 2: Jordan-Wigner mapping ( → qubit)
mapper = JordanWignerMapper
qubit_op = mapper.map(problem.second_q_ops[0])
print(f"Qubit Hamiltonian terms: {len(qubit_op)}")
print(f"Number of qubits: {qubit_op.num_qubits}")

# Step 3: Ansatz (times)
ansatz = EfficientSU2(num_qubits=qubit_op.num_qubits, reps=2,
 entanglement="linear")
print(f"Ansatz parameters: {ansatz.num_parameters}")

# Step 4: VQE 
estimator = Estimator
optimizer = COBYLA(maxiter=500)
vqe = VQE(estimator=estimator, ansatz=ansatz, optimizer=optimizer)

result = vqe.compute_minimum_eigenvalue(qubit_op)
print(f"VQE ground state energy: {result.eigenvalue:.6f} Ha")
print(f"Exact (FCI): -1.137276 Ha")
print(f"Chemical accuracy (1.6 mHa): {abs(result.eigenvalue - (-1.137276)) < 0.0016}")
```

### 3. PennyLane: amountmachine learning

```python
import pennylane as qml
from pennylane import numpy as pnp

# === amountkernelclassification ===
n_qubits = 4
dev = qml.device("default.qubit", wires=n_qubits)

@qml.qnode(dev)
def quantum_kernel_circuit(x1, x2):
 """Quantum kernel: |<φ(x1)|φ(x2)>|²"""
 # Feature map for x1
 for i in range(n_qubits):
 qml.RY(x1[i], wires=i)
 for i in range(n_qubits - 1):
 qml.CNOT(wires=[i, i + 1])
 for i in range(n_qubits):
 qml.RZ(x1[i] ** 2, wires=i)

 # Adjoint feature map for x2
 qml.adjoint(qml.RZ)(x2[0] ** 2, wires=0)
 for i in reversed(range(n_qubits - 1)):
 qml.CNOT(wires=[i, i + 1])
 for i in reversed(range(n_qubits)):
 qml.adjoint(qml.RY)(x2[i], wires=i)

 return qml.probs(wires=range(n_qubits))


# === Variational Quantum Classifier ===
@qml.qnode(dev)
def variational_classifier(weights, x):
 """amountclassificationtimes"""
 # Data encoding (Angle Encoding)
 for i in range(n_qubits):
 qml.RX(x[i], wires=i)

 # Variational layers
 n_layers = weights.shape[0]
 for layer in range(n_layers):
 for i in range(n_qubits):
 qml.RY(weights[layer, i, 0], wires=i)
 qml.RZ(weights[layer, i, 1], wires=i)
 for i in range(n_qubits - 1):
 qml.CNOT(wires=[i, i + 1])

 return qml.expval(qml.PauliZ(0))


def train_vqc(X_train, y_train, n_layers=3, epochs=100, lr=0.01):
 """VQC """
 weights = pnp.random.randn(n_layers, n_qubits, 2, requires_grad=True)
 bias = pnp.array(0.0, requires_grad=True)
 opt = qml.AdamOptimizer(stepsize=lr)

 for epoch in range(epochs):
 def cost_fn(w, b):
 predictions = [variational_classifier(w, x) + b for x in X_train]
 loss = pnp.mean((pnp.array(predictions) - y_train) ** 2)
 return loss

 weights, bias = opt.step(cost_fn, weights, bias)

 if (epoch + 1) % 20 == 0:
 loss = cost_fn(weights, bias)
 print(f"Epoch {epoch+1}: Loss = {loss:.4f}")

 return weights, bias
```

### 4. Cirq: Google Quantum AI

```python
import cirq
import numpy as np

# === Cirq basictimes ===
qubits = cirq.LineQubit.range(3)

circuit = cirq.Circuit([
 cirq.H(qubits[0]),
 cirq.CNOT(qubits[0], qubits[1]),
 cirq.CNOT(qubits[1], qubits[2]),
 cirq.measure(*qubits, key="result"),
])
print(circuit)

# simulation
noise_model = cirq.ConstantQubitNoiseModel(
 qubit_noise_gate=cirq.DepolarizingChannel(p=0.01)
)
noisy_simulator = cirq.DensityMatrixSimulator(noise=noise_model)
result = noisy_simulator.simulate(circuit[:-1]) # without measurement
print(f"State fidelity with noise: {cirq.fidelity(result.final_density_matrix, np.array([[0.5, 0, 0, 0.5], [0, 0, 0, 0], [0, 0, 0, 0], [0.5, 0, 0, 0.5]])):.4f}")
```

### 5. QAOA (Quantum Approximate Optimization Algorithm)

```python
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import Sampler

def solve_maxcut_qaoa(adjacency_matrix, p=2):
 """
 QAOA MaxCut problem

 C(z) = Σ_{(i,j)∈E} (1 - z_i z_j) / 2
 """
 n = len(adjacency_matrix)

 # Hamilton construction
 pauli_list = []
 for i in range(n):
 for j in range(i + 1, n):
 if adjacency_matrix[i][j] != 0:
 # 0.5 * (I - Z_i Z_j)
 z_str = ["I"] * n
 z_str[i] = "Z"
 z_str[j] = "Z"
 pauli_list.append(("".join(z_str), -0.5 * adjacency_matrix[i][j]))
 pauli_list.append(("I" * n, 0.5 * adjacency_matrix[i][j]))

 cost_op = SparsePauliOp.from_list(pauli_list).simplify

 # QAOA
 sampler = Sampler
 optimizer = COBYLA(maxiter=300)
 qaoa = QAOA(sampler=sampler, optimizer=optimizer, reps=p)

 result = qaoa.compute_minimum_eigenvalue(cost_op)
 return result
```

### 6. QuTiP: amountsystem

```python
import qutip

# === amountsystem's time ===
# Jaynes-Cummings (-interaction)
N = 20 # Fock statusnumber/count
wc = 1.0 # Cavity frequency
wa = 1.0 # Atom frequency
g = 0.05 # Coupling strength

# 
a = qutip.tensor(qutip.destroy(N), qutip.qeye(2))
sm = qutip.tensor(qutip.qeye(N), qutip.destroy(2))
H = wc * a.dag * a + wa * sm.dag * sm + g * (a.dag * sm + a * sm.dag)

# initialstatus: |1 photon, excited atom>
psi0 = qutip.tensor(qutip.basis(N, 1), qutip.basis(2, 0))

# time
tlist = np.linspace(0, 25, 1000)
result = qutip.mesolve(H, psi0, tlist, [], [a.dag * a, sm.dag * sm])

# Rabi plot
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(tlist, result.expect[0], label="Cavity photon number")
ax.plot(tlist, result.expect[1], label="Atom excitation")
ax.set_xlabel("Time")
ax.set_ylabel("Expectation value")
ax.set_title("Jaynes-Cummings Model: Rabi Oscillations")
ax.legend
plt.savefig("figures/quantum_rabi.png", dpi=300, bbox_inches="tight")
plt.show
```

---

## Best Practices

1. **Ansatz and 's**: times table high (p ≤ 5 recommended)
2. **Parameter Shift Rule**: gradient's analysiscalculation for
3. **Barren Plateau times**: initial 、problem ansatz selection
4. **errorrequired**: results ZNE / PEC correction
5. ****: VQE results FCI / CCSD(T) and comparison
6. **'sverification**: data for

## Completeness Checklist

- [ ] problem's / number/countdefinition
- [ ] amountencodingansatz design
- [ ] by/viaverification 
- [ ] simulation
- [ ] convergenceverification
- [ ] method and 'scomparison
- [ ] errormethodfor（case）
- [ ] resultsreportconvergenceplotgeneration

## Data Acquisition

> All data retrieval is implemented in Python using `requests` and public REST APIs.
> No external ToolUniverse tools are required.

### Implementation Pattern

```python
import requests
import pandas as pd

def fetch_api_data(url, params=None):
    """Generic REST API data retrieval with error handling."""
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()
```

### Report Generation

After data acquisition, generate a structured report:

1. Save raw results to `results/` as CSV/JSON
2. Create visualizations in `figures/`
3. Write `report.md` in the same language as the user's input, summarizing methods, results, and interpretation

## References

### Output Files

| File | Format | Generated When |
|---|---|---|
| `results/quantum_result.json` | amountcalculationresults（JSON） | calculationcompletion |
| `figures/quantum_convergence.png` | convergenceplot | VQE/QAOA completion |
| `figures/quantum_rabi.png` | amountfigure | QuTiP simulation |

### Related Skills

| Skill | Integration |
|---|---|
| `scientific-cheminformatics` | ← moleculestructure → |
| `scientific-process-optimization` | ← QAOA by/viaoptimization |
| `scientific-statistical-testing` | ← amountmeasurementresults'sanalysis |
| `scientific-deep-learning` | → amount- ML |
| `scientific-bayesian-statistics` | ← Bayesianoptimizationby/via VQE parametersoptimization |
---

## Harness Optimization (v0.5.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria

Before execution, define:
- [ ] **Objective**: specific, measurable outcome
- [ ] **Input requirements**: data format, size, quality
- [ ] **Output specification**: expected files, formats, metrics
- [ ] **Success threshold**: quantitative pass/fail criteria

#### Pass Criteria
- All specified outputs produced and validated
- Results reproducible with same inputs and seed
- Error cases handled gracefully with informative messages
- Performance within acceptable time/memory bounds
### Verification Loop

```
Phase 1: PLAN
  |-- Define eval criteria (above checklist)
  |-- Confirm input data availability and format
  |-- Select analysis methods with justification
  +-- Estimate resource requirements (time, memory, API calls)

Phase 2: EXECUTE
  |-- Run analysis pipeline step-by-step
  |-- Save intermediate results after each major step
  |-- Log execution time per step
  +-- Capture warnings/errors without stopping

Phase 3: VERIFY
  |-- Check all Pass Criteria (above)
  |-- Validate output file existence and non-empty
  |-- Cross-check numeric results for sanity (ranges, signs, units)
  |-- Verify figures are readable and correctly labeled
  +-- Run regression check: did existing outputs break?

Phase 4: RECOVER (on failure)
  |-- Identify failed phase and root cause
  |-- Isolate minimum reproducer
  |-- Apply fix and re-run only failed phase
  |-- Log fix as reusable pattern
  +-- If unrecoverable: document limitation and partial results

Phase 5: REPORT
  |-- Generate report.md with all sections in the user's input language
  |-- Embed all figures with captions
  |-- Save numeric results as JSON/CSV
  |-- List all generated files
  +-- Record execution metadata (duration, versions, seed)
```

### Quality Gates

| Gate | Check | Required |
|------|-------|----------|
| G1 | All figures saved to `figures/` (not `plt.show()`) | MUST |
| G2 | All figures embedded in `report.md` | MUST |
| G3 | Numeric results saved as JSON/CSV in `results/` | MUST |
| G4 | Report includes methods, results, discussion | MUST |
| G5 | All figure/table text is English-only; report.md body matches the user's input language | MUST |
| G6 | No hardcoded paths (use `Path` / config) | MUST |
| G7 | Random seed set and documented | MUST |
| G8 | Execution time logged | RECOMMENDED |
| G9 | Input validation performed | RECOMMENDED |
| G10 | Error messages are actionable | RECOMMENDED |

### Model Routing

| Task Complexity | Model Tier | Examples |
|----------------|-----------|----------|
| Mechanical | `fast` (haiku-class) | Data formatting, file I/O, unit conversion |
| Implementation | `standard` (sonnet-class) | Analysis code, pipeline execution, plotting |
| Reasoning | `premium` (opus-class) | Hypothesis generation, result interpretation, review |

### Sub-Agent Orchestration

When the task is complex, split into parallel sub-agents:

```
Orchestrator (this skill)
|-- Agent 1: Data preparation and validation
|-- Agent 2: Core analysis / computation
|-- Agent 3: Visualization and figure generation
+-- Agent 4: Report writing and quality check
```

Each sub-agent receives:
- Specific scope (what to do)
- Input specification (what data to use)
- Output specification (what files to produce)
- Quality gate subset (which gates to check)

### Token Optimization

- Load only the sub-skill needed for the current task
- Compact context after each major phase (discard intermediate logs)
- Use structured output (JSON) over prose for intermediate results
- Prefer code templates over natural language descriptions
- Cache expensive computations (API calls, model training)

### Error Recovery Protocol

```python
def execute_with_recovery(pipeline_steps, max_retries=2):
    results = {}
    for step in pipeline_steps:
        for attempt in range(max_retries + 1):
            try:
                results[step.name] = step.execute()
                break
            except Exception as e:
                if attempt < max_retries:
                    log(f"Step '{step.name}' failed (attempt {attempt+1}): {e}")
                    step.adjust_params()  # reduce batch size, increase timeout
                else:
                    log(f"Step '{step.name}' unrecoverable: {e}")
                    results[step.name] = {"status": "failed", "error": str(e)}
    return results
```
