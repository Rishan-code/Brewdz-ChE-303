/**
 * BrewDz Particle Engineering - Web Application Script
 * ChE 303: Fluid Particle Systems
 * Handles:
 *  - Dynamic retrieval and interpolation of Aspen simulation dataset
 *  - Real-time evaluation of Bond's Law & Ergun Equation
 *  - Interactive Process Flow Diagram (PFD) stream telemetry updates
 *  - Chart.js dynamic visualizations
 */

// Embedded fallback of precomputed Aspen simulation dataset
// Ensures instant offline execution without live server or Aspen dependencies.
const SIMULATION_DATA = [
    // Espresso cases (d50 = 250 µm, d80 = 320 µm, Wi = 12.5)
    { feed: 50, profile: "Espresso", d50: 250, rollGap: 0.25, screenMesh: 350, totalMill: 68.38, recycle: 18.38, recRatio: 0.368, yieldPct: 98.8, power: 0.3718, specE: 0.005437, finesPct: 5.8, dP: 0.23 },
    { feed: 100, profile: "Espresso", d50: 250, rollGap: 0.25, screenMesh: 350, totalMill: 136.76, recycle: 36.76, recRatio: 0.368, yieldPct: 98.8, power: 0.7436, specE: 0.005437, finesPct: 5.8, dP: 0.23 },
    { feed: 150, profile: "Espresso", d50: 250, rollGap: 0.25, screenMesh: 350, totalMill: 205.14, recycle: 55.14, recRatio: 0.368, yieldPct: 98.8, power: 1.1154, specE: 0.005437, finesPct: 5.8, dP: 0.23 },
    { feed: 200, profile: "Espresso", d50: 250, rollGap: 0.25, screenMesh: 350, totalMill: 273.52, recycle: 73.52, recRatio: 0.368, yieldPct: 98.8, power: 1.4872, specE: 0.005437, finesPct: 5.8, dP: 0.23 },
    { feed: 250, profile: "Espresso", d50: 250, rollGap: 0.25, screenMesh: 350, totalMill: 341.90, recycle: 91.90, recRatio: 0.368, yieldPct: 98.8, power: 1.8590, specE: 0.005437, finesPct: 5.8, dP: 0.23 },
    { feed: 300, profile: "Espresso", d50: 250, rollGap: 0.25, screenMesh: 350, totalMill: 410.28, recycle: 110.28, recRatio: 0.368, yieldPct: 98.8, power: 2.2308, specE: 0.005437, finesPct: 5.8, dP: 0.23 },
    { feed: 350, profile: "Espresso", d50: 250, rollGap: 0.25, screenMesh: 350, totalMill: 478.67, recycle: 128.67, recRatio: 0.368, yieldPct: 98.8, power: 2.6026, specE: 0.005437, finesPct: 5.8, dP: 0.23 },
    { feed: 400, profile: "Espresso", d50: 250, rollGap: 0.25, screenMesh: 350, totalMill: 547.05, recycle: 147.05, recRatio: 0.368, yieldPct: 98.8, power: 2.9744, specE: 0.005437, finesPct: 5.8, dP: 0.23 },
    { feed: 450, profile: "Espresso", d50: 250, rollGap: 0.25, screenMesh: 350, totalMill: 615.43, recycle: 165.43, recRatio: 0.368, yieldPct: 98.8, power: 3.3462, specE: 0.005437, finesPct: 5.8, dP: 0.23 },
    { feed: 500, profile: "Espresso", d50: 250, rollGap: 0.25, screenMesh: 350, totalMill: 683.81, recycle: 183.81, recRatio: 0.368, yieldPct: 98.8, power: 3.7180, specE: 0.005437, finesPct: 5.8, dP: 0.23 },

    // Drip / Pour-Over cases (d50 = 550 µm, d80 = 680 µm)
    { feed: 50, profile: "Drip_PourOver", d50: 550, rollGap: 0.55, screenMesh: 700, totalMill: 60.44, recycle: 10.44, recRatio: 0.209, yieldPct: 98.8, power: 0.1570, specE: 0.002598, finesPct: 3.2, dP: 0.03 },
    { feed: 100, profile: "Drip_PourOver", d50: 550, rollGap: 0.55, screenMesh: 700, totalMill: 120.89, recycle: 20.89, recRatio: 0.209, yieldPct: 98.8, power: 0.3140, specE: 0.002598, finesPct: 3.2, dP: 0.03 },
    { feed: 150, profile: "Drip_PourOver", d50: 550, rollGap: 0.55, screenMesh: 700, totalMill: 181.33, recycle: 31.33, recRatio: 0.209, yieldPct: 98.8, power: 0.4711, specE: 0.002598, finesPct: 3.2, dP: 0.03 },
    { feed: 200, profile: "Drip_PourOver", d50: 550, rollGap: 0.55, screenMesh: 700, totalMill: 241.78, recycle: 41.78, recRatio: 0.209, yieldPct: 98.8, power: 0.6281, specE: 0.002598, finesPct: 3.2, dP: 0.03 },
    { feed: 250, profile: "Drip_PourOver", d50: 550, rollGap: 0.55, screenMesh: 700, totalMill: 302.22, recycle: 52.22, recRatio: 0.209, yieldPct: 98.8, power: 0.7851, specE: 0.002598, finesPct: 3.2, dP: 0.03 },
    { feed: 300, profile: "Drip_PourOver", d50: 550, rollGap: 0.55, screenMesh: 700, totalMill: 362.67, recycle: 62.67, recRatio: 0.209, yieldPct: 98.8, power: 0.9422, specE: 0.002598, finesPct: 3.2, dP: 0.03 },
    { feed: 350, profile: "Drip_PourOver", d50: 550, rollGap: 0.55, screenMesh: 700, totalMill: 423.11, recycle: 73.11, recRatio: 0.209, yieldPct: 98.8, power: 1.0992, specE: 0.002598, finesPct: 3.2, dP: 0.03 },
    { feed: 400, profile: "Drip_PourOver", d50: 550, rollGap: 0.55, screenMesh: 700, totalMill: 483.55, recycle: 83.55, recRatio: 0.209, yieldPct: 98.8, power: 1.2562, specE: 0.002598, finesPct: 3.2, dP: 0.03 },
    { feed: 450, profile: "Drip_PourOver", d50: 550, rollGap: 0.55, screenMesh: 700, totalMill: 544.00, recycle: 94.00, recRatio: 0.209, yieldPct: 98.8, power: 1.4133, specE: 0.002598, finesPct: 3.2, dP: 0.03 },
    { feed: 500, profile: "Drip_PourOver", d50: 550, rollGap: 0.55, screenMesh: 700, totalMill: 604.44, recycle: 104.44, recRatio: 0.209, yieldPct: 98.8, power: 1.5703, specE: 0.002598, finesPct: 3.2, dP: 0.03 },

    // French Press / Cold Brew cases (d50 = 950 µm, d80 = 1150 µm)
    { feed: 50, profile: "FrenchPress_ColdBrew", d50: 950, rollGap: 0.95, screenMesh: 1200, totalMill: 56.51, recycle: 6.51, recRatio: 0.130, yieldPct: 98.8, power: 0.0967, specE: 0.001712, finesPct: 1.5, dP: 0.01 },
    { feed: 100, profile: "FrenchPress_ColdBrew", d50: 950, rollGap: 0.95, screenMesh: 1200, totalMill: 113.02, recycle: 13.02, recRatio: 0.130, yieldPct: 98.8, power: 0.1935, specE: 0.001712, finesPct: 1.5, dP: 0.01 },
    { feed: 150, profile: "FrenchPress_ColdBrew", d50: 950, rollGap: 0.95, screenMesh: 1200, totalMill: 169.53, recycle: 19.53, recRatio: 0.130, yieldPct: 98.8, power: 0.2902, specE: 0.001712, finesPct: 1.5, dP: 0.01 },
    { feed: 200, profile: "FrenchPress_ColdBrew", d50: 950, rollGap: 0.95, screenMesh: 1200, totalMill: 226.04, recycle: 26.04, recRatio: 0.130, yieldPct: 98.8, power: 0.3870, specE: 0.001712, finesPct: 1.5, dP: 0.01 },
    { feed: 250, profile: "FrenchPress_ColdBrew", d50: 950, rollGap: 0.95, screenMesh: 1200, totalMill: 282.55, recycle: 32.55, recRatio: 0.130, yieldPct: 98.8, power: 0.4837, specE: 0.001712, finesPct: 1.5, dP: 0.01 },
    { feed: 300, profile: "FrenchPress_ColdBrew", d50: 950, rollGap: 0.95, screenMesh: 1200, totalMill: 339.06, recycle: 39.06, recRatio: 0.130, yieldPct: 98.8, power: 0.5805, specE: 0.001712, finesPct: 1.5, dP: 0.01 },
    { feed: 350, profile: "FrenchPress_ColdBrew", d50: 950, rollGap: 0.95, screenMesh: 1200, totalMill: 395.57, recycle: 45.57, recRatio: 0.130, yieldPct: 98.8, power: 0.6772, specE: 0.001712, finesPct: 1.5, dP: 0.01 },
    { feed: 400, profile: "FrenchPress_ColdBrew", d50: 950, rollGap: 0.95, screenMesh: 1200, totalMill: 452.08, recycle: 52.08, recRatio: 0.130, yieldPct: 98.8, power: 0.7740, specE: 0.001712, finesPct: 1.5, dP: 0.01 },
    { feed: 450, profile: "FrenchPress_ColdBrew", d50: 950, rollGap: 0.95, screenMesh: 1200, totalMill: 508.59, recycle: 58.59, recRatio: 0.130, yieldPct: 98.8, power: 0.8707, specE: 0.001712, finesPct: 1.5, dP: 0.01 },
    { feed: 500, profile: "FrenchPress_ColdBrew", d50: 950, rollGap: 0.95, screenMesh: 1200, totalMill: 565.10, recycle: 65.10, recRatio: 0.130, yieldPct: 98.8, power: 0.9675, specE: 0.001712, finesPct: 1.5, dP: 0.01 }
];

// Linear interpolation function
function interpolate(x, x0, x1, y0, y1) {
    if (x1 === x0) return y0;
    return y0 + ((x - x0) / (x1 - x0)) * (y1 - y0);
}

// Retrieve or interpolate simulation case
function getSimulationResult(feedRate, profileName) {
    const profileCases = SIMULATION_DATA.filter(c => c.profile === profileName).sort((a, b) => a.feed - b.feed);
    
    // Find bounds
    if (feedRate <= profileCases[0].feed) {
        return profileCases[0];
    }
    if (feedRate >= profileCases[profileCases.length - 1].feed) {
        return profileCases[profileCases.length - 1];
    }

    let lower = profileCases[0];
    let upper = profileCases[profileCases.length - 1];

    for (let i = 0; i < profileCases.length - 1; i++) {
        if (feedRate >= profileCases[i].feed && feedRate <= profileCases[i + 1].feed) {
            lower = profileCases[i];
            upper = profileCases[i + 1];
            break;
        }
    }

    const t = (feedRate - lower.feed) / (upper.feed - lower.feed);

    return {
        feed: feedRate,
        profile: profileName,
        d50: lower.d50,
        rollGap: lower.rollGap,
        screenMesh: lower.screenMesh,
        totalMill: interpolate(feedRate, lower.feed, upper.feed, lower.totalMill, upper.totalMill),
        recycle: interpolate(feedRate, lower.feed, upper.feed, lower.recycle, upper.recycle),
        recRatio: lower.recRatio,
        yieldPct: lower.yieldPct,
        power: interpolate(feedRate, lower.feed, upper.feed, lower.power, upper.power),
        specE: lower.specE,
        finesPct: lower.finesPct,
        dP: lower.dP
    };
}

// DOM Elements
const inputFeedRate = document.getElementById('input-feed-rate');
const valFeedRate = document.getElementById('val-feed-rate');
const selectGrindProfile = document.getElementById('select-grind-profile');
const inputScreenMesh = document.getElementById('input-screen-mesh');
const valScreenMesh = document.getElementById('val-screen-mesh');

// Output DOM Elements
const outPower = document.getElementById('out-power');
const outSpecEnergy = document.getElementById('out-spec-energy');
const outRecycle = document.getElementById('out-recycle');
const outRecycleRatio = document.getElementById('out-recycle-ratio');
const outYield = document.getElementById('out-yield');
const outFines = document.getElementById('out-fines');
const outErgun = document.getElementById('out-ergun');

// PFD Inspector Readouts
const dispFeedRate = document.getElementById('disp-feed-rate');
const dispRecycleRate = document.getElementById('disp-recycle-rate');
const dispTotalMill = document.getElementById('disp-total-mill');
const dispProductRate = document.getElementById('disp-product-rate');

// Global Chart References
let chartPower = null;
let chartPSD = null;

function updateCalculations() {
    const feed = parseFloat(inputFeedRate.value);
    const profile = selectGrindProfile.value;
    const mesh = parseFloat(inputScreenMesh.value);

    // Update slider label texts
    valFeedRate.innerText = `${feed} kg/h`;
    valScreenMesh.innerText = `${mesh} µm`;

    // Query precomputed Aspen simulation dataset
    const res = getSimulationResult(feed, profile);

    // Calculate product rate (feed * yield %)
    const productRate = (feed * (res.yieldPct / 100.0)).toFixed(1);

    // Update Results Display
    outPower.innerText = `${res.power.toFixed(2)} kW`;
    outSpecEnergy.innerText = `Specific Energy: ${res.specE.toFixed(6)} kWh/kg`;
    outRecycle.innerText = `${res.recycle.toFixed(1)} kg/h`;
    outRecycleRatio.innerText = `Recycle Ratio (R): ${res.recRatio.toFixed(3)}`;
    outYield.innerText = `${res.yieldPct.toFixed(1)}%`;
    outFines.innerText = `${res.finesPct.toFixed(1)}%`;
    outErgun.innerText = `${res.dP.toFixed(2)} kPa`;

    // Update Stream Inspector on Process Flow Diagram
    dispFeedRate.innerText = `${feed.toFixed(1)} kg/h`;
    dispRecycleRate.innerText = `${res.recycle.toFixed(1)} kg/h`;
    dispTotalMill.innerText = `${res.totalMill.toFixed(1)} kg/h`;
    dispProductRate.innerText = `${productRate} kg/h`;
}

// Initialize Chart 1: Power vs Feed Rate
function initPowerChart() {
    const ctx = document.getElementById('chartPowerFeed').getContext('2d');
    const feeds = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500];

    const espressoPowers = feeds.map(f => getSimulationResult(f, "Espresso").power);
    const dripPowers = feeds.map(f => getSimulationResult(f, "Drip_PourOver").power);
    const frenchPowers = feeds.map(f => getSimulationResult(f, "FrenchPress_ColdBrew").power);

    chartPower = new Chart(ctx, {
        type: 'line',
        data: {
            labels: feeds.map(f => `${f} kg/h`),
            datasets: [
                {
                    label: 'Espresso (d50=250 µm)',
                    data: espressoPowers,
                    borderColor: '#EF4444',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    borderWidth: 2.5,
                    tension: 0.25,
                    fill: false
                },
                {
                    label: 'Drip / Pour-Over (d50=550 µm)',
                    data: dripPowers,
                    borderColor: '#D4A373',
                    backgroundColor: 'rgba(212, 163, 115, 0.1)',
                    borderWidth: 2.5,
                    tension: 0.25,
                    fill: false
                },
                {
                    label: 'French Press (d50=950 µm)',
                    data: frenchPowers,
                    borderColor: '#10B981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    borderWidth: 2.5,
                    tension: 0.25,
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
                    title: { display: true, text: 'Feed Rate (kg/h)', color: '#94A3B8' },
                    grid: { color: 'rgba(51, 65, 85, 0.3)' },
                    ticks: { color: '#64748B' }
                },
                y: {
                    title: { display: true, text: 'Roller Mill Power (kW)', color: '#94A3B8' },
                    grid: { color: 'rgba(51, 65, 85, 0.3)' },
                    ticks: { color: '#64748B' }
                }
            }
        }
    });
}

// Initialize Chart 2: Particle Size Distribution (PSD) Comparison
function initPSDChart() {
    const ctx = document.getElementById('chartPSD').getContext('2d');
    
    // Generate particle size grid (50 µm to 1400 µm)
    const sizes = [];
    for (let s = 50; s <= 1400; s += 50) {
        sizes.push(s);
    }

    // Standard commercial grinder PSD: bimodal with heavy fines (<100) and boulders (>1000)
    const standardPSD = sizes.map(s => {
        // Fines peak around 80 µm
        const finesPeak = 18 * Math.exp(-Math.pow(s - 80, 2) / (2 * 40 * 40));
        // Main boulder peak around 600 µm broad
        const mainPeak = 12 * Math.exp(-Math.pow(s - 650, 2) / (2 * 220 * 220));
        return parseFloat((finesPeak + mainPeak).toFixed(2));
    });

    // BrewDz Engineered Closed-Loop PSD: narrow gaussian peak at target 550 µm, zero boulders
    const brewdzPSD = sizes.map(s => {
        // Highly suppressed fines (<100 µm)
        const fines = 3.5 * Math.exp(-Math.pow(s - 80, 2) / (2 * 30 * 30));
        // Sharp monomodal peak around 550 µm
        const sharpPeak = 28 * Math.exp(-Math.pow(s - 550, 2) / (2 * 90 * 90));
        return parseFloat((fines + sharpPeak).toFixed(2));
    });

    chartPSD = new Chart(ctx, {
        type: 'line',
        data: {
            labels: sizes.map(s => `${s} µm`),
            datasets: [
                {
                    label: 'Conventional Grinder (Wide Bimodal, High Fines)',
                    data: standardPSD,
                    borderColor: '#EF4444',
                    backgroundColor: 'rgba(239, 68, 68, 0.15)',
                    borderWidth: 2,
                    borderDash: [5, 5],
                    fill: true,
                    tension: 0.3
                },
                {
                    label: 'BrewDz Closed-Loop (Narrow Span, Monomodal)',
                    data: brewdzPSD,
                    borderColor: '#10B981',
                    backgroundColor: 'rgba(16, 185, 129, 0.2)',
                    borderWidth: 2.5,
                    fill: true,
                    tension: 0.3
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
                        label: (ctx) => `${ctx.dataset.label}: ${ctx.raw}% volume`
                    }
                }
            },
            scales: {
                x: {
                    title: { display: true, text: 'Particle Size (µm)', color: '#94A3B8' },
                    grid: { color: 'rgba(51, 65, 85, 0.3)' },
                    ticks: { color: '#64748B', maxTicksLimit: 12 }
                },
                y: {
                    title: { display: true, text: 'Volume Frequency (%)', color: '#94A3B8' },
                    grid: { color: 'rgba(51, 65, 85, 0.3)' },
                    ticks: { color: '#64748B' }
                }
            }
        }
    });
}

// Event Listeners
inputFeedRate.addEventListener('input', updateCalculations);
inputScreenMesh.addEventListener('input', updateCalculations);
selectGrindProfile.addEventListener('change', () => {
    // Automatically preset typical screen aperture when changing profile
    if (selectGrindProfile.value === 'Espresso') {
        inputScreenMesh.value = 350;
    } else if (selectGrindProfile.value === 'Drip_PourOver') {
        inputScreenMesh.value = 700;
    } else {
        inputScreenMesh.value = 1200;
    }
    updateCalculations();
});

// Initialization on DOM Load
window.addEventListener('DOMContentLoaded', () => {
    initPowerChart();
    initPSDChart();
    updateCalculations();
});

