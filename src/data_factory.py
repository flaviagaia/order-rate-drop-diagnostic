from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Dict, List


PUBLIC_DATASET_REFERENCE = {
    "primary_reference": {
        "name": "NYC TLC Trip Record Data",
        "url": "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page",
        "role": "Public mobility marketplace reference used here only as inspiration for temporal and regional demand patterns.",
    },
    "notes": [
        "The runtime dataset is synthetic because production-grade order funnel diagnostics are rarely public.",
        "The project simulates two time windows so the analyst can explain where a 10% order-rate drop came from.",
    ],
}


def _write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def build_sample_dataset(base_dir: Path) -> Dict[str, str]:
    rows: List[Dict[str, object]] = []
    periods = [
        ("baseline", 1000, {"north": 0.26, "south": 0.24, "east": 0.25, "west": 0.25}, 0),
        ("current", 1000, {"north": 0.26, "south": 0.24, "east": 0.25, "west": 0.25}, 1),
    ]
    devices = ["ios", "android", "web"]
    segments = ["new_user", "casual", "power_user"]
    region_offsets = {"north": 0, "south": 1, "east": 2, "west": 0}

    row_id = 1
    for period_name, total_sessions, region_mix, period_offset in periods:
        for region, share in region_mix.items():
            region_sessions = int(total_sessions * share)
            for index in range(region_sessions):
                device = devices[(index + period_offset) % len(devices)]
                user_segment = segments[(index + region_offsets[region] + period_offset) % len(segments)]
                peak_hour = 1 if index % 5 in (0, 1) else 0
                promo_shown = 1 if index % 4 == 0 else 0

                checkout_start_rate = 0.74
                order_place_rate = 0.64

                if period_name == "current":
                    checkout_start_rate -= 0.015
                    order_place_rate -= 0.02
                if region == "south" and period_name == "current":
                    checkout_start_rate -= 0.055
                    order_place_rate -= 0.05
                if device == "web" and period_name == "current":
                    checkout_start_rate -= 0.025
                if user_segment == "power_user":
                    order_place_rate += 0.05
                if promo_shown and period_name == "baseline":
                    checkout_start_rate += 0.02
                if promo_shown and period_name == "current":
                    checkout_start_rate += 0.01

                sessions = 1
                app_open = 1
                store_view = 1 if (index + row_id) % 100 < 91 else 0
                cart_add = 1 if (index + row_id) % 100 < int(checkout_start_rate * 100) else 0
                checkout_start = 1 if cart_add and (index * 3 + row_id) % 100 < int(checkout_start_rate * 100) else 0
                order_placed = 1 if checkout_start and (index * 7 + row_id) % 100 < int(order_place_rate * 100) else 0

                rows.append(
                    {
                        "period": period_name,
                        "session_id": f"ORD-{row_id:05d}",
                        "region": region,
                        "device": device,
                        "user_segment": user_segment,
                        "peak_hour": peak_hour,
                        "promo_shown": promo_shown,
                        "app_open": app_open,
                        "store_view": store_view,
                        "cart_add": cart_add,
                        "checkout_start": checkout_start,
                        "order_placed": order_placed,
                        "sessions": sessions,
                    }
                )
                row_id += 1

    raw_dir = base_dir / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    dataset_path = raw_dir / "order_funnel_sessions.csv"
    reference_path = raw_dir / "public_dataset_reference.json"
    _write_csv(dataset_path, rows)
    reference_path.write_text(json.dumps(PUBLIC_DATASET_REFERENCE, ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        "dataset_source": "synthetic_order_rate_drop_diagnostic",
        "dataset_path": str(dataset_path),
        "dataset_reference_path": str(reference_path),
    }
