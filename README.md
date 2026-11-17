# BrewDz Particle Engineering — Perfect Coffee Powder
**Course:** ChE 303: Fluid Particle Systems  
**Project:** Build Your Own Engineering Startup (Project 4: Engineering the Perfect Coffee Powder)  
**Institution:** Chemical Engineering Department  

---

## ☕ Overview

**BrewDz Particle Engineering Pvt. Ltd.** is an engineering startup concept designed to solve the fundamental flaw in commercial coffee processing: **polydisperse particle size distributions (PSD)**.

In coffee extraction, particle size dictates packed-bed permeability ($\Delta P / L$ via the **Ergun Equation**) and solid-liquid extraction kinetics:
- **"Boulders" (> 1000 µm):** Under-extract due to long internal diffusion pathways, causing sourness.
- **"Fines" (< 100 µm):** Blind bed filter pores, causing severe hydraulic resistance and channel flow, leaching bitter chlorogenic acids.

BrewDz implements a closed-loop comminution and classification circuit with **low-shear chilled roller milling**, **vibratory screen classification**, and an **automated oversize recycle loop** that boosts on-spec product yield to **>96%**.

---

## 📁 Repository Structure

The project is organized into modular folders for documentation, python modeling, simulation datasets, and the web platform:

```text
Brewdz-ChE-303/
├── .gitignore
├── README.md                         # Complete project documentation & setup
├── index.html                        # GitHub Pages root redirect to frontend/
│
├── Aspen/                            # Aspen Plus V14 Raw Simulation Results (Charan's Runs)
│   ├── run_1.xlsx ... run_6.xlsx     # Open-loop single-pass grinding cases
│   └── mix_1.xlsx ... mix_6.xlsx     # Closed-loop converged cases with oversize recycle
│
├── frontend/                         # Interactive Web Application & Simulation Dashboard
│   ├── index.html                    # Main web portal (Fraunces typography & warm paper theme)
│   ├── app.js                        # Bilinear interpolation engine, Angle of Nip & Chart.js
│   ├── style.css                     # Responsive CSS layout & styling
│   ├── simulation_data.js            # Precomputed 399-case simulation database
│   └── simulation_dataset.csv        # Downloadable parametric CSV dataset
│
├── simulation/                       # Python Computational Modeling & Aspen Solids Circuits
│   ├── coffee_particle_calc.py       # Double Roll Crusher calculations, Angle of Nip & Bond hand-check
│   ├── generate_simulation_dataset.py# Aspen-equivalent steady-state parametric dataset generator
│   └── parse_aspen_runs.py           # Automated parser for Aspen Excel stream results
│
├── data/                             # Raw & Parametric Simulation Data
│   └── simulation_dataset.csv        # 399-case comprehensive simulation dataset
│
└── docs/                             # Deliverables, Course Guidelines & Defense Materials
    ├── ASPEN_SIMULATION_REPORT.md    # In-depth analysis of Aspen Plus V14 flowsheet & runs
    ├── aspen_screenshots/            # Aspen Plus V14 GUI screenshots (flowsheet, feed, PSD)
    ├── ChE 303_Project.pdf           # Official course project guidelines
    ├── COMPETITOR_STUDY_DETAILED.md  # Detailed 5-competitor Indore & pan-India benchmark
    ├── PRESENTATION_SLIDES_DRAFT.md  # 8-slide final presentation deck & viva defense Q&A
    └── PROJECT_MASTER_GUIDELINES.md  # Master engineering execution manual
```

---

## 🚀 Key Deliverables & Execution

### 1. Equipment Calculations & Hand Verification (`simulation/coffee_particle_calc.py`)
- **Double Roll Crusher Angle of Nip ($\alpha$):** Evaluates $\cos(\alpha/2) = \frac{D_R + s}{D_R + D_p}$ and verifies zero-slip gripping ($\tan(\alpha/2) \le \mu = 0.32$).
- **Crusher Mass Capacity:** Computes theoretical and practical capacity ($Q_{\text{practical}} = 60\pi D_R W_R N s \rho_{\text{bulk}}\eta_v$).
- **Bond's Comminution Law:** Calculates comminution power across feed rates and product sizes ($d_{80}$).
- **Screen Separation Effectiveness ($E$):** Evaluates oversize ($E_O$) and undersize ($E_U$) recoveries.
- **Ergun Equation:** Evaluates packed-bed hydraulic resistance during coffee extraction.
- **Analytical Benchmark:** Matches hand calculations at $0.0000000000$ error.

Run verification:
```bash
python simulation/coffee_particle_calc.py
```

### 2. Parametric Simulation Dataset (`data/simulation_dataset.csv`)
- Parametric dataset across feed rates ($50\text{--}500\,\text{kg/h}$), screen apertures ($550\text{--}850\,\mu\text{m}$), and three brewing profiles:
  - **Espresso:** $d_{50} = 250\,\mu\text{m}$, roller gap $= 0.25\,\text{mm}$
  - **Drip / Pour-Over:** $d_{50} = 550\,\mu\text{m}$, roller gap $= 0.55\,\text{mm}$
  - **French Press / Cold Brew:** $d_{50} = 950\,\mu\text{m}$, roller gap $= 0.95\,\text{mm}$

Regenerate dataset:
```bash
python simulation/generate_simulation_dataset.py
```

### 3. Interactive Web Application (`frontend/index.html`)
- **Live Deployment:** [https://rishan-code.github.io/Brewdz-ChE-303/](https://rishan-code.github.io/Brewdz-ChE-303/)
- **Zero Aspen Live Dependency:** Runs standalone in modern web browsers.
- **Interactive PFD:** Animated SVG flowsheet with dynamic stream telemetry.
- **Live Engineering Calculator:** Sliders for feed rate (mass flow), feed bean size ($d_{50}$), feed span, and screen mesh aperture with real-time bilinear dataset interpolation.
- **Double Roll Crusher Readouts:** Live Angle of Nip status badge (`✓ PASS (≤ 35.5°)`), practical capacity, and full product PSD percentiles ($d_{10}, d_{50}, d_{80}, d_{90}$, span).
- **Competitor Benchmark:** Detailed landscape analysis covering Indore/MP and Pan-India competitors.

Open in browser locally:
```bash
python -m http.server 8000
```
Then navigate to `http://localhost:8000`.

---

## 📊 8-Slide Evaluation Presentation Guide
See [docs/PRESENTATION_SLIDES_DRAFT.md](docs/PRESENTATION_SLIDES_DRAFT.md) for complete slide-by-slide bullet points, talking points, and anticipated faculty viva defense Q&A.

---

## 👥 Authors
* **Charan:** Process Simulation Lead (*Aspen Plus Flowsheet, Solids Circuit Design, Recycle Convergence*)
* **Rishan:** Computational Modelling Lead (*Double Roll Crusher Mechanics, Angle of Nip, Bond Verification*)
* **Sohil Thakur:** Web & Data Lead (*Interactive Engineering Portal, Simulation Dataset Interpolation, SVG Flowsheet*)
* **ChE 303 Team:** Systems & Market Analysis (*Indore Competitor Benchmarking, Ergun Bed Hydraulics, Technical Defense*)

