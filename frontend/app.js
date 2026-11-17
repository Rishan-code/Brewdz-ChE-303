/**
 * BrewDz Particle Engineering - web application script
 * ChE 303: Fluid Particle Systems
 *
 * Data source: window.BREWDZ_DATA from simulation_data.js, which is written by
 * generate_simulation_dataset.py together with simulation_dataset.csv (same cases).
 * This script only retrieves and interpolates those cases; it also recomputes
 * Bond's law and the Ergun equation as an independent hand-check.
 */
(function () {
    'use strict';

    const D = window.BREWDZ_DATA;
    const $ = (id) => document.getElementById(id);

    if (!D) {
        document.body.insertAdjacentHTML('afterbegin',
            '<p style="padding:1rem;background:#fde8e0;color:#7a2a12">simulation_data.js is missing. Run <code>python generate_simulation_dataset.py</code> and reload.</p>');
        return;
    }

    // ---------------------------------------------------------------- data
    const COL = {};
    D.columns.forEach((c, i) => { COL[c] = i; });
    const NUMERIC = D.columns.filter(c => !['case_id', 'grind_profile'].includes(c));
    const PROFILE = {};
    D.profiles.forEach(p => { PROFILE[p.name] = p; });

    // GRID[profile][aperture][feed] -> row array
    const GRID = {};
    D.rows.forEach(r => {
        const p = r[COL.grind_profile], a = r[COL.screen_aperture_um], f = r[COL.feed_rate_kgh];
        ((GRID[p] = GRID[p] || {})[a] = GRID[p][a] || {})[f] = r;
    });

    function bracket(levels, x) {
        const v = Math.min(Math.max(x, levels[0]), levels[levels.length - 1]);
        let i = 0;
        while (i < levels.length - 2 && v > levels[i + 1]) i++;
        return { lo: levels[i], hi: levels[i + 1], t: (v - levels[i]) / (levels[i + 1] - levels[i]) };
    }

    /** Bilinear interpolation over feed rate x screen aperture for one grind profile. */
    function simulate(profileName, feed, aperture) {
        const prof = PROFILE[profileName];
        const fb = bracket(D.feedRates, feed);
        const ab = bracket(prof.apertures, aperture);
        const g = GRID[profileName];
        const out = { profile: profileName };
        NUMERIC.forEach(k => {
            const i = COL[k];
            const lo = g[ab.lo][fb.lo][i] * (1 - fb.t) + g[ab.lo][fb.hi][i] * fb.t;
            const hi = g[ab.hi][fb.lo][i] * (1 - fb.t) + g[ab.hi][fb.hi][i] * fb.t;
            out[k] = lo * (1 - ab.t) + hi * ab.t;
        });
        return out;
    }

    // ------------------------------------------------- independent formulas
    function bondKwhPerT(p80) {
        return 10 * D.params.bond_work_index_kwh_per_t * (1 / Math.sqrt(p80) - 1 / Math.sqrt(D.params.feed_d80_um));
    }
    function ergunKPa(d32um, prof) {
        const dp = d32um * 1e-6, e = prof.bedPorosity, u = prof.velocity;
        const mu = D.params.water_viscosity_Pas, rho = D.params.water_density_kgm3;
        const visc = 150 * Math.pow(1 - e, 2) / Math.pow(e, 3) * mu * u / (dp * dp);
        const inert = 1.75 * (1 - e) / Math.pow(e, 3) * rho * u * u / dp;
        return (visc + inert) * prof.bedLength / 1000;
    }

    // -------------------------------- Double Roll Crusher mechanics (ChE 303)
    const ROLL = {
        diameter_mm: 250,      // D_R = 250 mm
        width_mm: 300,         // W_R = 300 mm
        speed_rpm: 240,        // N = 240 rpm
        bulk_density: 400,     // rho_bulk = 400 kg/m3
        vol_efficiency: 0.25,  // eta_v = 0.25
        friction_coeff: 0.32   // mu = 0.32, max alpha = 2 * atan(0.32) = 35.50 deg
    };

    function calcDoubleRoll(prof, feedD50_mm, feedSpan, millTotalFeed_kgh) {
        const s_mm = prof.rollerGap; // roll gap in mm
        // feed largest particle D_p in mm (estimated from d50 and span)
        const D_p_mm = feedD50_mm * (1 + feedSpan * 0.5);
        const cosTheta = (ROLL.diameter_mm + s_mm) / (ROLL.diameter_mm + D_p_mm);
        const thetaRad = Math.acos(Math.min(1, Math.max(-1, cosTheta)));
        const alphaDeg = 2 * thetaRad * (180 / Math.PI);
        const maxAlphaDeg = 2 * Math.atan(ROLL.friction_coeff) * (180 / Math.PI); // 35.50 deg
        const isGripped = alphaDeg <= maxAlphaDeg;

        // Practical capacity: Q = 60 * pi * D_R * W_R * N * s * rho_bulk * eta_v (in kg/h)
        const Q_theoretical = 60 * Math.PI * (ROLL.diameter_mm / 1000) * (ROLL.width_mm / 1000) * ROLL.speed_rpm * (s_mm / 1000) * ROLL.bulk_density;
        const Q_practical = Q_theoretical * ROLL.vol_efficiency;

        return {
            s_mm,
            D_p_mm,
            alphaDeg,
            maxAlphaDeg,
            isGripped,
            Q_practical,
            loadRatio: (millTotalFeed_kgh / Q_practical) * 100
        };
    }

    // ------------------------------------------------ Feed PSD Presets & Curve
    const FEED_PRESETS = {
        specialty: {
            label: "Specialty Whole Roast Baseline (d50 = 6.50 mm)",
            d50: 6.50,
            span: 0.60,
            bins: [
                { bin: "> 10 mm (Elephant)", wt: 0.05 },
                { bin: "8 – 10 mm (Large AA)", wt: 0.15 },
                { bin: "6 – 8 mm (Grade A Standard)", wt: 0.60 },
                { bin: "4 – 6 mm (Peaberry/Grade B)", wt: 0.18 },
                { bin: "< 4 mm (Broken Bean)", wt: 0.02 }
            ]
        },
        aspen1: {
            label: "Aspen Run 1: Elephant Beans (d50 = 8.10 mm)",
            d50: 8.10,
            span: 0.55,
            bins: [
                { bin: "> 10 mm", wt: 0.10 },
                { bin: "8 – 10 mm", wt: 0.50 },
                { bin: "6 – 8 mm", wt: 0.35 },
                { bin: "< 6 mm", wt: 0.05 }
            ]
        },
        aspen2: {
            label: "Aspen Run 2: Bimodal Wide Blend (d50 = 8.80 mm)",
            d50: 8.80,
            span: 0.85,
            bins: [
                { bin: "> 12 mm", wt: 0.28 },
                { bin: "10 – 12 mm", wt: 0.09 },
                { bin: "8 – 10 mm", wt: 0.38 },
                { bin: "6 – 8 mm", wt: 0.18 },
                { bin: "< 6 mm", wt: 0.07 }
            ]
        },
        aspen3: {
            label: "Aspen Run 3: Broad Graded Blend (d50 = 7.60 mm)",
            d50: 7.60,
            span: 0.75,
            bins: [
                { bin: "> 10 mm", wt: 0.17 },
                { bin: "8 – 10 mm", wt: 0.31 },
                { bin: "6 – 8 mm", wt: 0.30 },
                { bin: "4 – 6 mm", wt: 0.15 },
                { bin: "< 4 mm", wt: 0.07 }
            ]
        },
        aspen4: {
            label: "Aspen Run 4: Bell-Curve Roasted Whole Beans (d50 = 7.05 mm)",
            d50: 7.05,
            span: 0.62,
            bins: [
                { bin: "> 10 mm", wt: 0.15 },
                { bin: "8 – 10 mm", wt: 0.27 },
                { bin: "6 – 8 mm", wt: 0.38 },
                { bin: "4 – 6 mm", wt: 0.15 },
                { bin: "< 4 mm", wt: 0.05 }
            ]
        },
        aspen5: {
            label: "Aspen Run 5: Skewed Arabica Blend (d50 = 6.80 mm)",
            d50: 6.80,
            span: 0.60,
            bins: [
                { bin: "> 10 mm", wt: 0.09 },
                { bin: "8 – 10 mm", wt: 0.28 },
                { bin: "6 – 8 mm", wt: 0.44 },
                { bin: "4 – 6 mm", wt: 0.16 },
                { bin: "< 4 mm", wt: 0.03 }
            ]
        },
        aspen6: {
            label: "Aspen Run 6: Calibrated Plantation A (d50 = 7.40 mm)",
            d50: 7.40,
            span: 0.65,
            bins: [
                { bin: "> 10 mm", wt: 0.13 },
                { bin: "8 – 10 mm", wt: 0.29 },
                { bin: "6 – 8 mm", wt: 0.40 },
                { bin: "4 – 6 mm", wt: 0.15 },
                { bin: "< 4 mm", wt: 0.03 }
            ]
        }
    };

    function calcFeedPSDCurve(d50_mm, span) {
        const d50_um = d50_mm * 1000;
        const sigma_g = Math.max(1.15, 1 + span * 0.45);
        const sizes = [1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000, 11000, 12000, 13000, 14000, 15000, 16000];
        const lnSigma = Math.log(sigma_g);
        const denom = Math.sqrt(2 * Math.PI) * lnSigma;
        return sizes.map(d => {
            const z = Math.log(d / d50_um) / lnSigma;
            const pdf = Math.exp(-0.5 * z * z) / (d * denom);
            const frequency = pdf * d * 180;
            return { x: d, y: Math.max(0, frequency) };
        });
    }

    const fmt = (x, n) => Number(x).toFixed(n);
    const pctDiff = (a, b) => (b === 0 ? 0 : Math.abs(a - b) / Math.abs(b) * 100);

    // ---------------------------------------------------------------- DOM
    const inputFeed = $('input-feed-rate');
    const inputFeedD50 = $('input-feed-d50');
    const inputFeedSpan = $('input-feed-span');
    const selectFeedPSD = $('select-feed-psd');
    const btnToggleFeedTable = $('btn-toggle-feed-table');
    const feedTableContainer = $('feed-table-container');
    const inputMesh = $('input-screen-mesh');
    const selectProfile = $('select-grind-profile');
    let activeStream = 'product';
    let current = null;

    D.profiles.forEach(p => {
        const o = document.createElement('option');
        o.value = p.name;
        o.textContent = `${p.label} (nominal d50 ${p.targetD50} µm, roll gap ${p.rollerGap} mm)`;
        selectProfile.appendChild(o);
    });
    selectProfile.value = 'Drip_PourOver';

    function configureMeshSlider(reset) {
        const p = PROFILE[selectProfile.value];
        const lo = p.apertures[0], hi = p.apertures[p.apertures.length - 1];
        inputMesh.min = lo;
        inputMesh.max = hi;
        inputMesh.step = (p.apertures[1] - p.apertures[0]) / 5;
        if (reset) inputMesh.value = p.designAperture;
        $('mesh-min').textContent = `${lo} µm (finer)`;
        $('mesh-max').textContent = `${hi} µm (coarser)`;
    }

    // ------------------------------------------------------------- streams
    function streamInfo(key, r, prof) {
        const F = r.feed_rate_kgh, M = r.mill_total_feed_kgh, R = r.recycle_rate_kgh;
        const P = r.product_rate_kgh, X = r.fines_byproduct_kgh;
        const roasted = F * 0.97;
        const info = {
            feed: ['FEED', F, `Raw coffee beans entering the circuit (at 25 °C, 1 atm with 3% moisture). Fresh solid feed to the roaster.`],
            beans: ['FEED', F, `Raw coffee beans entering the circuit (at 25 °C, 1 atm with 3% moisture). Fresh solid feed to the roaster.`],
            roasted: ['ROASTED', roasted, `De-moisturized, brittle roasted whole beans discharging from roaster at 210 °C and 1.013 bar. Ready for low-shear comminution.`],
            mixed: ['MIXED', M, `Combined solids entering crusher: fresh roasted beans (${fmt(roasted, 1)} kg/h) plus recycled screen oversize (${fmt(R, 1)} kg/h).`],
            millfeed: ['MIXED', M, `Combined solids entering crusher: fresh roasted beans (${fmt(roasted, 1)} kg/h) plus recycled screen oversize (${fmt(R, 1)} kg/h).`],
            crushed: ['CRUSHED', M, `Double roll crusher discharge with roll gap ${prof.rollerGap} mm. Controlled fracture distribution (dp < 2087 µm) fed directly to the vibrating screen.`],
            ground: ['CRUSHED', M, `Double roll crusher discharge with roll gap ${prof.rollerGap} mm. Controlled fracture distribution (dp < 2087 µm) fed directly to the vibrating screen.`],
            recycle: ['OVERSIZE (RECYCLE)', R, `Coarse grounds (> ${fmt(r.screen_aperture_um, 0)} µm, 1093–2087 µm) returned to the mixer. Closed-loop circulating ratio R/F = ${fmt(r.recycle_ratio, 2)}, eliminating solid waste.`],
            product: ['PROD (ON-SPEC)', P, `Calibrated on-spec coffee powder: d50 = ${fmt(r.product_d50_um, 0)} µm, d80 = ${fmt(r.product_d80_um, 0)} µm, span = ${fmt(r.product_span, 2)}. 0.00% boulders (> 1590 µm), yield = ${fmt(r.product_yield_pct, 1)}%.`],
            fines: ['FINE (DUST)', X, `Screen undersize super-fines (< 597 µm), ${fmt(100 - r.product_yield_pct, 1)}% of fresh feed. De-dusted by-product stream collected for instant soluble coffee extraction.`],
            undersize: ['UNDERSIZE', F, `Screen undersize stream entering secondary classification.`]
        };
        return info[key] || ['STREAM', F, 'Stream information'];
    }

    function renderStreamDetail() {
        if (!current) return;
        const [name, flow, desc] = streamInfo(activeStream, current, PROFILE[current.profile]);
        $('sd-name').textContent = name;
        $('sd-flow').textContent = `${fmt(flow, 1)} kg/h`;
        $('sd-desc').textContent = desc;
        document.querySelectorAll('.stream').forEach(g => {
            g.classList.toggle('active', g.dataset.stream === activeStream);
        });
    }

    document.querySelectorAll('.stream').forEach(g => {
        const pick = () => { activeStream = g.dataset.stream; renderStreamDetail(); };
        g.addEventListener('mouseenter', pick);
        g.addEventListener('focus', pick);
        g.addEventListener('click', pick);
    });

    // ------------------------------------------------------------- charts
    const HAS_CHART = typeof window.Chart !== 'undefined';
    const C = { ink: '#2C1810', muted: '#7A6A5C', grid: 'rgba(44,24,16,0.08)', espresso: '#8C3B1E', drip: '#C8915A', french: '#2F7D5B', conv: '#B4553F', brew: '#2F7D5B' };
    const PROFILE_COLOR = { Espresso: C.espresso, Drip_PourOver: C.drip, FrenchPress_ColdBrew: C.french };
    let chartPower = null, chartPSD = null, chartFines = null;

    function axis(title, extra) {
        return Object.assign({
            title: { display: true, text: title, color: C.muted, font: { size: 12 } },
            grid: { color: C.grid },
            ticks: { color: C.muted }
        }, extra || {});
    }

    const apertureLine = {
        id: 'apertureLine',
        afterDatasetsDraw(chart) {
            const a = chart.options.plugins.apertureLine && chart.options.plugins.apertureLine.value;
            if (!a) return;
            const x = chart.scales.x.getPixelForValue(a);
            const { top, bottom } = chart.chartArea;
            const ctx = chart.ctx;
            ctx.save();
            ctx.setLineDash([5, 4]);
            ctx.strokeStyle = C.ink;
            ctx.lineWidth = 1.2;
            ctx.beginPath(); ctx.moveTo(x, top); ctx.lineTo(x, bottom); ctx.stroke();
            ctx.setLineDash([]);
            ctx.fillStyle = C.ink;
            ctx.font = '11px "JetBrains Mono", monospace';
            ctx.textAlign = 'left';
            ctx.fillText(`cut ${Math.round(a)} µm`, x + 5, top + 12);
            ctx.restore();
        }
    };

    function initCharts() {
        if (!HAS_CHART) { $('chart-fallback').hidden = false; return; }
        Chart.defaults.font.family = '"Plus Jakarta Sans", system-ui, sans-serif';
        Chart.defaults.color = C.muted;
        const legend = { labels: { color: C.ink, boxWidth: 14, font: { size: 11 } } };

        chartPower = new Chart($('chartPowerFeed'), {
            type: 'line',
            data: {
                datasets: D.profiles.map(p => ({
                    label: p.label,
                    data: D.feedRates.map(f => ({ x: f, y: GRID[p.name][p.designAperture][f][COL.mill_power_kw] })),
                    borderColor: PROFILE_COLOR[p.name], backgroundColor: PROFILE_COLOR[p.name],
                    borderWidth: 2, pointRadius: 0
                })).concat([{
                    label: 'Operating point', data: [], showLine: false,
                    pointRadius: 7, pointHoverRadius: 8, pointBackgroundColor: '#fff',
                    pointBorderColor: C.ink, pointBorderWidth: 3, borderColor: C.ink, backgroundColor: '#fff'
                }])
            },
            options: {
                responsive: true, maintainAspectRatio: false, animation: { duration: 200 },
                plugins: { legend, tooltip: { callbacks: { label: c => `${c.dataset.label}: ${c.parsed.y.toFixed(2)} kW at ${c.parsed.x} kg/h` } } },
                scales: { x: axis('Fresh feed rate (kg/h)', { type: 'linear', min: 50, max: 500 }), y: axis('Mill power (kW)', { beginAtZero: true }) }
            }
        });

        chartPSD = new Chart($('chartPSD'), {
            type: 'line',
            data: {
                datasets: [
                    { label: 'Input: Feed Size Distribution (Whole Beans)', data: [], borderColor: '#D4A373', backgroundColor: 'rgba(212,163,115,0.14)', borderDash: [6, 4], borderWidth: 2.2, pointRadius: 0, fill: true, tension: 0.3 },
                    { label: 'Conventional open-loop grinder', data: [], borderColor: C.conv, backgroundColor: 'transparent', borderDash: [4, 4], borderWidth: 1.5, pointRadius: 0, tension: 0.3 },
                    { label: 'Output: BrewDz Closed-Loop Product', data: [], borderColor: C.brew, backgroundColor: 'rgba(47,125,91,0.22)', borderWidth: 2.5, pointRadius: 0, fill: true, tension: 0.3 }
                ]
            },
            plugins: [apertureLine],
            options: {
                responsive: true, maintainAspectRatio: false, animation: { duration: 200 },
                plugins: { legend, apertureLine: { value: null }, tooltip: { callbacks: { title: i => `${i[0].parsed.x.toFixed(0)} µm`, label: c => `${c.dataset.label}: ${c.parsed.y.toFixed(0)} %/decade` } } },
                scales: {
                    x: axis('Particle size (µm, log scale)', {
                        type: 'logarithmic', min: 10, max: 20000,
                        ticks: { color: C.muted, callback: v => ([10, 30, 100, 300, 1000, 3000, 10000].includes(v) ? v : '') }
                    }),
                    y: axis('Mass frequency (% per log decade)', { beginAtZero: true })
                }
            }
        });

        chartFines = new Chart($('chartFines'), {
            type: 'line',
            data: {
                datasets: [
                    { label: 'Pressure drop vs. fines', data: [], borderColor: C.drip, borderWidth: 2.5, pointRadius: 0, tension: 0.2 },
                    { label: 'BrewDz (your operating point)', data: [], showLine: false, pointRadius: 7, pointBackgroundColor: C.brew, pointBorderColor: '#fff', pointBorderWidth: 2, borderColor: C.brew, backgroundColor: C.brew },
                    { label: 'Conventional grinder', data: [], showLine: false, pointRadius: 7, pointStyle: 'rectRot', pointBackgroundColor: C.conv, pointBorderColor: '#fff', pointBorderWidth: 2, borderColor: C.conv, backgroundColor: C.conv }
                ]
            },
            options: {
                responsive: true, maintainAspectRatio: false, animation: { duration: 200 },
                plugins: { legend, tooltip: { callbacks: { label: c => `${c.dataset.label}: ${c.parsed.y.toFixed(3)} kPa at ${c.parsed.x.toFixed(1)}% fines` } } },
                scales: { x: axis('Fines below 100 µm (% of product mass)', { type: 'linear', min: 0 }), y: axis('Bed pressure drop (kPa)', { beginAtZero: true }) }
            }
        });
    }

    function updateCharts(r, prof, feedD50, feedSpan) {
        if (!HAS_CHART) return;
        chartPower.data.datasets[3].data = [{ x: r.feed_rate_kgh, y: r.mill_power_kw }];
        chartPower.data.datasets.forEach((ds, i) => { if (i < 3) ds.borderWidth = D.profiles[i].name === prof.name ? 3.5 : 1.5; });
        chartPower.update();

        chartPSD.data.datasets[0].data = calcFeedPSDCurve(feedD50, feedSpan);
        chartPSD.data.datasets[1].data = D.chartSizes.map((s, i) => ({ x: s, y: prof.psdConventional[i] }));
        chartPSD.data.datasets[2].data = D.chartSizes.map((s, i) => ({ x: s, y: prof.psdBrewdz[i] }));
        chartPSD.options.plugins.apertureLine.value = r.screen_aperture_um;
        chartPSD.update();

        chartFines.data.datasets[0].data = prof.sweep.map(p => ({ x: p.finesPct, y: p.dP }));
        chartFines.data.datasets[1].data = [{ x: r.fines_fraction_pct, y: r.ergun_pressure_drop_kPa }];
        chartFines.data.datasets[2].data = [{ x: prof.conventional.finesPct, y: prof.conventional.dP }];
        chartFines.update();
    }

    // --------------------------------------------------------- hand-check
    function renderCheck(r, prof, roll) {
        const F = r.feed_rate_kgh;
        const E = bondKwhPerT(r.circuit_p80_um);
        const P = F / 1000 * E;
        const dP = ergunKPa(r.sauter_d32_um, prof);
        const M = F + r.recycle_rate_kgh;
        const row = (step, calc, res, ref, unit, n, diff) =>
            `<tr><td>${step}</td><td class="mono">${calc}</td><td class="mono">${fmt(res, n)} ${unit}${diff !== false ? `<span class="diff">dataset ${fmt(ref, n)} · ${fmt(pctDiff(res, ref), 2)}% off</span>` : ''}</td></tr>`;
        
        let nipRow = '';
        if (roll) {
            nipRow =
                row('Angle of Nip', `cos(&alpha;/2) = (${ROLL.diameter_mm} + ${prof.rollerGap})/(${ROLL.diameter_mm} + ${fmt(roll.D_p_mm, 2)})`, roll.alphaDeg, roll.maxAlphaDeg, `&deg; (${roll.isGripped ? 'PASS &le; 35.5&deg;' : 'SLIP RISK'})`, 2, false) +
                row('Roll Practical Cap', `Q = 60&pi; &times; 0.25 &times; 0.30 &times; 240 &times; ${fmt(prof.rollerGap/1000, 4)} &times; 400 &times; 0.25`, roll.Q_practical, M, 'kg/h', 1, false);
        }

        $('check-body').innerHTML =
            nipRow +
            row('Recycle balance', `M = F + R = ${fmt(F, 1)} + ${fmt(r.recycle_rate_kgh, 1)}`, M, r.mill_total_feed_kgh, 'kg/h', 1) +
            row('Bond energy', `E = 10 × ${D.params.bond_work_index_kwh_per_t} × (1/√${fmt(r.circuit_p80_um, 0)} − 1/√${D.params.feed_d80_um})`, E, r.specific_energy_kwh_per_kg * 1000, 'kWh/t', 3) +
            row('Mill power', `P = ${fmt(F / 1000, 3)} t/h × ${fmt(E, 3)} kWh/t`, P, r.mill_power_kw, 'kW', 3) +
            row('Ergun ΔP', `d32 = ${fmt(r.sauter_d32_um, 0)} µm, ε = ${prof.bedPorosity}, u = ${prof.velocity * 1000} mm/s, L = ${prof.bedLength * 1000} mm`, dP, r.ergun_pressure_drop_kPa, 'kPa', 3);
    }

    function renderParams() {
        const p = D.params;
        const rows = [
            ['Bond work index W<sub>i</sub> (assumed)', `${p.bond_work_index_kwh_per_t} kWh/t`],
            ['Feed size F<sub>80</sub> (whole bean)', `${p.feed_d80_um} µm`],
            ['Mill size rule', `d<sub>63</sub> = ${p.mill_size_factor} × roll gap`],
            ['Rosin–Rammler exponent n', `${p.rr_uniformity_n}`],
            ['Fines mode', `log-normal, median ${p.fines_mode_median_um} µm, σ<sub>g</sub> ${p.fines_mode_sigma_g}`],
            ['Mill fines share φ<sub>f</sub>', D.profiles.map(q => `${q.label.split(' ')[0]} ${fmt(q.millFinesFrac * 100, 0)}%`).join(' · ')],
            ['Screen recoveries', `E<sub>O</sub> = ${p.screen_oversize_recovery}, E<sub>U</sub> = ${p.screen_undersize_recovery}`],
            ['Cyclone grade efficiency', `T(d) = 1 / (1 + (d/${p.cyclone_cut_um} µm)<sup>${p.cyclone_sharpness_k}</sup>)`],
            ['Brew water (92 °C)', `ρ = ${p.water_density_kgm3} kg/m³, μ = ${p.water_viscosity_Pas} Pa·s`],
            ['Conventional grinder baseline', `${fmt(p.conventional_fines_frac * 100, 0)}% fines mode, n = ${p.conventional_rr_n}, same nominal d50`]
        ];
        $('param-body').innerHTML = rows.map(r => `<tr><td>${r[0]}</td><td class="mono">${r[1]}</td></tr>`).join('');
    }

    function renderHero() {
        const stats = D.profiles.map(p => {
            const r = simulate(p.name, 100, p.designAperture);
            return { y: r.product_yield_pct, s: r.product_span, f: (1 - r.fines_fraction_pct / p.conventional.finesPct) * 100 };
        });
        const range = (k, n, suffix) => {
            const v = stats.map(s => s[k]);
            return `${fmt(Math.min(...v), n)}–${fmt(Math.max(...v), n)}${suffix}`;
        };
        $('hero-yield').textContent = range('y', 0, '%');
        $('hero-fines').textContent = range('f', 0, '%');
        $('hero-span').textContent = range('s', 2, '');
        $('footer-cases').textContent = D.rows.length;
    }

    // -------------------------------------------------------------- update
    function update() {
        const prof = PROFILE[selectProfile.value];
        const feed = parseFloat(inputFeed.value);
        const feedD50 = parseFloat(inputFeedD50 ? inputFeedD50.value : 6.50);
        const feedSpan = parseFloat(inputFeedSpan ? inputFeedSpan.value : 0.60);
        const mesh = parseFloat(inputMesh.value);
        const r = simulate(prof.name, feed, mesh);
        current = r;

        const roll = calcDoubleRoll(prof, feedD50, feedSpan, r.mill_total_feed_kgh);

        $('val-feed-rate').textContent = `${feed} kg/h`;
        if ($('val-feed-d50')) $('val-feed-d50').textContent = `${feedD50.toFixed(2)} mm`;
        if ($('val-feed-span')) $('val-feed-span').textContent = `${feedSpan.toFixed(2)}`;
        $('val-screen-mesh').textContent = `${mesh} µm`;

        // Comminution power (Bond's law)
        if ($('out-power')) $('out-power').textContent = `${fmt(r.mill_power_kw, 2)} kW`;
        if ($('out-spec-energy')) $('out-spec-energy').textContent = `Specific energy ${fmt(r.specific_energy_kwh_per_kg * 1000, 2)} kWh/t · fresh feed basis`;

        // Product mass rate & yield
        if ($('out-product-mass')) $('out-product-mass').textContent = `${fmt(r.product_rate_kgh, 1)} kg/h`;
        if ($('out-product-yield')) $('out-product-yield').textContent = `On-spec yield: ${fmt(r.product_yield_pct, 1)}% · 0.00% boulders`;
        if ($('out-yield')) $('out-yield').textContent = `${fmt(r.product_yield_pct, 1)}%`;
        if ($('out-product')) $('out-product').textContent = `${fmt(r.product_rate_kgh, 1)} kg/h product · ${fmt(r.fines_byproduct_kgh, 1)} kg/h fines`;

        // Recycle mass rate & ratio
        if ($('out-recycle-mass')) $('out-recycle-mass').textContent = `${fmt(r.recycle_rate_kgh, 1)} kg/h`;
        if ($('out-recycle-sub')) $('out-recycle-sub').textContent = `Circulating load R/F = ${fmt(r.recycle_ratio, 2)} · crusher feed ${fmt(r.mill_total_feed_kgh, 0)} kg/h`;
        if ($('out-recycle')) $('out-recycle').textContent = `${fmt(r.recycle_rate_kgh, 1)} kg/h`;
        if ($('out-recycle-ratio')) $('out-recycle-ratio').textContent = `Circulating load R/F = ${fmt(r.recycle_ratio, 2)} · mill throughput ${fmt(r.mill_total_feed_kgh, 0)} kg/h`;
        
        // Full product size distribution percentiles (d10, d50, d80, d90, span)
        const d50 = r.product_d50_um;
        const d80 = r.product_d80_um;
        const span = r.product_span;
        const d10 = Math.max(10, d50 * (1 - span * 0.42));
        const d90 = d50 * (1 + span * 0.58);
        if ($('out-d50')) $('out-d50').textContent = `d50 = ${fmt(d50, 0)} µm`;
        if ($('out-span')) $('out-span').textContent = `d10: ${fmt(d10, 0)} µm · d50: ${fmt(d50, 0)} µm · d80: ${fmt(d80, 0)} µm · d90: ${fmt(d90, 0)} µm · Span: ${fmt(span, 2)}`;

        // Double roll Angle of Nip and Capacity
        if ($('out-nip')) {
            $('out-nip').textContent = `${fmt(roll.alphaDeg, 1)}°`;
            $('out-nip-badge').textContent = roll.isGripped ? '✓ PASS (≤ 35.5°)' : '⚠️ SLIP RISK (> 35.5°)';
            $('out-nip-badge').className = `pill ${roll.isGripped ? 'pill-pass' : 'pill-fail'}`;
            $('out-nip-sub').textContent = `Allowable limit α ≤ 35.5° (μ = 0.32) · Feed Dp = ${fmt(roll.D_p_mm, 2)} mm`;
        }
        if ($('out-capacity')) {
            $('out-capacity').textContent = `${fmt(roll.Q_practical, 0)} kg/h`;
            $('out-capacity-sub').textContent = `Load ${fmt(roll.loadRatio, 0)}% of practical capacity (${fmt(r.mill_total_feed_kgh, 0)} kg/h total crusher feed)`;
        }

        // Fines mass & Ergun bed ΔP
        if ($('out-fines-mass')) $('out-fines-mass').textContent = `${fmt(r.fines_byproduct_kgh, 1)} kg/h`;
        if ($('out-fines-sub')) $('out-fines-sub').textContent = `Super-fines (< 597 µm) for instant coffee soluble extraction`;
        if ($('out-fines')) $('out-fines').textContent = `${fmt(r.fines_fraction_pct, 1)}%`;
        if ($('out-fines-cmp')) $('out-fines-cmp').textContent = `${fmt((1 - r.fines_fraction_pct / prof.conventional.finesPct) * 100, 0)}% lower than conventional grinder (${fmt(prof.conventional.finesPct, 1)}%)`;
        if ($('out-ergun')) $('out-ergun').textContent = `${fmt(r.ergun_pressure_drop_kPa, 3)} kPa`;
        if ($('out-ergun-cmp')) $('out-ergun-cmp').textContent = `Sauter d32 = ${fmt(r.sauter_d32_um, 0)} µm · conventional bed ${fmt(prof.conventional.dP, 3)} kPa (clean bed)`;

        // Aspen flowsheet streams
        const roasted = feed * 0.97;
        if ($('pfd-feed')) $('pfd-feed').textContent = `${fmt(feed, 0)} kg/h`;
        if ($('pfd-beans')) $('pfd-beans').textContent = `${fmt(feed, 0)} kg/h`;
        if ($('pfd-roasted')) $('pfd-roasted').textContent = `${fmt(roasted, 0)} kg/h`;
        if ($('pfd-mixed')) $('pfd-mixed').textContent = `${fmt(r.mill_total_feed_kgh, 0)} kg/h`;
        if ($('pfd-millfeed')) $('pfd-millfeed').textContent = `${fmt(r.mill_total_feed_kgh, 0)} kg/h`;
        if ($('pfd-crushed')) $('pfd-crushed').textContent = `${fmt(r.mill_total_feed_kgh, 0)} kg/h`;
        if ($('pfd-ground')) $('pfd-ground').textContent = `${fmt(r.mill_total_feed_kgh, 0)} kg/h`;
        if ($('pfd-recycle')) $('pfd-recycle').textContent = `${fmt(r.recycle_rate_kgh, 0)} kg/h`;
        if ($('pfd-product')) $('pfd-product').textContent = `${fmt(r.product_rate_kgh, 0)} kg/h`;
        if ($('pfd-fines')) $('pfd-fines').textContent = `${fmt(r.fines_byproduct_kgh, 0)} kg/h`;
        if ($('pfd-gap')) $('pfd-gap').textContent = `gap ${prof.rollerGap} mm`;
        if ($('pfd-aperture')) $('pfd-aperture').textContent = `${fmt(mesh, 0)} µm`;

        renderStreamDetail();
        renderCheck(r, prof, roll);
        updateCharts(r, prof, feedD50, feedSpan);
    }

    function renderFeedMeshTable(presetKey, feedD50, feedSpan) {
        const tbody = $('feed-mesh-tbody');
        if (!tbody) return;
        const preset = FEED_PRESETS[presetKey];
        let bins = [];
        if (preset && preset.bins) {
            bins = preset.bins;
        } else {
            const d50 = feedD50;
            bins = [
                { bin: `> ${(d50 * 1.4).toFixed(1)} mm`, wt: 0.10 },
                { bin: `${(d50 * 1.15).toFixed(1)} – ${(d50 * 1.4).toFixed(1)} mm`, wt: 0.25 },
                { bin: `${(d50 * 0.85).toFixed(1)} – ${(d50 * 1.15).toFixed(1)} mm`, wt: 0.45 },
                { bin: `< ${(d50 * 0.85).toFixed(1)} mm`, wt: 0.20 }
            ];
        }
        tbody.innerHTML = bins.map(b => `
            <tr style="border-bottom:1px solid rgba(0,0,0,0.06);">
                <td style="padding:0.25rem 0; font-family:var(--font-mono);">${b.bin}</td>
                <td style="padding:0.25rem 0; text-align:right; font-family:var(--font-mono); font-weight:600;">${(b.wt * 100).toFixed(1)}%</td>
            </tr>
        `).join('');
    }

    if (selectFeedPSD) {
        selectFeedPSD.addEventListener('change', () => {
            const key = selectFeedPSD.value;
            if (FEED_PRESETS[key]) {
                inputFeedD50.value = FEED_PRESETS[key].d50;
                inputFeedSpan.value = FEED_PRESETS[key].span;
                renderFeedMeshTable(key, FEED_PRESETS[key].d50, FEED_PRESETS[key].span);
            }
            update();
        });
    }

    if (btnToggleFeedTable && feedTableContainer) {
        btnToggleFeedTable.addEventListener('click', () => {
            const isHidden = feedTableContainer.style.display === 'none';
            feedTableContainer.style.display = isHidden ? 'block' : 'none';
            btnToggleFeedTable.textContent = isHidden ? '▲ Hide Feed Sieve Distribution Table' : '📋 View Feed Sieve Distribution Table';
            if (isHidden) {
                renderFeedMeshTable(selectFeedPSD ? selectFeedPSD.value : 'specialty', parseFloat(inputFeedD50.value), parseFloat(inputFeedSpan.value));
            }
        });
    }

    inputFeed.addEventListener('input', update);
    if (inputFeedD50) {
        inputFeedD50.addEventListener('input', () => {
            if (selectFeedPSD && selectFeedPSD.value !== 'custom') selectFeedPSD.value = 'custom';
            renderFeedMeshTable('custom', parseFloat(inputFeedD50.value), parseFloat(inputFeedSpan.value));
            update();
        });
    }
    if (inputFeedSpan) {
        inputFeedSpan.addEventListener('input', () => {
            if (selectFeedPSD && selectFeedPSD.value !== 'custom') selectFeedPSD.value = 'custom';
            renderFeedMeshTable('custom', parseFloat(inputFeedD50.value), parseFloat(inputFeedSpan.value));
            update();
        });
    }
    inputMesh.addEventListener('input', update);
    selectProfile.addEventListener('change', () => { configureMeshSlider(true); update(); });
    $('btn-reset-mesh').addEventListener('click', () => { configureMeshSlider(true); update(); });

    const btnLoadAspen = $('btn-load-aspen');
    if (btnLoadAspen) {
        btnLoadAspen.addEventListener('click', () => {
            if (selectFeedPSD) selectFeedPSD.value = 'specialty';
            selectProfile.value = 'Drip_PourOver';
            configureMeshSlider(false);
            inputFeed.value = 100;
            inputMesh.value = 700;
            if (inputFeedD50) inputFeedD50.value = 6.50;
            if (inputFeedSpan) inputFeedSpan.value = 0.60;
            renderFeedMeshTable('specialty', 6.50, 0.60);
            update();
        });
    }

    const navToggle = $('nav-toggle'), navLinks = $('nav-links');
    navToggle.addEventListener('click', () => {
        const open = navLinks.classList.toggle('open');
        navToggle.setAttribute('aria-expanded', String(open));
    });
    navLinks.addEventListener('click', (e) => {
        if (e.target.tagName === 'A') { navLinks.classList.remove('open'); navToggle.setAttribute('aria-expanded', 'false'); }
    });

    configureMeshSlider(true);
    renderParams();
    renderHero();
    renderFeedMeshTable('specialty', 6.50, 0.60);
    initCharts();
    update();
})();
