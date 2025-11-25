# test_engine.py
import math
from app.engine import StatsEngine

def almost_equal(a, b, tol=1e-6):
    return abs(a - b) <= tol

def test_normalize_and_compute_core_stats():
    engine = StatsEngine()
    values = [1, 2, 3, 4, 5]
    normalized = engine.normalize_values(values)
    assert normalized == [1.0, 2.0, 3.0, 4.0, 5.0]
    stats = engine.compute_core_stats(normalized)
    # mean = 3
    assert almost_equal(stats['mean'], 3.0)
    # median = 3
    assert almost_equal(stats['median'], 3.0)
    # sd (population) sqrt(2) ~ 1.41421356
    assert almost_equal(stats['sd'], math.sqrt(2.0))
    # sd_pct = sd/mean*100
    assert almost_equal(stats['sd_pct'], (math.sqrt(2.0)/3.0)*100)

def test_analyze_outputs_public_schema():
    engine = StatsEngine()
    values = [10, 12, 11, 13, 12]
    out = engine.analyze(kpi='CTR', values=values)
    assert out['kpi'] == 'CTR'
    assert out['severity'] in ('Green', 'Yellow', 'Red')
    assert 'benchmark_min' in out and 'benchmark_max' in out
    assert out['benchmark_min'] <= out['benchmark_max']
    assert 'summary_th' in out and 'summary_en' in out
    assert out['timestamp'].endswith('Z')

def test_invalid_values_raise():
    engine = StatsEngine()
    try:
        engine.normalize_values(['a', 'b'])
        assert False, "Expected ValueError"
    except ValueError:
        pass
