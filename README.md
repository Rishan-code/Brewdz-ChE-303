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

```text
├── ChE 303_Project.pdf               # Official course project guidelines
├── PROJECT_MASTER_GUIDELINES.md      # Detailed master execution manual & technical guide
├── PRESENTATION_SLIDES_DRAFT.md      # 8-slide final evaluation presentation & viva Q&A
├── coffee_particle_calc.py           # Python calculations (Bond's Law, Screen Eff., Ergun Eq.) + Hand Verification
├── generate_simulation_dataset.py    # Aspen Plus parametric simulation data generator
├── simulation_dataset.csv            # 57 precomputed simulation cases
├── index.html                        # Standalone interactive web portal & simulation viewer
├── style.css                         # Web app styling (specialty coffee + engineering theme)
├── app.js                            # Interactive calculator, CSV interpolation & Chart.js engine
├── .gitignore                        # Git ignore rules
└── README.md                         # Project documentation
```

---

## 🚀 Key Features

### 1. Equipment Calculations & Hand Verification (`coffee_particle_calc.py`)
- **Bond's Comminution Law:** Calculates roller mill power across varying feed rates and product sizes ($d_{80}$).
- **Screen Separation Effectiveness ($E$):** Evaluates oversize ($E_O$) and undersize ($E_U$) recoveries.
- **Ergun Equation:** Models pressure drop across the packed bed during fluid percolation.
- **Analytical Benchmark:** Validates Python outputs against step-by-step hand calculations ($100\%$ match).

Run verification:
```bash
python coffee_particle_calc.py
```

### 2. Parametric Simulation Dataset (`simulation_dataset.csv`)
- 57 simulation cases across feed rates ($50\text{--}500\,\text{kg/h}$) and three brewing modes:
  - **Espresso:** $d_{50} = 250\,\mu\text{m}$, roller gap $= 0.25\,\text{mm}$
  - **Drip / Pour-Over:** $d_{50} = 550\,\mu\text{m}$, roller gap $= 0.55\,\text{mm}$
  - **French Press / Cold Brew:** $d_{50} = 950\,\mu\text{m}$, roller gap $= 0.95\,\text{mm}$

Regenerate dataset:
```bash
python generate_simulation_dataset.py
```

### 3. Interactive Web Application (`index.html`)
- **Zero Aspen Live Dependency:** Runs standalone in any browser.
- **Interactive PFD:** Animated SVG flowsheet with dynamic stream telemetry.
- **Live Engineering Calculator:** Sliders for feed rate, grind preset, and screen mesh with real-time dataset interpolation.
- **Dynamic Charts (Chart.js):** Power vs. feed rate curves and PSD distribution comparison.
- **Competitor Benchmark:** Detailed landscape analysis covering Indore and Pan-India competitors.

Open in browser:
Simply double-click `index.html` or run:
```bash
python -m http.server 8000
```
Then navigate to `http://localhost:8000`.

---

## 📊 8-Slide Evaluation Presentation Guide
See [PRESENTATION_SLIDES_DRAFT.md](PRESENTATION_SLIDES_DRAFT.md) for complete slide-by-slide bullet points, talking points, and anticipated faculty viva defense Q&A.

---

## 👥 Authors
* **Course:** ChE 303 — Fluid Particle Systems
* **Team:** BrewDz Engineering Group

