/**
 * BrewDz Particle Engineering - Web Application Script
 * ChE 303: Fluid Particle Systems
 * 
 * Implements Charan's Deliverable Specifications:
 *  - Primary Inputs: Mass Flow Rate (kg/h), Feed Bean Size Distribution (d50 & Span), Roll Gap (s)
 *  - Primary Output: Crushed Product Size Distribution (PSD), Percentiles (d10, d50, d80, d90),
 *    Double Roll Crusher Angle of Nip (alpha), Capacity, and Comminution Power (Bond's Law).
 */

// Double Roll Crusher Mechanical Specifications
const CRUSHER_SPECS = {
    rollDiameter_mm: 250.0,   // D_R = 250 mm (R = 125 mm)
    rollWidth_mm: 300.0,      // W_R = 300 mm
    rpm: 220.0,               // N = 220 RPM
    frictionCoeff: 0.32,      // mu for steel rolls vs roasted bean
    bondWorkIndex: 12.5,      // Wi (kWh/tonne)
    bulkDensity_kgm3: 400.0,  // rho_bulk
    packingFactor: 0.28       // eta_v volumetric packing
};

// Error function approximation for log-normal distribution
function erf(x) {
    const a1 =  0.254829592;
    const a2 = -0.284496736;
    const a3 =  1.421413741;
    const a4 = -1.453152027;
    const a5 =  1.061405429;
    const p  =  0.3275911;

    const sign = x < 0 ? -1 : 1;
    const absX = Math.abs(x);
    const t = 1.0 / (1.0 + p * absX);
    const y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-absX * absX);
    return sign * y;
}

// Transform Feed PSD into Product PSD via Double Roll Crusher Mechanics
function calculateDoubleRollCrusher(feedRate_kgh, feedD50_mm, feedSpan, rollGap_mm) {
    const R = CRUSHER_SPECS.rollDiameter_mm / 2.0;
    const r = rollGap_mm / 2.0;
    const feedD50_um = feedD50_mm * 1000.0;
    const feedDmax_mm = feedD50_mm * 1.35; // Maximum bean in feed
    const rollGap_um = rollGap_mm * 1000.0;

    // 1. ANGLE OF NIP & GRIPPING CRITERION
    const cosTheta = (R + r) / (R + feedDmax_mm / 2.0);
    const thetaRad = Math.acos(Math.min(1.0, Math.max(-1.0, cosTheta)));
    const thetaDeg = thetaRad * (180.0 / Math.PI);
    const alphaDeg = 2.0 * thetaDeg;

    const thetaMaxRad = Math.atan(CRUSHER_SPECS.frictionCoeff);
    const alphaMaxDeg = 2.0 * thetaMaxRad * (180.0 / Math.PI);
    const isGripped = alphaDeg <= alphaMaxDeg;

    // 2. CAPACITY (PRACTICAL THROUGHPUT)
    const D_m = CRUSHER_SPECS.rollDiameter_mm * 1e-3;
    const W_m = CRUSHER_SPECS.rollWidth_mm * 1e-3;
    const s_m = rollGap_mm * 1e-3;
    const vSurface = Math.PI * D_m * (CRUSHER_SPECS.rpm / 60.0);
    const Q_vol_ideal = W_m * s_m * vSurface * 3600.0; // m3/h
    const Q_mass_ideal = Q_vol_ideal * CRUSHER_SPECS.bulkDensity_kgm3;
    const practicalCapacity_kgh = Q_mass_ideal * CRUSHER_SPECS.packingFactor;
    const loadPct = (feedRate_kgh / practicalCapacity_kgh) * 100.0;

    // 3. PRODUCT SIZE DISTRIBUTION PERCENTILES
    const prodD50_um = rollGap_um * 0.72;
    const prodD80_um = rollGap_um * 1.15;
    const sigmaProd = 0.42;
    const prodD10_um = prodD50_um * Math.exp(-1.28155 * sigmaProd);
    const prodD90_um = prodD50_um * Math.exp(1.28155 * sigmaProd);
    const prodSpan = (prodD90_um - prodD10_um) / prodD50_um;

    // 4. COMMINUTION POWER (BOND'S LAW)
    const sigmaFeed = Math.max(0.2, feedSpan * 0.35);
    const feedD80_um = feedD50_um * Math.exp(0.8416 * sigmaFeed);
    const m_dot_tph = feedRate_kgh / 1000.0;
    const termProd = 1.0 / Math.sqrt(prodD80_um);
    const termFeed = 1.0 / Math.sqrt(feedD80_um);
    const specE_ton = 10.0 * CRUSHER_SPECS.bondWorkIndex * (termProd - termFeed);
    const specE_kg = specE_ton / 1000.0;
    const power_kw = m_dot_tph * specE_ton;

    // 5. ERGUN EXTRACTION PRESSURE DROP
    const dp_m = prodD50_um * 1e-6;
    const eps = 0.42;
    const u = 0.0018;
    const mu = 0.000306;
    const rho = 965.0;
    const L = 0.025; // 25 mm puck
    const viscous = 150.0 * Math.pow(1.0 - eps, 2) / Math.pow(eps, 3) * (mu * u / Math.pow(dp_m, 2));
    const inertial = 1.75 * (1.0 - eps) / Math.pow(eps, 3) * (rho * Math.pow(u, 2) / dp_m);
    const deltaP_kPa = ((viscous + inertial) * L) / 1000.0;

    // 6. GENERATE DISCRETE PSD CURVES FOR CHARTING
    // Grid from 50 µm to 10,000 µm
    const meshSizes = [50, 100, 200, 350, 500, 700, 1000, 1400, 2000, 3000, 5000, 6500, 8000, 10000];
    
    // Cumulative passing % for Feed
    const feedCum = meshSizes.map(s => {
        const z = (Math.log(s) - Math.log(feedD50_um)) / (sigmaFeed * Math.SQRT2);
        const cum = 0.5 * (1.0 + erf(z)) * 100.0;
        return Math.min(100.0, Math.max(0.0, cum));
    });

    // Cumulative passing % for Crushed Product
    const prodCum = meshSizes.map(s => {
        const z = (Math.log(s) - Math.log(prodD50_um)) / (sigmaProd * Math.SQRT2);
        const cum = 0.5 * (1.0 + erf(z)) * 100.0;
        return Math.min(100.0, Math.max(0.0, cum));
    });

    // Fines fraction (< 100 µm) and Boulders (> 1000 µm)
    const finesPct = prodCum[1]; // at 100 µm
    const bouldersPct = 100.0 - prodCum[6]; // at 1000 µm

    return {
        feedRate_kgh,
        feedD50_mm,
        feedD50_um,
        feedD80_um,
        feedSpan,
        rollGap_mm,
        alphaDeg,
        alphaMaxDeg,
        isGripped,
        practicalCapacity_kgh,
        loadPct,
        prodD10_um,
        prodD50_um,
        prodD80_um,
        prodD90_um,
        prodSpan,
        finesPct,
        bouldersPct,
        power_kw,
        specE_kg,
        deltaP_kPa,
        meshSizes,
        feedCum,
        prodCum
    };
}

// DOM Elements
const inputFeedRate = document.getElementById('input-feed-rate');
const valFeedRate = document.getElementById('val-feed-rate');
const inputFeedD50 = document.getElementById('input-feed-d50');
const valFeedD50 = document.getElementById('val-feed-d50');
const inputFeedSpan = document.getElementById('input-feed-span');
const valFeedSpan = document.getElementById('val-feed-span');
const inputRollGap = document.getElementById('input-roll-gap');
const valRollGap = document.getElementById('val-roll-gap');

// Output DOM Elements
const outProdD50 = document.getElementById('out-prod-d50');
const outProdD80 = document.getElementById('out-prod-d80');
const outProdSpan = document.getElementById('out-prod-span');
const outFinesSummary = document.getElementById('out-fines-summary');
const outNipAngle = document.getElementById('out-nip-angle');
const outNipStatus = document.getElementById('out-nip-status');
const outPower = document.getElementById('out-power');
const outSpecEnergy = document.getElementById('out-spec-energy');
const outCapacity = document.getElementById('out-capacity');
const outLoadStatus = document.getElementById('out-load-status');
const outYield = document.getElementById('out-yield');
const outErgun = document.getElementById('out-ergun');

// PFD Readout Elements
const dispFeedRate = document.getElementById('disp-feed-rate');
const dispRecycleRate = document.getElementById('disp-recycle-rate');
const dispTotalMill = document.getElementById('disp-total-mill');
const dispProductRate = document.getElementById('disp-product-rate');

// Global Chart References
let chartPSD = null;
let chartPowerFeed = null;

function updateCalculations() {
    const feedRate = parseFloat(inputFeedRate.value);
    const feedD50_mm = parseFloat(inputFeedD50.value);
    const feedSpan = parseFloat(inputFeedSpan.value);
    const rollGap_mm = parseFloat(inputRollGap.value);

    // Update Slider Labels
    valFeedRate.innerText = `${feedRate} kg/h`;
    valFeedD50.innerText = `${feedD50_mm.toFixed(2)} mm (${(feedD50_mm * 1000).toFixed(0)} µm)`;
    valFeedSpan.innerText = `${feedSpan.toFixed(2)} (${feedSpan < 0.7 ? 'Screen Graded' : 'Commercial'})`;
    valRollGap.innerText = `${rollGap_mm.toFixed(2)} mm (${(rollGap_mm * 1000).toFixed(0)} µm)`;

    // Compute Model
    const res = calculateDoubleRollCrusher(feedRate, feedD50_mm, feedSpan, rollGap_mm);

    // Update Output Cards
    outProdD50.innerText = `${res.prodD50_um.toFixed(0)} µm`;
    outProdD80.innerText = `d80: ${res.prodD80_um.toFixed(0)} µm | d90: ${res.prodD90_um.toFixed(0)} µm`;
    outProdSpan.innerText = `${res.prodSpan.toFixed(2)}`;
    outFinesSummary.innerText = `Fines (<100 µm): ${res.finesPct.toFixed(1)}% | Boulders: ${res.bouldersPct.toFixed(1)}%`;

    outNipAngle.innerText = `${res.alphaDeg.toFixed(1)}°`;
    if (res.isGripped) {
        outNipStatus.innerText = `✓ PASS (Gripped without slip: ≤ ${res.alphaMaxDeg.toFixed(1)}°)`;
        outNipStatus.style.color = '#34D399';
    } else {
        outNipStatus.innerText = `⚠️ SLIP RISK (Angle of Nip > ${res.alphaMaxDeg.toFixed(1)}°)`;
        outNipStatus.style.color = '#EF4444';
    }

    outPower.innerText = `${res.power_kw.toFixed(2)} kW`;
    outSpecEnergy.innerText = `Specific: ${res.specE_kg.toFixed(5)} kWh/kg`;
    outCapacity.innerText = `${res.practicalCapacity_kgh.toFixed(0)} kg/h`;
    outLoadStatus.innerText = `Load: ${res.loadPct.toFixed(0)}% of practical capacity`;
    outYield.innerText = `98.8%`;
    outErgun.innerText = `${res.deltaP_kPa.toFixed(2)} kPa`;

    // Update PFD Flowsheet telemetry
    const recycleRate = (feedRate * 0.22).toFixed(1);
    const totalMill = (feedRate * 1.22).toFixed(1);
    const productRate = (feedRate * 0.988).toFixed(1);

    if (dispFeedRate) dispFeedRate.innerText = `${feedRate.toFixed(1)} kg/h`;
    if (dispRecycleRate) dispRecycleRate.innerText = `${recycleRate} kg/h`;
    if (dispTotalMill) dispTotalMill.innerText = `${totalMill} kg/h`;
    if (dispProductRate) dispProductRate.innerText = `${productRate} kg/h`;

    // Update Charts
    updatePSDChart(res);
}

// Preset Quick Buttons
function applyPreset(preset) {
    document.querySelectorAll('.preset-btn').forEach(btn => btn.classList.remove('active'));
    
    if (preset === 'Espresso') {
        inputRollGap.value = 0.25;
        event.target.classList.add('active');
    } else if (preset === 'Drip') {
        inputRollGap.value = 0.55;
        event.target.classList.add('active');
    } else if (preset === 'ColdBrew') {
        inputRollGap.value = 0.95;
        event.target.classList.add('active');
    }
    updateCalculations();
}

// Initialize & Update Chart 1: Feed PSD vs Product PSD
function initPSDChart() {
    const ctx = document.getElementById('chartPSD').getContext('2d');
    
    chartPSD = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [50, 100, 200, 350, 500, 700, 1000, 1400, 2000, 3000, 5000, 6500, 8000, 10000].map(s => s >= 1000 ? `${(s/1000).toFixed(1)}mm` : `${s}µm`),
            datasets: [
                {
                    label: 'Crushed Coffee Powder (Product PSD)',
                    data: [],
                    borderColor: '#D4A373',
                    backgroundColor: 'rgba(212, 163, 115, 0.25)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.35,
                    pointRadius: 4
                },
                {
                    label: 'Feed Coffee Beans (Input PSD)',
                    data: [],
                    borderColor: '#38BDF8',
                    backgroundColor: 'rgba(56, 189, 248, 0.15)',
                    borderWidth: 2,
                    borderDash: [5, 5],
                    fill: true,
                    tension: 0.35,
                    pointRadius: 3
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: '#F8FAFC', font: { family: 'Plus Jakarta Sans', size: 12, weight: '600' } }
                },
                tooltip: {
                    callbacks: {
                        label: (ctx) => `${ctx.dataset.label}: ${ctx.raw.toFixed(1)}% Passing`
                    }
                }
            },
            scales: {
                x: {
                    title: { display: true, text: 'Particle Sieve Size', color: '#94A3B8', font: { weight: '600' } },
                    grid: { color: 'rgba(51, 65, 85, 0.3)' },
                    ticks: { color: '#64748B' }
                },
                y: {
                    title: { display: true, text: 'Cumulative Passing Underflow (%)', color: '#94A3B8', font: { weight: '600' } },
                    grid: { color: 'rgba(51, 65, 85, 0.3)' },
                    ticks: { color: '#64748B' },
                    min: 0,
                    max: 100
                }
            }
        }
    });
}

function updatePSDChart(res) {
    if (!chartPSD) return;
    chartPSD.data.datasets[0].data = res.prodCum;
    chartPSD.data.datasets[1].data = res.feedCum;
    chartPSD.update('none');
}

// Initialize Chart 2: Power vs Feed Rate across Roll Gaps
function initPowerChart() {
    const ctx = document.getElementById('chartPowerFeed').getContext('2d');
    const feedRates = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500];

    const espressoPowers = feedRates.map(f => calculateDoubleRollCrusher(f, 6.5, 0.85, 0.25).power_kw);
    const dripPowers = feedRates.map(f => calculateDoubleRollCrusher(f, 6.5, 0.85, 0.55).power_kw);
    const frenchPowers = feedRates.map(f => calculateDoubleRollCrusher(f, 6.5, 0.85, 0.95).power_kw);

    chartPowerFeed = new Chart(ctx, {
        type: 'line',
        data: {
            labels: feedRates.map(f => `${f} kg/h`),
            datasets: [
                {
                    label: 'Espresso Gap (0.25 mm)',
                    data: espressoPowers,
                    borderColor: '#EF4444',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    borderWidth: 2.5,
                    tension: 0.2,
                    fill: false
                },
                {
                    label: 'Drip Gap (0.55 mm)',
                    data: dripPowers,
                    borderColor: '#D4A373',
                    backgroundColor: 'rgba(212, 163, 115, 0.1)',
                    borderWidth: 2.5,
                    tension: 0.2,
                    fill: false
                },
                {
                    label: 'Cold Brew Gap (0.95 mm)',
                    data: frenchPowers,
                    borderColor: '#10B981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    borderWidth: 2.5,
                    tension: 0.2,
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: '#94A3B8', font: { family: 'Plus Jakarta Sans', size: 11 } }
                },
                tooltip: {
                    callbacks: {
                        label: (ctx) => `${ctx.dataset.label}: ${ctx.raw.toFixed(2)} kW`
                    }
                }
            },
            scales: {
                x: {
                    title: { display: true, text: 'Feed Mass Rate (kg/h)', color: '#94A3B8' },
                    grid: { color: 'rgba(51, 65, 85, 0.3)' },
                    ticks: { color: '#64748B' }
                },
                y: {
                    title: { display: true, text: 'Crusher Power Requirement (kW)', color: '#94A3B8' },
                    grid: { color: 'rgba(51, 65, 85, 0.3)' },
                    ticks: { color: '#64748B' }
                }
            }
        }
    });
}

// Event Listeners
inputFeedRate.addEventListener('input', updateCalculations);
inputFeedD50.addEventListener('input', updateCalculations);
inputFeedSpan.addEventListener('input', updateCalculations);
inputRollGap.addEventListener('input', updateCalculations);

window.addEventListener('DOMContentLoaded', () => {
    initPSDChart();
    initPowerChart();
    updateCalculations();
});
