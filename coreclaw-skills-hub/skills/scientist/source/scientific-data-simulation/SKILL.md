---
name: scientific-data-simulation
description: |
 -basedsynthesisdatageneration's skill。experimentdata、
 simulationdata is generatedfor。
 Scientific Skills Exp-06, 07, 08, 09, 12, 13 。
tu_tools:
 - key: biotools
 name: bio.tools
 description: simulationTool Registry Search
---

# Scientific Data Simulation & Generation

method 、simulationdata
generatesskill。data's、ML pipeline's verification possible.

## When to Use

- experimentData Retrievalormin and
- ML pipeline'ssynthesisdatawhen needed
- 's method-baseddatageneration
- known's data's

## Quick Start

## designprinciples

1. ****: normal distribution、's
2. **'s**: experiment's uncertainty
3. **/group's**: multiple's typecondition generation、group
4. **range's**: parametersrange experimentlimitations-based

## datagenerationtemplate

### 1. processdatageneration（Exp-12, 13 ）

```python
import numpy as np
import pandas as pd

def generate_process_dataset(n_samples=500, seed=42):
 """
 'sprocessdata is generatedtemplate。
 : Process → Structure → Property
 """
 rng = np.random.default_rng(seed)

 # === Process parameters（number/count）===
 temperature = rng.uniform(25, 500, n_samples) # °C
 pressure = rng.uniform(0.1, 5.0, n_samples) # Pa
 power = rng.uniform(50, 500, n_samples) # W
 time = rng.uniform(5, 120, n_samples) # min

 # === Structure number/count（Process dependency）===
 # ：
 dep_rate = (
 0.5
 + 0.02 * power # outputdependency
 - 0.005 * pressure ** 2 # 's
 + rng.normal(0, 0.5, n_samples) # 
 )
 dep_rate = np.clip(dep_rate, 0.1, 30)

 thickness = dep_rate * time
 thickness = np.clip(thickness, 5, 2000)

 crystallite_size = (
 5
 + 0.1 * temperature # temperaturedependency（）
 + 0.01 * time # timedependency
 + rng.normal(0, 2, n_samples) # 
 )
 crystallite_size = np.clip(crystallite_size, 2, 80)

 # === Property number/count（Structure dependency）===
 resistivity = (
 1e-2
 * np.exp(-0.005 * temperature) # temperatureactivation
 * (1 + 0.01 * pressure)
 * np.exp(rng.normal(0, 0.3, n_samples)) # number/count
 )

 transmittance = (
 95
 - 0.02 * thickness # dependency
 + 0.05 * crystallite_size # crystaldependency
 + rng.normal(0, 1, n_samples)
 )
 transmittance = np.clip(transmittance, 40, 98)

 df = pd.DataFrame({
 "Temperature": temperature,
 "Pressure": pressure,
 "Power": power,
 "Time": time,
 "Deposition_Rate": dep_rate,
 "Thickness": thickness,
 "Crystallite_Size": crystallite_size,
 "Resistivity": resistivity,
 "Transmittance": transmittance,
 })

 return df
```

### 2. datageneration（Exp-13 ）

```python
def generate_multi_material_dataset(materials, n_per_material=100, seed=42):
 """
 multiple's PSP data is generated。
 materials: {"ZnO": {"Tm": 2248, "Eg": 3.3},...} 's
 """
 rng = np.random.default_rng(seed)
 all_data = []

 for mat_name, props in materials.items:
 n = n_per_material
 Tm = props["Tm"] # point (K)
 Eg = props["Eg"] # band gap (eV)

 # Process
 Tsub = rng.uniform(25, 500, n)
 Pwork = rng.uniform(0.1, 5.0, n)
 Power = rng.uniform(50, 500, n)

 # Structure（dependency's）
 T_homologous = (Tsub + 273.15) / Tm # phasetemperature
 crystallite = 5 + 80 * T_homologous + rng.normal(0, 3, n)
 crystallite = np.clip(crystallite, 2, 80)

 # Property（value + processdependency）
 bandgap = Eg + rng.normal(0, 0.1, n)

 data = pd.DataFrame({
 "Material": mat_name,
 "Substrate_Temp": Tsub,
 "Working_Pressure": Pwork,
 "Power": Power,
 "T_homologous": T_homologous,
 "Crystallite_Size": crystallite,
 "Bandgap": bandgap,
 })
 all_data.append(data)

 return pd.concat(all_data, ignore_index=True)
```

### 3. clinical trialdatageneration（Exp-06 ）

```python
def generate_clinical_trial_data(n_total=500, effect_size=0.3, seed=42):
 """RCT simulationdata is generated。"""
 rng = np.random.default_rng(seed)
 n_per_arm = n_total // 2

 # 
 ages = np.concatenate([
 rng.normal(55, 12, n_per_arm),
 rng.normal(55, 12, n_per_arm),
 ])
 sex = rng.choice(["M", "F"], n_total)
 group = np.array(["Treatment"] * n_per_arm + ["Control"] * n_per_arm)

 # keyendpoint
 baseline = rng.normal(100, 15, n_total)
 treatment_effect = np.where(group == "Treatment", effect_size * 15, 0)
 endpoint = baseline + treatment_effect + rng.normal(0, 10, n_total)

 # time（number/countdistribution）
 survival_time = rng.exponential(
 np.where(group == "Treatment", 365 * 2, 365 * 1.5),
 n_total
 )
 event = rng.binomial(1, 0.7, n_total)

 return pd.DataFrame({
 "Patient_ID": range(1, n_total + 1),
 "Group": group,
 "Age": ages.astype(int),
 "Sex": sex,
 "Baseline": baseline,
 "Endpoint": endpoint,
 "Survival_Time": survival_time,
 "Event": event,
 })
```

### 4. spectrumdatageneration（Exp-08, 11 ）

```python
def generate_spectrum(wavenumbers, peak_positions, peak_heights,
 peak_widths, noise_level=0.02, seed=None):
 """
 peaksynthesisby/viaspectrum is generated。
 / IR / UV-Vis etc.for。
 """
 rng = np.random.default_rng(seed)
 spectrum = np.zeros_like(wavenumbers, dtype=float)

 for pos, height, width in zip(peak_positions, peak_heights, peak_widths):
 spectrum += height * np.exp(-0.5 * ((wavenumbers - pos) / width) ** 2)

 # 
 spectrum += rng.normal(0, noise_level * spectrum.max, len(wavenumbers))
 return spectrum


def generate_ecg_beat(t, hr=72):
 """synthesis ECG shape（PQRST ） is generated。"""
 beat_duration = 60.0 / hr
 # P 、QRS group、T 's
 p_wave = 0.1 * np.exp(-((t % beat_duration - 0.16) / 0.04) ** 2)
 qrs = 1.0 * np.exp(-((t % beat_duration - 0.25) / 0.01) ** 2)
 q_wave = -0.15 * np.exp(-((t % beat_duration - 0.22) / 0.015) ** 2)
 s_wave = -0.1 * np.exp(-((t % beat_duration - 0.28) / 0.015) ** 2)
 t_wave = 0.2 * np.exp(-((t % beat_duration - 0.40) / 0.05) ** 2)
 return p_wave + q_wave + qrs + s_wave + t_wave
```

## 

generationdata's foritem：

- [ ] parametersrange
- [ ] 's direction correct（temperature↑ → crystal↑ etc.）
- [ ] experiment's reproducibilitycorresponding
- [ ] value's ratio（ 1-5%）
- [ ] number/count's correlationstructure known's method and
- [ ] groupeffect sizeaspossiblelevels

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `biotools` | bio.tools | simulationTool Registry Search |

## References

### Output Files

| File | Format |
|---|---|
| `data/<dataset_name>.csv` | CSV |

#### Reference Experiments

- **Exp-06**: clinical trial RCT simulation（500 、2 group）
- **Exp-07**: synthesisdata（100 × 200 metabolite）
- **Exp-08**: synthesis ECG/EEG （PQRST、synthesis）
- **Exp-09**: genomesequence
- **Exp-12**: processdata（500 × 8 parameters）
- **Exp-13**: data（600 × 6 × PSP 3 ）
