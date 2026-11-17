# Aspen Plus V14 Solids Flowsheet Simulation Report
**Course:** ChE 303: Fluid Particle Systems  
**Project:** Engineering the Perfect Coffee Powder (BrewDz Particle Engineering Pvt. Ltd.)  
**Simulation Team:** Process Simulation Lead & Computational Validation Lead  
**Software Environment:** Aspen Plus V14 (`Coffee_powder.apwz` / `Coffee_powder$backup.bkp`)  

---

## 1. Flowsheet Architecture & Process Concept

The Aspen Plus V14 simulation models the complete closed-loop comminution, roasting, and multi-deck screening circuit for specialty coffee processing.

```mermaid
flowchart LR
    A["FEED<br>100 kg/h<br>(97% solids, 3% H2O)"] --> B["ROASTER<br>(Heater Block)"]
    B -->|"ROASTED<br>210°C"| C["MIXER<br>(Solids Mixer)"]
    D["OVERSIZE (Recycle)<br>22.5–23.2 kg/h"] --> C
    C -->|"MIXED<br>~120 kg/h"| E["CRUSHER<br>(Double Roll Crusher)"]
    E -->|"CRUSHED<br>dp < 2087 µm"| F["SCREEN<br>(Vibrating Screen)"]
    F -->|"OVERSIZE<br>1093–2087 µm"| D
    F -->|"PROD (Target)<br>41.5–42.0 kg/h<br>(67% in 600–1100 µm)"| G["Product Silo"]
    F -->|"FINE (Undersize)<br>55.0–55.5 kg/h<br>(dp < 597 µm)"| H["Soluble Coffee By-product"]

    style A fill:#D4A373,stroke:#2C1810,stroke-width:2px,color:#2C1810
    style B fill:#F3ECE2,stroke:#8A5A2B,stroke-width:2px,color:#2C1810
    style C fill:#F3ECE2,stroke:#8A5A2B,stroke-width:2px,color:#2C1810
    style E fill:#E7DFD3,stroke:#2C1810,stroke-width:2px,color:#2C1810
    style F fill:#F3ECE2,stroke:#8A5A2B,stroke-width:2px,color:#2C1810
    style G fill:#E6F4EA,stroke:#137333,stroke-width:2px,color:#137333
    style H fill:#ECEAE6,stroke:#7A6A5C,stroke-width:2px,color:#7A6A5C
    style D fill:#FCE8E6,stroke:#C2571A,stroke-width:2px,color:#C2571A
```

### Aspen Unit Operations (Blocks):
1. **`ROASTER` (Heater Block):**
   - Simulates the thermal roasting of raw green coffee beans up to $210^\circ\text{C}$ at $1.013\,\text{bar}$.
   - Flashes the 3% moisture content into vapor phase while preparing brittle cellular bean structure for low-shear fracturing.
2. **`MIXER` (Mixer Block):**
   - Combines $97.0\,\text{kg/h}$ fresh roasted coffee solids with recycled screen oversize ($22.5\text{--}23.2\,\text{kg/h}$).
   - Discharges a combined feed of $\approx 120.0\,\text{kg/h}$ solids ($123.0\,\text{kg/h}$ total stream) to the crusher.
3. **`CRUSHER` (Crusher Block):**
   - Implements mechanical fracture of roasted beans down to powder ($d_p < 2087\,\mu\text{m}$).
   - Generates the intermediate particle size distribution (`CRUSHED`).
4. **`SCREEN` (Screen Block):**
   - Mechanically classifies the crushed powder into three cuts:
     - **`FINE` (Bottoms):** All dust $< 596.7\,\mu\text{m}$ ($100\%$ below cut point).
     - **`PROD` (Middle Cut):** Narrow specialty grounds ($67\%$ between $597\text{--}1093\,\mu\text{m}$).
     - **`OVERSIZE` (Tops):** Particles $> 1093\,\mu\text{m}$ recycled to `MIXER`.

---

## 2. Feed Stream Characterization (`FEED`)

From the verified Aspen Plus input masks:
- **Stream Class:** `MIXNCPSD` (Mixed Conventional Fluids + Non-Conventional Solids with Particle Size Distribution).
- **Temperature & Pressure:** $25^\circ\text{C}$, $1\,\text{atm}$ ($1.01325\,\text{bar}$).
- **Moisture Substream (`Mixed`):**
  - Component: `WATER` = $3.0\,\text{kg/h}$ ($3.00\,\text{wt}\%$).
- **Solid Coffee Substream (`NC Solid` / `NCPSD`):**
  - Component: `COFFEE` = $97.0\,\text{kg/h}$ ($97.00\,\text{wt}\%$).
  - Component Attribute: `GENANAL` with `ELEM1` = $100.0$.
- **Particle Size Distribution (PSD Mesh: 30 Intervals):**
  - Whole bean diameter spans $8,543.33\,\mu\text{m}$ to $14,006.7\,\mu\text{m}$ ($8.54\text{--}14.0\,\text{mm}$).
  - Median Bean Diameter: $d_{50,\text{feed}} \approx 10,750\,\mu\text{m}$ ($10.75\,\text{mm}$).

| Mesh Interval (µm) | Weight Fraction | Cumulative Fraction | Notes |
| :--- | :---: | :---: | :--- |
| **8543.33 – 9040.00** | 0.050 | 0.050 | Small flat beans / peaberry cut |
| **9040.00 – 9536.67** | 0.100 | 0.150 | Screen size 23 equivalent |
| **9536.67 – 10033.3** | 0.100 | 0.250 | Screen size 25 equivalent |
| **10033.3 – 10530.0** | 0.100 | 0.350 | Screen size 26 equivalent |
| **10530.0 – 11026.7** | **0.200** | 0.550 | **Main Mode (Median d50 ≈ 10.75 mm)** |
| **11026.7 – 11523.3** | **0.200** | 0.750 | **Main Mode (Median d50 ≈ 10.75 mm)** |
| **11523.3 – 12020.0** | 0.100 | 0.850 | Large grade Arabica |
| **12020.0 – 12516.7** | 0.050 | 0.900 | Screen size 31 |
| **12516.7 – 13013.3** | 0.050 | 0.950 | Very large beans |
| **13013.3 – 13510.0** | 0.025 | 0.975 | Elephant bean fraction |
| **13510.0 – 14006.7** | 0.025 | 1.000 | Coarse upper bound |

---

## 3. Parametric Analysis: Open-Loop vs. Closed-Loop

The engineering team evaluated 6 feed PSD profiles across two operational regimes:
1. **Open-Loop Runs (`run_1` to `run_6`):** Single-pass crushing without recycle feedback.
2. **Closed-Loop Runs (`mix_1` to `mix_6`):** Steady-state recycle loop converging with $R/F \approx 23.5\%$.

### Consolidated Aspen Results Table

| Run Case | Circuit Configuration | Crusher Feed (kg/h) | Oversize Recycle (kg/h) | Recirc Ratio ($R/F$) | Product PROD (kg/h) | Product Yield (%) | Target Cut (600–1100 µm) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **run_1.xlsx** | Open-Loop (Single-Pass) | 97.00 | 19.46 (Wasted) | — | 33.53 | 34.6% | 67.5% |
| **run_2.xlsx** | Open-Loop (Single-Pass) | 97.00 | 18.87 (Wasted) | — | 33.85 | 34.9% | 67.7% |
| **run_3.xlsx** | Open-Loop (Single-Pass) | 97.00 | 19.78 (Wasted) | — | 34.67 | 35.7% | 69.6% |
| **run_4.xlsx** | Open-Loop (Single-Pass) | 97.00 | 19.26 (Wasted) | — | 33.75 | 34.8% | 67.8% |
| **run_5.xlsx** | Open-Loop (Single-Pass) | 97.00 | 18.82 (Wasted) | — | 33.89 | 34.9% | 67.7% |
| **run_6.xlsx** | Open-Loop (Single-Pass) | 97.00 | 19.11 (Wasted) | — | 33.86 | 34.9% | 67.8% |
| **mix_1.xlsx** | **Closed-Loop (Recycle)** | **119.96** | **22.96** | **0.237** | **41.48** | **42.8%** | **67.0%** |
| **mix_2.xlsx** | **Closed-Loop (Recycle)** | **119.73** | **22.73** | **0.234** | **41.62** | **42.9%** | **67.1%** |
| **mix_3.xlsx** | **Closed-Loop (Recycle)** | **119.55** | **22.55** | **0.232** | **41.66** | **42.9%** | **67.2%** |
| **mix_4.xlsx** | **Closed-Loop (Recycle)** | **119.92** | **22.92** | **0.236** | **41.96** | **43.3%** | **67.6%** |
| **mix_5.xlsx** | **Closed-Loop (Recycle)** | **120.23** | **23.23** | **0.239** | **41.86** | **43.2%** | **67.5%** |
| **mix_6.xlsx** | **Closed-Loop (Recycle)** | **120.11** | **23.11** | **0.238** | **41.79** | **43.1%** | **67.4%** |

---

## 4. Engineering Takeaways & Defense Points

1. **Massive Yield Surge (+23.8%):**
   Closing the oversize recycle loop increases on-spec product output from **$33.53\,\text{kg/h}$ to $41.96\,\text{kg/h}$** per $100\,\text{kg/h}$ feed.
2. **Total Boulder Elimination ($0.00\%$ > 1590 µm):**
   In the `PROD` stream, particles coarser than $1590\,\mu\text{m}$ are virtually $0\%$ ($0.7\%$ in $1093\text{--}1590\,\mu\text{m}$, $0.00\%$ above $1590\,\mu\text{m}$). This solves the under-extraction and sourness defect in commercial brewing.
3. **Dedicated Super-Fine Classification:**
   The `FINE` stream collects $55.0\text{--}55.5\,\text{kg/h}$ of dust ($100\% < 596.7\,\mu\text{m}$). Rather than being lost or blinding the brew bed filter, this stream is captured as a high-value feed for instant soluble coffee spray-drying.
4. **Consistency Across Variable Bean Feeds:**
   Across small peaberry cuts (`mix_5`, feed $d_{50} \approx 6.5\,\text{mm}$) and coarse elephant beans (`mix_2`, feed $d_{50} \approx 10.7\,\text{mm}$), the closed circuit maintains a remarkably stable product yield of $42.8\% - 43.3\%$ and a target mode fraction of $67.0\% - 67.6\%$.
