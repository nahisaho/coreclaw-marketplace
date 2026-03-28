---
name: scientific-spectral-signal
description: |
 Spectral signal processing skill. Spectroscopy data analysis (UV-Vis/NMR/MS), peak detection, spectral deconvolution, and signal-to-noise optimization.
tu_tools:
 - key: biotools
 name: bio.tools
 description: spectrumtoolsearch
---

# Scientific Spectral & Signal Processing

minspectrum（、IR、UV-Vis etc.）andorganism（ECG, EEG）'s 
preprocessinganalysispipelineskill。、correction、peak、
frequencyanalysis's standardworkflow is provided。

## When to Use

- spectrumdata's preprocessing（correction、、normalization）
- time series's filter（、）
- peakand amount
- frequencyanalysis（EEG δ/θ/α/β/γ）
- spectrumdegreeanalysis andclassification

## Quick Start

## spectrumpreprocessingpipeline

### 1. ALS correction（Exp-11）

```python
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve

def baseline_correction_als(y, lam=1e5, p=0.01, niter=10):
 """
 Asymmetric Least Squares (ALS) by/via。
 's for。
 lam: parameters（large）
 p: parameters（small）
 """
 L = len(y)
 D = sparse.diags([1, -2, 1], [0, -1, -2], shape=(L, L - 2))
 w = np.ones(L)
 for _ in range(niter):
 W = sparse.diags(w)
 Z = W + lam * D.dot(D.transpose)
 z = spsolve(Z, w * y)
 w = p * (y > z) + (1 - p) * (y < z)
 return z

def remove_baseline(spectrum, wavenumbers, lam=1e5, p=0.01):
 """correctionspectrum is returned。"""
 baseline = baseline_correction_als(spectrum, lam=lam, p=p)
 return spectrum - baseline
```

### 2. Savitzky-Golay 

```python
from scipy.signal import savgol_filter

def smooth_spectrum(spectrum, window_length=11, polyorder=3):
 """Savitzky-Golay filterspectrum."""
 return savgol_filter(spectrum, window_length=window_length, polyorder=polyorder)
```

### 3. normalization

```python
def normalize_spectrum(spectrum, method="minmax"):
 """
 spectrum normalization.
 method: 'minmax', 'snv' (Standard Normal Variate), 'area'
 """
 if method == "minmax":
 return (spectrum - spectrum.min) / (spectrum.max - spectrum.min + 1e-10)
 elif method == "snv":
 return (spectrum - spectrum.mean) / (spectrum.std + 1e-10)
 elif method == "area":
 return spectrum / (np.trapz(np.abs(spectrum)) + 1e-10)
 else:
 raise ValueError(f"Unknown method: {method}")
```

### 4. peak

```python
from scipy.signal import find_peaks

def detect_peaks(spectrum, wavenumbers=None, height=None,
 prominence=0.05, distance=10, width=None):
 """
 spectrum's peak.
 value: peak、peak
 """
 peaks, properties = find_peaks(
 spectrum, height=height, prominence=prominence,
 distance=distance, width=width
 )

 if wavenumbers is not None:
 peak_positions = wavenumbers[peaks]
 else:
 peak_positions = peaks

 return peaks, peak_positions, properties
```

## organismpipeline

### 5. /filter（Exp-08）

```python
from scipy.signal import butter, sosfilt, iirnotch

def bandpass_filter(signal, fs, lowcut, highcut, order=4):
 """Butterworth filter。"""
 nyq = 0.5 * fs
 sos = butter(order, [lowcut / nyq, highcut / nyq], btype="band", output="sos")
 return sosfilt(sos, signal)

def notch_filter(signal, fs, freq=50.0, Q=30.0):
 """forforfilter（50/60 Hz）。"""
 b, a = iirnotch(freq, Q, fs)
 from scipy.signal import filtfilt
 return filtfilt(b, a, signal)
```

### 6. frequencyanalysis（EEG）

```python
from scipy.signal import welch

EEG_BANDS = {
 "delta": (0.5, 4),
 "theta": (4, 8),
 "alpha": (8, 13),
 "beta": (13, 30),
 "gamma": (30, 100),
}

def band_power(signal, fs, band, method="welch"):
 """specificationfrequency's is computed。"""
 freqs, psd = welch(signal, fs=fs, nperseg=min(len(signal), 256))
 low, high = band
 idx = np.logical_and(freqs >= low, freqs <= high)
 return np.trapz(psd[idx], freqs[idx])

def eeg_band_powers(signal, fs, bands=None):
 """EEG 's allcalculation."""
 if bands is None:
 bands = EEG_BANDS
 powers = {}
 for name, (low, high) in bands.items:
 powers[name] = band_power(signal, fs, (low, high))
 total = sum(powers.values)
 relative = {k: v / total for k, v in powers.items}
 return powers, relative
```

### 7. R & HRV analysis（ECG）

```python
def detect_r_peaks(ecg_signal, fs, height_factor=0.5, distance_ms=300):
 """ECG from R."""
 min_distance = int(distance_ms * fs / 1000)
 threshold = height_factor * np.max(ecg_signal)
 peaks, _ = find_peaks(ecg_signal, height=threshold, distance=min_distance)
 return peaks

def hrv_analysis(r_peaks, fs):
 """R-R intervalfrom HRV is computed。"""
 rr_intervals = np.diff(r_peaks) / fs * 1000 # ms
 return {
 "mean_RR": np.mean(rr_intervals),
 "SDNN": np.std(rr_intervals, ddof=1),
 "RMSSD": np.sqrt(np.mean(np.diff(rr_intervals) ** 2)),
 "pNN50": np.sum(np.abs(np.diff(rr_intervals)) > 50) / len(rr_intervals) * 100,
 "mean_HR": 60000 / np.mean(rr_intervals),
 }
```

### 8. spectrumdegreeanalysis（Exp-11）

```python
from scipy.spatial.distance import cosine
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import squareform

def spectral_similarity_matrix(spectra_dict, method="cosine"):
 """
 spectrum's degree is computed。
 spectra_dict: {name: spectrum_array}
 """
 names = list(spectra_dict.keys)
 n = len(names)
 sim_matrix = np.zeros((n, n))

 for i in range(n):
 for j in range(n):
 if method == "cosine":
 sim_matrix[i, j] = 1 - cosine(spectra_dict[names[i]],
 spectra_dict[names[j]])
 elif method == "pearson":
 sim_matrix[i, j] = np.corrcoef(spectra_dict[names[i]],
 spectra_dict[names[j]])[0, 1]

 return pd.DataFrame(sim_matrix, index=names, columns=names)
```

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `biotools` | bio.tools | spectrumtoolsearch |

## References

### Output Files

| File | Format |
|---|---|
| `results/peak_detection_results.csv` | CSV |
| `results/hrv_metrics.csv` | CSV |
| `results/spectral_similarity.csv` | CSV |
| `figures/spectrum_processed.png` | PNG |
| `figures/peak_detection.png` | PNG |
| `figures/eeg_band_powers.png` | PNG |

#### Reference Experiments

- **Exp-08**: ECG/EEG organism（filter、R 、HRV、）
- **Exp-11**: min（ALS 、peak、degree、clustering）
---

## Harness Optimization (v0.4.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Chemistry/Materials)

Before execution, define:
- [ ] **Target property**: specific value or range (e.g., band gap 1.5-2.0 eV)
- [ ] **Validity domain**: applicable chemical space, temperature/pressure range
- [ ] **Accuracy target**: prediction error threshold (MAE, RMSE)
- [ ] **Structure validation**: expected symmetry, stability criteria

#### Pass Criteria
- Crystal structures validated (symmetry, bond lengths, coordination)
- Thermodynamic stability checked (energy above hull < threshold)
- Predictions include uncertainty estimates
- Units and physical constants verified
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
  |-- Generate report.md with all sections
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
| G5 | All figure/table text is English-only | MUST |
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
