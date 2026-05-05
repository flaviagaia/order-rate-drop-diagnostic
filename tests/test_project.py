from __future__ import annotations

import unittest
from pathlib import Path

from src.data_factory import build_sample_dataset
from src.modeling import run_analysis


class OrderRateDropDiagnosticTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.base_dir = Path(__file__).resolve().parents[1]

    def test_dataset_factory_creates_files(self) -> None:
        dataset_info = build_sample_dataset(self.base_dir)
        self.assertEqual(dataset_info["dataset_source"], "synthetic_order_rate_drop_diagnostic")
        self.assertTrue(Path(dataset_info["dataset_path"]).exists())
        self.assertTrue(Path(dataset_info["dataset_reference_path"]).exists())

    def test_analysis_contract(self) -> None:
        report = run_analysis(self.base_dir)
        self.assertEqual(report["dataset_source"], "synthetic_order_rate_drop_diagnostic")
        self.assertGreater(report["baseline_orders"], report["current_orders"])
        self.assertLess(report["order_rate_drop_pct"], 0.0)
        self.assertIn("south", report["region_diagnostic"])
        self.assertEqual(report["recommendation"]["decision"], "investigate_checkout_and_south_region")
        self.assertTrue(Path(report["report_artifact"]).exists())


if __name__ == "__main__":
    unittest.main()
