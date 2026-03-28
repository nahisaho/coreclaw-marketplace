---
name: scientific-quantum-computing
description: |
 amountcalculationskill。QiskitCirqPennyLaneQuTiP utilizing、
 amounttimesdesignsimulationvariationalamount（VQE/QAOA）
 quantum chemistrycalculationamountmachine learning support。
 「amounttimes design」「VQE energy」「amountsimulation」 。
tu_tools:
 - key: papers_with_code
 name: Papers with Code
 description: amountcalculationpapersearch
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

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `papers_with_code` | Papers with Code | amountcalculationpapersearch |

## References

### Output Files

| File | Format | Generation Timing |
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
