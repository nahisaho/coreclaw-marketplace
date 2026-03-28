---
name: scientific-spectral-signal
description: |
 minspectrumandorganism's preprocessinganalysisskill。correction、filter、
 peak、analysis is performedfor。
 Scientific Skills Exp-08（ECG/EEG）、Exp-11（min）。
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
