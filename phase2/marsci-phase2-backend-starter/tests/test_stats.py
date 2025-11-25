from app.models.stats import compute_stats, severity_from_sd_pct
def test_compute_stats_basic():
    arr = [1.0, 1.2, 0.8, 1.1, 1.0]
    m, med, s, i, sp = compute_stats(arr)
    assert round(m,3) == 1.02
    assert med == 1.0
    assert s > 0
    assert sp >= 0
def test_severity():
    assert severity_from_sd_pct(5) == "Green"
    assert severity_from_sd_pct(15) == "Yellow"
    assert severity_from_sd_pct(30) == "Red"
