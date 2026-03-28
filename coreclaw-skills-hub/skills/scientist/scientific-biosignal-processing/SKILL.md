---
name: scientific-biosignal-processing
description: |
 Biosignal processing skill. EEG, ECG, EMG signal processing with filtering, spectral analysis, wavelet transforms, and time-frequency analysis pipelines.
tu_tools:
 - key: biotools
 name: bio.tools
 description: organismtoolsearch
---

# Scientific Biosignal Processing

figure（ECG）、brain（EEG）、figure（EMG）、etc.'s organism and
preprocessingfeaturesextractionvisualizationpipeline。spectral-signal skillmindata
（IRUV-Vis）and 's 、papersskill timeaxis's data.

## When to Use

- ECG 's R HRV analysiswhen needed
- EEG 's extractionERP analysiswhen needed
- EMG 'sonset analysiswhen needed
- organism'sdatawhen handling

---

## Quick Start

## 1. ECG analysispipeline

### 1.1 PQRST synthesis（test datafor）

```python
import numpy as np
from scipy.signal import butter, filtfilt, find_peaks

def synthesize_ecg(duration_s=10, fs=500, heart_rate_bpm=72, noise_level=0.05):
 """testingforsynthesis ECG is generated。"""
 t = np.arange(0, duration_s, 1/fs)
 beat_interval = 60 / heart_rate_bpm
 ecg = np.zeros_like(t)

 beat_times = np.arange(0, duration_s, beat_interval)
 for bt in beat_times:
 # P
 ecg += 0.15 * np.exp(-((t - bt + 0.16)**2) / (2 * 0.01**2))
 # QRSgroup
 ecg += -0.10 * np.exp(-((t - bt + 0.04)**2) / (2 * 0.005**2))
 ecg += 1.00 * np.exp(-((t - bt)**2) / (2 * 0.008**2))
 ecg += -0.15 * np.exp(-((t - bt - 0.04)**2) / (2 * 0.005**2))
 # T
 ecg += 0.30 * np.exp(-((t - bt - 0.20)**2) / (2 * 0.03**2))

 ecg += noise_level * np.random.randn(len(t))
 return t, ecg
```

### 1.2 R 

```python
def detect_r_peaks(ecg, fs, min_distance_ms=300):
 """ECG fromR、RRinterval is computed。"""
 min_distance = int(min_distance_ms * fs / 1000)
 height_threshold = np.mean(ecg) + 0.6 * np.std(ecg)

 r_peaks, properties = find_peaks(ecg, height=height_threshold,
 distance=min_distance)
 rr_intervals_ms = np.diff(r_peaks) / fs * 1000 # ms

 return r_peaks, rr_intervals_ms
```

### 1.3 HRV timeanalysis

```python
def hrv_time_domain(rr_intervals_ms):
 """
 HRV time is computed。

 Returns:
 dict with keys: mean_rr, sdnn, rmssd, pnn50, mean_hr
 """
 rr = np.array(rr_intervals_ms)
 diff_rr = np.diff(rr)

 return {
 "mean_rr_ms": np.mean(rr),
 "sdnn_ms": np.std(rr, ddof=1),
 "rmssd_ms": np.sqrt(np.mean(diff_rr**2)),
 "pnn50_pct": np.sum(np.abs(diff_rr) > 50) / len(diff_rr) * 100,
 "mean_hr_bpm": 60000 / np.mean(rr),
 "cv_rr": np.std(rr, ddof=1) / np.mean(rr) * 100,
 }
```

### 1.4 HRV frequencyanalysis

```python
from scipy.signal import welch

def hrv_frequency_domain(rr_intervals_ms, fs_interp=4):
 """
 HRV frequency is computed。

 definition:
 VLF: 0.003 - 0.04 Hz
 LF: 0.04 - 0.15 Hz
 HF: 0.15 - 0.40 Hz

 Returns:
 dict with vlf_power, lf_power, hf_power, lf_hf_ratio, total_power
 """
 from scipy.interpolate import interp1d

 rr_s = np.array(rr_intervals_ms) / 1000
 cum_time = np.cumsum(rr_s)
 cum_time -= cum_time[0]

 # intervalsampling
 t_interp = np.arange(0, cum_time[-1], 1/fs_interp)
 f_interp = interp1d(cum_time, rr_s, kind="cubic", fill_value="extrapolate")
 rr_resampled = f_interp(t_interp)
 rr_resampled -= np.mean(rr_resampled)

 # Welch PSD
 freqs, psd = welch(rr_resampled, fs=fs_interp, nperseg=min(256, len(rr_resampled)))

 # and 's
 vlf_mask = (freqs >= 0.003) & (freqs < 0.04)
 lf_mask = (freqs >= 0.04) & (freqs < 0.15)
 hf_mask = (freqs >= 0.15) & (freqs < 0.40)

 vlf = np.trapz(psd[vlf_mask], freqs[vlf_mask])
 lf = np.trapz(psd[lf_mask], freqs[lf_mask])
 hf = np.trapz(psd[hf_mask], freqs[hf_mask])

 return {
 "vlf_power_ms2": vlf * 1e6,
 "lf_power_ms2": lf * 1e6,
 "hf_power_ms2": hf * 1e6,
 "lf_hf_ratio": lf / (hf + 1e-10),
 "total_power_ms2": (vlf + lf + hf) * 1e6,
 }
```

### 1.5 Poincaré plot

```python
import matplotlib.pyplot as plt

def poincare_plot(rr_intervals_ms, figsize=(8, 8)):
 """
 Poincaré plot (RR_n vs RR_n+1) drawing/plotting.
 SD1: （）
 SD2: （+）
 """
 rr = np.array(rr_intervals_ms)
 rr_n = rr[:-1]
 rr_n1 = rr[1:]

 # SD1, SD2
 diff = rr_n1 - rr_n
 sd1 = np.std(diff / np.sqrt(2), ddof=1)
 sd2 = np.std((rr_n + rr_n1) / np.sqrt(2), ddof=1)

 fig, ax = plt.subplots(figsize=figsize)
 ax.scatter(rr_n, rr_n1, c="steelblue", alpha=0.5, s=15)
 ax.plot([rr.min, rr.max], [rr.min, rr.max], "k--", alpha=0.3)

 # 
 from matplotlib.patches import Ellipse
 center = (np.mean(rr_n), np.mean(rr_n1))
 ellipse = Ellipse(center, width=2*sd2, height=2*sd1, angle=45,
 fill=False, color="red", linewidth=2)
 ax.add_patch(ellipse)

 ax.set_xlabel("RR_n (ms)")
 ax.set_ylabel("RR_{n+1} (ms)")
 ax.set_title(f"Poincaré Plot (SD1={sd1:.1f}, SD2={sd2:.1f})",
 fontweight="bold")
 ax.set_aspect("equal")
 plt.tight_layout
 plt.savefig("figures/poincare_plot.png", dpi=300, bbox_inches="tight")
 plt.close

 return {"sd1_ms": sd1, "sd2_ms": sd2, "sd1_sd2_ratio": sd1/sd2}
```

---

## 2. EEG analysispipeline

### 2.1 extraction

```python
EEG_BANDS = {
 "delta": (0.5, 4),
 "theta": (4, 8),
 "alpha": (8, 13),
 "beta": (13, 30),
 "gamma": (30, 50),
}

def extract_band_power(eeg, fs, bands=None):
 """
 EEG fromeachfrequency's phase is extracted。
 """
 if bands is None:
 bands = EEG_BANDS

 freqs, psd = welch(eeg, fs=fs, nperseg=min(fs*2, len(eeg)))
 total_power = np.trapz(psd, freqs)

 band_powers = {}
 for band_name, (low, high) in bands.items:
 mask = (freqs >= low) & (freqs < high)
 power = np.trapz(psd[mask], freqs[mask])
 band_powers[f"{band_name}_abs"] = power
 band_powers[f"{band_name}_rel"] = power / total_power * 100

 return band_powers
```

### 2.2 log

```python
from scipy.signal import spectrogram

def plot_spectrogram(eeg, fs, channel_name="EEG", max_freq=50, figsize=(12, 4)):
 """EEG 's log（time-frequencytable） drawing/plotting."""
 nperseg = min(fs * 2, len(eeg))
 f, t, Sxx = spectrogram(eeg, fs=fs, nperseg=nperseg,
 noverlap=nperseg//2)

 freq_mask = f <= max_freq

 fig, ax = plt.subplots(figsize=figsize)
 im = ax.pcolormesh(t, f[freq_mask], 10 * np.log10(Sxx[freq_mask] + 1e-10),
 shading="gouraud", cmap="viridis")
 ax.set_ylabel("Frequency (Hz)")
 ax.set_xlabel("Time (s)")
 ax.set_title(f"Spectrogram — {channel_name}", fontweight="bold")
 plt.colorbar(im, ax=ax, label="Power (dB)")
 plt.tight_layout
 plt.savefig(f"figures/spectrogram_{channel_name}.png", dpi=300,
 bbox_inches="tight")
 plt.close
```

### 2.3 ERP (Event-Related Potential)

```python
def compute_erp(eeg, fs, event_times_s, window_s=(-0.2, 0.8)):
 """
 （ERP） calculation.

 Parameters:
 eeg: 1D EEG signal
 fs: samplingfrequency
 event_times_s: 's (sec)
 window_s: (pre, post) (sec)

 Returns:
 erp_mean: mean ERP, erp_sem: standard error, t_axis: timeaxis
 """
 pre_samples = int(abs(window_s[0]) * fs)
 post_samples = int(window_s[1] * fs)
 total = pre_samples + post_samples

 epochs = []
 for evt in event_times_s:
 idx = int(evt * fs)
 start = idx - pre_samples
 end = idx + post_samples
 if start >= 0 and end <= len(eeg):
 epoch = eeg[start:end]
 epoch = epoch - np.mean(epoch[:pre_samples]) # baseline correction
 epochs.append(epoch)

 epochs = np.array(epochs)
 t_axis = np.linspace(window_s[0], window_s[1], total)
 erp_mean = np.mean(epochs, axis=0)
 erp_sem = np.std(epochs, axis=0) / np.sqrt(len(epochs))

 return erp_mean, erp_sem, t_axis


def detect_erp_components(erp, t_axis, components=None):
 """ERP component（N100, P300 etc.）'s peak."""
 if components is None:
 components = {
 "N100": {"window": (0.08, 0.15), "polarity": "negative"},
 "P200": {"window": (0.15, 0.25), "polarity": "positive"},
 "P300": {"window": (0.25, 0.50), "polarity": "positive"},
 }

 results = {}
 for name, spec in components.items:
 mask = (t_axis >= spec["window"][0]) & (t_axis <= spec["window"][1])
 segment = erp[mask]
 t_seg = t_axis[mask]
 if spec["polarity"] == "negative":
 idx = np.argmin(segment)
 else:
 idx = np.argmax(segment)
 results[name] = {
 "latency_ms": t_seg[idx] * 1000,
 "amplitude_uV": segment[idx],
 }
 return results
```

---

## 3. EMG analysis

```python
def emg_envelope(emg, fs, cutoff=10):
 """EMG 's line（Hilbert transformation + filter） is computed。"""
 from scipy.signal import hilbert
 analytic = hilbert(emg)
 envelope = np.abs(analytic)

 b, a = butter(4, cutoff / (fs / 2), btype="low")
 envelope_smooth = filtfilt(b, a, envelope)
 return envelope_smooth


def detect_muscle_bursts(envelope, fs, threshold_factor=2.0,
 min_duration_ms=50):
 """EMG （start）."""
 threshold = np.mean(envelope) + threshold_factor * np.std(envelope)
 active = envelope > threshold
 min_samples = int(min_duration_ms * fs / 1000)

 bursts = []
 in_burst = False
 start = 0
 for i, val in enumerate(active):
 if val and not in_burst:
 start = i
 in_burst = True
 elif not val and in_burst:
 duration = i - start
 if duration >= min_samples:
 bursts.append({
 "onset_s": start / fs,
 "offset_s": i / fs,
 "duration_ms": duration / fs * 1000,
 "peak_amplitude": np.max(envelope[start:i]),
 })
 in_burst = False

 return bursts
```

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `biotools` | bio.tools | organismtoolsearch |

## References

- **Exp-08**: ECG RHRVPoincaré、EEG logERP、EMG
---

## Harness Optimization (v0.4.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Bioinformatics)

Before execution, define:
- [ ] **Organism/assembly**: genome build, annotation version
- [ ] **Input format**: FASTQ/BAM/VCF/GFF/AnnData expected schema
- [ ] **Quality thresholds**: min read quality, min coverage, FDR cutoff
- [ ] **Normalization**: method and justification

#### Pass Criteria
- QC metrics reported (read quality, mapping rate, duplication rate)
- All gene/protein IDs mapped to standard nomenclature
- Multiple testing correction applied (BH/Bonferroni)
- Biological replicates handled appropriately
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
