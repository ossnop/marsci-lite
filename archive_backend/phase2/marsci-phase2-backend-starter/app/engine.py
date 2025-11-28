# engine.py
# MarSci Lite — Phase 2 Backend Stats Engine
# Production-ready core stats logic (server-side)
from typing import List, Dict, Any
import numpy as np
from statistics import mean, median
from datetime import datetime

class StatsEngine:
    """Backend Calculation Engine for MarSci Lite (Phase 2)
    - Computes mean, median, SD, SD%, IQR
    - Determines anomaly severity (Green / Yellow / Red)
    - Outputs benchmark range (mean ± SD)
    - Fully masks intermediate results (internal use only)
    """

    def __init__(self, severity_config: Dict[str, float] = None):
        # severity_config allows overriding thresholds for tests / env
        # expected keys: green_max_pct, yellow_max_pct (red is > yellow_max_pct)
        if severity_config is None:
            severity_config = {"green_max_pct": 10.0, "yellow_max_pct": 25.0}
        self.severity_config = severity_config

    # -------------------------------------------------
    # Normalization / Preprocessing
    # -------------------------------------------------
    def normalize_values(self, values: List[float]) -> List[float]:
        """Ensure values are parsed correctly and cleaned."""
        cleaned: List[float] = []
        for v in values:
            try:
                # Accept numeric strings or numbers
                cleaned.append(float(v))
            except Exception as exc:
                raise ValueError(f"Invalid numeric value detected: {v}") from exc
        if len(cleaned) == 0:
            raise ValueError("No numeric values provided")
        return cleaned

    # -------------------------------------------------
    # Statistical Computation
    # -------------------------------------------------
    def compute_core_stats(self, values: List[float]) -> Dict[str, float]:
        """Compute metrics. All returned metrics are internal-use values."""
        arr = np.array(values, dtype=float)

        m = float(mean(arr))
        med = float(median(arr))
        sd = float(np.std(arr, ddof=0)) if arr.size > 1 else 0.0
        sd_pct = float((sd / m) * 100) if m != 0 else 0.0

        q1 = float(np.percentile(arr, 25))
        q3 = float(np.percentile(arr, 75))
        iqr = q3 - q1

        return {
            "mean": m,
            "median": med,
            "sd": sd,
            "sd_pct": sd_pct,
            "q1": q1,
            "q3": q3,
            "iqr": iqr,
        }

    # -------------------------------------------------
    # Severity Decision Logic (Blueprint rules)
    # -------------------------------------------------
    def determine_severity(self, sd_pct: float) -> str:
        """Severity classification using configured thresholds."""
        gmax = self.severity_config.get("green_max_pct", 10.0)
        ymax = self.severity_config.get("yellow_max_pct", 25.0)
        if sd_pct < gmax:
            return "Green"
        if sd_pct < ymax:
            return "Yellow"
        return "Red"

    # -------------------------------------------------
    # Public Output (masked)
    # -------------------------------------------------
    def build_public_output(self, kpi: str, stats: Dict[str, float]) -> Dict[str, Any]:
        """Return public-safe JSON for frontend. Mask internal metrics."""
        severity = self.determine_severity(stats["sd_pct"])

        benchmark_min = stats["mean"] - stats["sd"]
        benchmark_max = stats["mean"] + stats["sd"]

        summary_th = {
            "Green": "ไม่พบความผิดปกติ",
            "Yellow": "พบความผิดปกติเล็กน้อย",
            "Red": "พบความผิดปกติสูง",
        }[severity]

        summary_en = {
            "Green": "No anomaly detected",
            "Yellow": "Minor anomaly detected",
            "Red": "High anomaly detected",
        }[severity]

        return {
            "kpi": kpi,
            "severity": severity,
            "benchmark_min": round(benchmark_min, 6),
            "benchmark_max": round(benchmark_max, 6),
            "summary_th": summary_th,
            "summary_en": summary_en,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    # -------------------------------------------------
    # Main Public Entry
    # -------------------------------------------------
    def analyze(self, kpi: str, values: List[float]) -> Dict[str, Any]:
        """Main function used by /analyze API endpoint."""
        normalized = self.normalize_values(values)
        stats = self.compute_core_stats(normalized)
        output = self.build_public_output(kpi, stats)
        return output


# module-level engine instance (can be imported)
default_stats_engine = StatsEngine()
