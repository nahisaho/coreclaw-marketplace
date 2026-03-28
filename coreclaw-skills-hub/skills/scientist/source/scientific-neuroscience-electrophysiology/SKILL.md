---
name: scientific-neuroscience-electrophysiology
description: |
 neural/nerveanalysisskill。Neuropixels/electrode's
 (SpikeInterface + Kilosort4)、 (SNR/ISI rate)、
 EEG (MNE-Python)、ECG HRV analysis、
 EDA 、EMG analysis (NeuroKit2)、
 brainbindinganalysis (/) integrationneural/nervepipeline。
tu_tools:
 - key: biotools
 name: bio.tools
 description: analysistoolsearch
---

# Scientific Neuroscience & Electrophysiology

Neuropixels degreeelectrodeEEGECGEMGEDA 'sneural/nerve、
→quality control→feature extraction→analysis's
Standard Pipeline is provided。SpikeInterface + NeuroKit2 + MNE-Python 。

## When to Use

- Neuropixels/MEA 'spipelinewhen needed
- EEG (ERP) analysis is performedand
- ECG from's (HRV) analysisneural/nervesystemevaluationwhen needed
- EDA  'sneural/nerveanalysis is performedand
- brainbinding (/) 'swhen needed

---

## Quick Start

## 1. Neuropixels (SpikeInterface)

```python
import numpy as np
import spikeinterface.full as si


def neuropixels_preprocessing(recording_path, probe_type="NP1",
 output_dir="results/neuroscience"):
 """
 Neuropixels 'spreprocessingpipeline (SpikeInterface)。

 1. SpikeGLX/OpenEphys fileload
 2. filter (300-6000 Hz)
 3. phasecorrection (ADC multiplexing)
 4. CMR (Common Median Reference) 
 5. correction (Motion correction)
 """
 import os
 os.makedirs(output_dir, exist_ok=True)

 # load
 recording = si.read_spikeglx(recording_path)
 print(f" Probe: {probe_type}")
 print(f" Channels: {recording.get_num_channels}")
 print(f" Sampling rate: {recording.get_sampling_frequency} Hz")
 print(f" Duration: {recording.get_total_duration:.1f} sec")

 # preprocessing
 rec_filt = si.bandpass_filter(recording, freq_min=300, freq_max=6000)
 rec_shift = si.phase_shift(rec_filt) # ADC phasecorrection
 rec_cmr = si.common_reference(rec_shift, reference="global",
 operator="median")

 # correction 
 motion_info = si.correct_motion(
 rec_cmr, preset="nonrigid_accurate",
 output_motion_info=True
 )

 print(f" Preprocessing complete: filter → phase_shift → CMR → motion")

 return rec_cmr


def spike_sorting_kilosort4(recording, output_dir="results/spike_sorting"):
 """
 Kilosort4 by/via。

 SpikeInterface wrapper for。
 """
 import os
 os.makedirs(output_dir, exist_ok=True)

 sorting = si.run_sorter(
 sorter_name="kilosort4",
 recording=recording,
 output_folder=output_dir,
 verbose=True,
 )

 print(f" Kilosort4 results:")
 print(f" Units found: {len(sorting.get_unit_ids)}")

 return sorting


def spike_sorting_quality_metrics(sorting, recording,
 output_dir="results/spike_sorting"):
 """
 。

 ENCODE/Allen Institute criteria:
 - SNR ≥ 5: 
 - ISI violation rate < 0.5%: min
 - Presence ratio > 0.9: 
 - Amplitude cutoff < 0.1
 """
 we = si.extract_waveforms(recording, sorting, folder=f"{output_dir}/waveforms")
 metrics = si.compute_quality_metrics(we)

 # Allen Institute criteriafilter
 good_units = metrics[
 (metrics["snr"] >= 5) &
 (metrics["isi_violations_ratio"] < 0.005) &
 (metrics["presence_ratio"] > 0.9) &
 (metrics["amplitude_cutoff"] < 0.1)
 ]

 print(f" Quality metrics computed for {len(metrics)} units")
 print(f" Good units (Allen criteria): {len(good_units)} / {len(metrics)}")
 print(f" Mean SNR: {metrics['snr'].mean:.1f}")
 print(f" Mean ISI violation rate: {metrics['isi_violations_ratio'].mean:.4f}")
 print(f" Mean firing rate: {metrics['firing_rate'].mean:.1f} Hz")

 return metrics, good_units
```

## 2. EEG analysis (MNE-Python)

```python
import numpy as np
import mne


def eeg_preprocessing(raw_file, montage="standard_1020",
 l_freq=1.0, h_freq=40.0):
 """
 EEG preprocessingpipeline (MNE-Python)。

 1. fileload (BDF/EDF/FIF/BrainVision)
 2. settings
 3. filter (1-40 Hz)
 4. ICA by/via (, )
 5. reference (meanreference)
 """
 raw = mne.io.read_raw(raw_file, preload=True)
 raw.set_montage(montage)

 print(f" Channels: {len(raw.ch_names)}")
 print(f" Sampling rate: {raw.info['sfreq']} Hz")
 print(f" Duration: {raw.times[-1]:.1f} sec")

 # filter
 raw.filter(l_freq=l_freq, h_freq=h_freq, fir_design="firwin")

 # ICA 
 ica = mne.preprocessing.ICA(n_components=20, random_state=42)
 ica.fit(raw)

 # EOG/ECG componentautomated
 eog_indices, eog_scores = ica.find_bads_eog(raw)
 ica.exclude = eog_indices
 raw_clean = ica.apply(raw.copy)

 print(f" ICA components excluded: {len(eog_indices)} (EOG artifacts)")

 # meanreference
 raw_clean.set_eeg_reference("average")

 return raw_clean


def eeg_erp_analysis(raw, events, event_id, tmin=-0.2, tmax=0.8,
 baseline=(-0.2, 0)):
 """
 (ERP) analysis。

 Parameters:
 events: MNE events sequence
 event_id: (e.g., {"target": 1, "standard": 2})
 """
 epochs = mne.Epochs(raw, events, event_id,
 tmin=tmin, tmax=tmax,
 baseline=baseline,
 reject=dict(eeg=100e-6),
 preload=True)

 print(f" Epochs: {len(epochs)} / {len(events)} (after rejection)")

 evokeds = {}
 for condition in event_id:
 evoked = epochs[condition].average
 evokeds[condition] = evoked

 # peak
 ch_name, latency, amplitude = evoked.get_peak(
 ch_type="eeg", tmin=0.05, tmax=0.5
 )
 print(f" {condition}: peak at {latency*1000:.0f} ms, "
 f"{amplitude*1e6:.1f} µV ({ch_name})")

 return epochs, evokeds


def eeg_microstate_analysis(raw, n_states=4):
 """
 EEG analysis。

 brain's status (4-7 A-G) GFP peakfrom。
 each's frequencytimerate 。
 """
 from sklearn.cluster import KMeans

 # GFP (Global Field Power) calculation
 data = raw.get_data(picks="eeg")
 gfp = np.std(data, axis=0)

 # GFP peakextraction
 from scipy.signal import find_peaks
 peaks, _ = find_peaks(gfp, height=np.percentile(gfp, 50))

 # K-means clustering
 peak_maps = data[:, peaks].T
 kmeans = KMeans(n_clusters=n_states, random_state=42, n_init=50)
 labels = kmeans.fit_predict(peak_maps)

 # each's
 print(f" Microstate analysis ({n_states} states):")
 for i in range(n_states):
 ms_label = chr(65 + i) # A, B, C, D,...
 count = np.sum(labels == i)
 pct = count / len(labels)
 print(f" State {ms_label}: {pct:.1%} occurrence")

 return kmeans, labels
```

## 3. ECG analysis (NeuroKit2)

```python
import numpy as np
import pandas as pd
import neurokit2 as nk


def ecg_hrv_analysis(ecg_signal, sampling_rate=1000):
 """
 ECG from's (HRV) analysispipeline。

 1. R peak
 2. RR interval
 3. time HRV (SDNN, RMSSD, pNN50)
 4. frequency HRV (VLF, LF, HF, LF/HF )
 5. lineshape HRV (SD1, SD2, ApEn, SampEn)
 """
 # ECG preprocessing + R peak
 ecg_cleaned = nk.ecg_clean(ecg_signal, sampling_rate=sampling_rate)
 signals, info = nk.ecg_process(ecg_cleaned, sampling_rate=sampling_rate)

 r_peaks = info["ECG_R_Peaks"]
 print(f" R-peaks detected: {len(r_peaks)}")
 print(f" Mean HR: {signals['ECG_Rate'].mean:.1f} bpm")

 # HRV analysis (time + frequency + lineshape)
 hrv_time = nk.hrv_time(signals, sampling_rate=sampling_rate)
 hrv_freq = nk.hrv_frequency(signals, sampling_rate=sampling_rate)
 hrv_nonlinear = nk.hrv_nonlinear(signals, sampling_rate=sampling_rate)

 hrv_results = pd.concat([hrv_time, hrv_freq, hrv_nonlinear], axis=1)

 print(f" Time-domain HRV:")
 print(f" SDNN: {hrv_results['HRV_SDNN'].values[0]:.1f} ms")
 print(f" RMSSD: {hrv_results['HRV_RMSSD'].values[0]:.1f} ms")
 print(f" pNN50: {hrv_results['HRV_pNN50'].values[0]:.1f}%")
 print(f" Frequency-domain HRV:")
 print(f" LF/HF ratio: {hrv_results['HRV_LFHF'].values[0]:.2f}")

 return hrv_results, signals


def eda_sympathetic_analysis(eda_signal, sampling_rate=1000):
 """
 EDA  analysis — neural/nervesystem。

 1. min (Skin Conductance Level, SCL) min
 2. min (Skin Conductance Response, SCR) 
 3. SCR peakamplitudetimestime
 """
 eda_cleaned = nk.eda_clean(eda_signal, sampling_rate=sampling_rate)
 signals, info = nk.eda_process(eda_cleaned, sampling_rate=sampling_rate)

 scr_peaks = info["SCR_Peaks"]
 print(f" SCR peaks detected: {len(scr_peaks)}")
 print(f" Mean SCL (tonic): {signals['EDA_Tonic'].mean:.3f} µS")
 if len(scr_peaks) > 0:
 print(f" Mean SCR amplitude: {signals['SCR_Amplitude'].dropna.mean:.3f} µS")

 return signals, info
```

## 4. brainbindinganalysis

```python
import numpy as np
import pandas as pd


def functional_connectivity(epochs, method="wpli2_debiased",
 fmin=8, fmax=13):
 """
 EEG/MEG brainbinding's。

 Methods:
 - coh: Coherence
 - imcoh: Imaginary Coherence
 - plv: Phase Locking Value
 - wpli: Weighted Phase Lag Index
 - wpli2_debiased: Debiased Squared WPLI (recommended)
 """
 from mne_connectivity import spectral_connectivity_epochs

 con = spectral_connectivity_epochs(
 epochs, method=method,
 fmin=fmin, fmax=fmax,
 faverage=True, n_jobs=-1
 )

 conn_matrix = con.get_data(output="dense")[:, :, 0]

 print(f" Connectivity method: {method}")
 print(f" Frequency band: {fmin}-{fmax} Hz")
 print(f" Matrix shape: {conn_matrix.shape}")
 print(f" Mean connectivity: {np.mean(conn_matrix[np.triu_indices_from(conn_matrix, k=1)]):.3f}")

 return conn_matrix, con


def graph_theory_brain_network(conn_matrix, ch_names, threshold=0.3):
 """
 brainnetwork's graphanalysis。

 - Global efficiency
 - Clustering coefficient
 - Small-world index
 - Hub (degree centrality)
 """
 import networkx as nx

 n = conn_matrix.shape[0]
 G = nx.Graph
 for i in range(n):
 G.add_node(ch_names[i])
 for j in range(i + 1, n):
 if conn_matrix[i, j] > threshold:
 G.add_edge(ch_names[i], ch_names[j],
 weight=conn_matrix[i, j])

 # graph
 eff = nx.global_efficiency(G)
 cc = nx.average_clustering(G, weight="weight")
 degree = dict(G.degree(weight="weight"))
 top_hubs = sorted(degree.items, key=lambda x: x[1], reverse=True)[:5]

 print(f" Brain network: {G.number_of_nodes} nodes, {G.number_of_edges} edges")
 print(f" Global efficiency: {eff:.3f}")
 print(f" Clustering coefficient: {cc:.3f}")
 print(f" Top hubs: {[h[0] for h in top_hubs]}")

 return G
```

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `biotools` | bio.tools | analysistoolsearch |

## References

### Output Files

| File | Format |
|---|---|
| `results/spike_sorting/sorting_results.npz` | NPZ |
| `results/spike_sorting/quality_metrics.csv` | CSV |
| `results/eeg/erp_evokeds.fif` | FIF |
| `results/eeg/microstates.csv` | CSV |
| `results/ecg/hrv_results.csv` | CSV |
| `results/eda/scr_peaks.csv` | CSV |
| `results/connectivity/conn_matrix.csv` | CSV |
| `figures/spike_rasters.png` | PNG |
| `figures/erp_waveforms.png` | PNG |
| `figures/hrv_poincare.png` | PNG |

### Related Skills

| Skill | Relationship |
|---|---|
| `scientific-biosignal-processing` | fororganism |
| `scientific-spectral-signal` | spectrumfrequencyanalysis |
| `scientific-time-series` | time seriesdegradationprediction |
| `scientific-network-analysis` | graphnetwork |
| `scientific-deep-learning` | DL classification |

### Dependencies

`spikeinterface`, `mne`, `mne-connectivity`, `neurokit2`, `numpy`, `pandas`, `scipy`, `scikit-learn`, `networkx`
