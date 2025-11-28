# app/engine.py
from statistics import mean, median, pstdev
from typing import List, Dict
from math import fabs

# Default thresholds (MarSci Lite rules)
YELLOW_SD_PCT = 10     # 10–25% = minor anomaly
RED_SD_PCT = 25        # >25% = major anomaly

def validate_kpi_values(values: List[float], window: int):
    if len(values) != window:
        return False, f"Length mismatch: {len(values)} values for window {window}"
    if any(v is None for v in values):
        return False, "Values contain null"
    try:
        _ = [float(v) for v in values]
    except Exception:
        return False, "Values contain non-numeric items"
    return True, None

def compute_stats(values: List[float]) -> Dict[str, float]:
    n = len(values)
    if n == 0:
        return {
            "mean": 0,
            "median": 0,
            "sd": 0,
            "sd_pct": 0,
            "iqr": 0,
            "max_dev_pct": 0
        }
    mu = mean(values)
    med = median(values)
    sd = pstdev(values) if n > 1 else 0
    sd_pct = (sd / mu * 100) if mu != 0 else sd * 100
    sorted_v = sorted(values)
    q1 = sorted_v[n // 4]
    q3 = sorted_v[(3 * n) // 4]
    iqr = q3 - q1
    max_dev_pct = max([fabs((v - mu) / mu) * 100 if mu != 0 else 0 for v in values])
    return {
        "mean": mu,
        "median": med,
        "sd": sd,
        "sd_pct": sd_pct,
        "iqr": iqr,
        "max_dev_pct": max_dev_pct,
    }

def classify_severity(stats: Dict[str, float]) -> str:
    sd_pct = stats["sd_pct"]
    max_dev = stats["max_dev_pct"]
    if sd_pct > RED_SD_PCT or max_dev > RED_SD_PCT:
        return "Red"
    if sd_pct >= YELLOW_SD_PCT or max_dev >= YELLOW_SD_PCT:
        return "Yellow"
    return "Green"

def evaluate_kpi(kpi: str, window: int, values: List[float]) -> Dict:
    ok, err = validate_kpi_values(values, window)
    if not ok:
        return {"error": err}
    stats = compute_stats(values)
    sev = classify_severity(stats)
    benchmark_min = stats["mean"] - stats["sd"]
    benchmark_max = stats["mean"] + stats["sd"]
    if sev == "Green":
        summary = "No anomaly detected / ไม่พบความผิดปกติ"
    elif sev == "Yellow":
        summary = "Minor anomaly detected / พบความผิดปกติเล็กน้อย"
    else:
        summary = "High anomaly detected / ความผิดปกติสูง"
    return {
        "kpi": kpi,
        "severity": sev,
        "benchmark_min": round(benchmark_min, 6),
        "benchmark_max": round(benchmark_max, 6),
        "summary": summary,
        "raw_stats": stats
    }
