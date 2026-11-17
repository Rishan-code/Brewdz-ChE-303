"""
ChE 303: Fluid Particle Systems
Course Project: Engineering the Perfect Coffee Powder
Company: BrewDz Particle Engineering Pvt. Ltd.

Module: Parametric Simulation Dataset Generator
Generates: simulation_dataset.csv
Varies feed rate (50 - 500 kg/h) across 3 distinct brewing grind profiles.
Models steady-state closed loop Aspen Plus flowsheet behavior with oversize recycle.
"""

import csv
import math


def generate_dataset():
    feed_rates = list(range(50, 525, 25))  # 50, 75, ..., 500 kg/h (19 levels)
    
    profiles = [
        {
            "name": "Espresso",
            "target_d50_um": 250.0,
            "d80_product_um": 320.0,
            "roller_gap_mm": 0.25,
            "screen_mesh_um": 350.0,
            "single_pass_oversize_frac": 0.28,
            "fines_fraction_pct": 5.8,
            "bed_porosity": 0.38,
            "bed_length_m": 0.02, # 20 mm espresso puck
            "superficial_velocity_ms": 0.0022, # ~ 9 bar machine flow
        },
        {
            "name": "Drip_PourOver",
            "target_d50_um": 550.0,
            "d80_product_um": 680.0,
            "roller_gap_mm": 0.55,
            "screen_mesh_um": 700.0,
            "single_pass_oversize_frac": 0.18,
            "fines_fraction_pct": 3.2,
            "bed_porosity": 0.44,
            "bed_length_m": 0.05, # 50 mm cone bed
            "superficial_velocity_ms": 0.0012, # gravity drip
        },
        {
            "name": "FrenchPress_ColdBrew",
            "target_d50_um": 950.0,
            "d80_product_um": 1150.0,
            "roller_gap_mm": 0.95,
            "screen_mesh_um": 1200.0,
            "single_pass_oversize_frac": 0.12,
            "fines_fraction_pct": 1.5,
            "bed_porosity": 0.48,
            "bed_length_m": 0.08, # immersion bed
            "superficial_velocity_ms": 0.0008,
        }
    ]

    d80_feed_um = 6500.0  # Whole roasted coffee bean
    Wi = 12.5             # Bond Work Index (kWh/tonne)
    water_rho = 965.0     # kg/m3 (92°C)
    water_mu = 0.000306   # Pa.s (92°C)

    cases = []
    case_id = 1

    for prof in profiles:
        for f_rate in feed_rates:
            # Steady-state recycle mass balance:
            # Let alpha = fraction of mill effluent that is oversize (> screen mesh)
            # Fresh feed F, Mill feed M = F + R.
            # At steady state, if screen separation is high efficiency (95% of oversize recovered to recycle):
            alpha = prof["single_pass_oversize_frac"]
            screen_oversize_eff = 0.96
            
            # Recycle rate R = M * alpha * screen_oversize_eff
            # M = F + R  =>  M = F + M * (alpha * 0.96)
            # M = F / (1 - alpha * 0.96)
            split_recycle = alpha * screen_oversize_eff
            total_mill_feed = f_rate / (1.0 - split_recycle)
            recycle_rate = total_mill_feed - f_rate
            recycle_ratio = recycle_rate / f_rate

            # Product rate (undersize product stream)
            product_rate = f_rate * (1.0 - 0.012) # minor dusting/loss 1.2%
            product_yield_pct = (product_rate / f_rate) * 100.0

            # Bond's Comminution Power for the roller mill:
            # Product d80 and feed d80:
            term_prod = 1.0 / math.sqrt(prof["d80_product_um"])
            term_feed = 1.0 / math.sqrt(d80_feed_um)
            specific_energy_kwh_ton = 10.0 * Wi * (term_prod - term_feed)
            specific_energy_kwh_kg = specific_energy_kwh_ton / 1000.0

            # Total mill power based on total throughput through mill (M in ton/h)
            mill_throughput_tph = total_mill_feed / 1000.0
            mill_power_kw = mill_throughput_tph * specific_energy_kwh_ton

            # Ergun equation for coffee extraction bed pressure drop:
            dp_m = prof["target_d50_um"] * 1e-6
            eps = prof["bed_porosity"]
            u = prof["superficial_velocity_ms"]
            L = prof["bed_length_m"]

            viscous = 150.0 * ((1.0 - eps) ** 2) / (eps ** 3) * (water_mu * u / (dp_m ** 2))
            inertial = 1.75 * (1.0 - eps) / (eps ** 3) * (water_rho * (u ** 2) / dp_m)
            delta_P_Pa = (viscous + inertial) * L
            delta_P_kPa = delta_P_Pa / 1000.0

            cases.append({
                "case_id": case_id,
                "feed_rate_kgh": round(f_rate, 1),
                "grind_profile": prof["name"],
                "target_d50_um": round(prof["target_d50_um"], 1),
                "d80_product_um": round(prof["d80_product_um"], 1),
                "roller_gap_mm": round(prof["roller_gap_mm"], 2),
                "screen_mesh_um": round(prof["screen_mesh_um"], 1),
                "mill_total_feed_kgh": round(total_mill_feed, 2),
                "recycle_rate_kgh": round(recycle_rate, 2),
                "recycle_ratio": round(recycle_ratio, 3),
                "product_rate_kgh": round(product_rate, 2),
                "product_yield_pct": round(product_yield_pct, 2),
                "mill_power_kw": round(mill_power_kw, 4),
                "specific_energy_kwh_per_kg": round(specific_energy_kwh_kg, 6),
                "fines_fraction_pct": round(prof["fines_fraction_pct"], 2),
                "ergun_pressure_drop_kPa": round(delta_P_kPa, 2),
            })
            case_id += 1

    # Write to CSV in data/ and frontend/
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.dirname(script_dir)
    target_paths = [
        os.path.join(repo_dir, "data", "simulation_dataset.csv"),
        os.path.join(repo_dir, "frontend", "simulation_dataset.csv")
    ]

    fieldnames = list(cases[0].keys())
    for target in target_paths:
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(cases)
        print(f"Generated {len(cases)} cases in '{target}'.")


if __name__ == "__main__":
    generate_dataset()

