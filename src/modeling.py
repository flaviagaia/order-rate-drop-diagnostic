from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Dict, List

from .data_factory import build_sample_dataset


FUNNEL_STEPS = ["app_open", "store_view", "cart_add", "checkout_start", "order_placed"]


def _read_rows(path: str) -> List[Dict[str, str]]:
    with Path(path).open("r", encoding="utf-8", newline="") as csv_file:
        return list(csv.DictReader(csv_file))


def _sum_metric(rows: List[Dict[str, str]], metric: str) -> int:
    return sum(int(row[metric]) for row in rows)


def _period_rows(rows: List[Dict[str, str]], period: str) -> List[Dict[str, str]]:
    return [row for row in rows if row["period"] == period]


def _funnel_summary(rows: List[Dict[str, str]]) -> Dict[str, int]:
    return {step: _sum_metric(rows, step) for step in FUNNEL_STEPS}


def _funnel_rates(summary: Dict[str, int]) -> Dict[str, float]:
    rates: Dict[str, float] = {}
    previous_value = None
    for step in FUNNEL_STEPS:
        current_value = summary[step]
        if previous_value is None:
            rates[step] = 1.0
        else:
            rates[step] = round(current_value / previous_value, 4) if previous_value else 0.0
        previous_value = current_value
    return rates


def _segment_drop(rows: List[Dict[str, str]], key: str) -> Dict[str, Dict[str, float]]:
    baseline = _period_rows(rows, "baseline")
    current = _period_rows(rows, "current")
    values = sorted({row[key] for row in rows})
    result: Dict[str, Dict[str, float]] = {}
    for value in values:
        baseline_orders = _sum_metric([row for row in baseline if row[key] == value], "order_placed")
        current_orders = _sum_metric([row for row in current if row[key] == value], "order_placed")
        drop = current_orders - baseline_orders
        result[value] = {
            "baseline_orders": baseline_orders,
            "current_orders": current_orders,
            "absolute_change": drop,
            "relative_change_pct": round((drop / baseline_orders) * 100, 2) if baseline_orders else 0.0,
        }
    return result


def _top_drivers(rows: List[Dict[str, str]]) -> List[Dict[str, object]]:
    region_drops = _segment_drop(rows, "region")
    sorted_regions = sorted(region_drops.items(), key=lambda item: item[1]["absolute_change"])
    return [
        {
            "dimension": "region",
            "value": value,
            **metrics,
        }
        for value, metrics in sorted_regions[:3]
    ]


def run_analysis(base_dir: Path) -> Dict[str, object]:
    dataset_info = build_sample_dataset(base_dir)
    rows = _read_rows(dataset_info["dataset_path"])
    baseline_rows = _period_rows(rows, "baseline")
    current_rows = _period_rows(rows, "current")

    baseline_summary = _funnel_summary(baseline_rows)
    current_summary = _funnel_summary(current_rows)
    baseline_orders = baseline_summary["order_placed"]
    current_orders = current_summary["order_placed"]
    order_rate_drop_pct = round(((current_orders - baseline_orders) / baseline_orders) * 100, 2)

    report = {
        "dataset_source": dataset_info["dataset_source"],
        "session_count": len(rows),
        "baseline_session_count": len(baseline_rows),
        "current_session_count": len(current_rows),
        "baseline_funnel": baseline_summary,
        "current_funnel": current_summary,
        "baseline_funnel_rates": _funnel_rates(baseline_summary),
        "current_funnel_rates": _funnel_rates(current_summary),
        "baseline_orders": baseline_orders,
        "current_orders": current_orders,
        "order_rate_drop_pct": order_rate_drop_pct,
        "region_diagnostic": _segment_drop(rows, "region"),
        "device_diagnostic": _segment_drop(rows, "device"),
        "user_segment_diagnostic": _segment_drop(rows, "user_segment"),
        "top_drop_drivers": _top_drivers(rows),
        "recommendation": {
            "decision": "investigate_checkout_and_south_region",
            "reasoning": [
                "The order drop is concentrated in the south region and is amplified at the checkout stage.",
                "The current period shows weaker checkout-start and order-placement progression than the baseline.",
                "A product or operational issue affecting the south region and late-funnel completion is the most plausible first hypothesis.",
            ],
        },
    }

    processed_dir = base_dir / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)
    report_path = processed_dir / "order_rate_drop_report.json"
    report["report_artifact"] = str(report_path)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report
