from typing import List, Tuple
import math
def mean(arr: List[float]) -> float:
    return sum(arr)/len(arr) if arr else 0.0
def median(arr: List[float]) -> float:
    s = sorted(arr)
    n = len(s)
    mid = n//2
    return s[mid] if n%2 else (s[mid-1]+s[mid])/2
def sd(arr: List[float]) -> float:
    n = len(arr)
    if n < 2: return 0.0
    m = mean(arr)
    var = sum((x-m)**2 for x in arr) / (n-1)
    return math.sqrt(var)
def iqr(arr: List[float]) -> float:
    s = sorted(arr)
    n = len(s)
    q1 = s[(n-1)//4]
    q3 = s[((n-1)*3)//4]
    return q3 - q1
def sd_pct(arr: List[float]) -> float:
    m = mean(arr)
    if m == 0: return 0.0
    return (sd(arr)/abs(m))*100
def severity_from_sd_pct(sd_pct: float) -> str:
    if sd_pct > 25: return "Red"
    if sd_pct > 10: return "Yellow"
    return "Green"
def compute_stats(arr: List[float]) -> Tuple[float,float,float,float,float]:
    m = mean(arr)
    med = median(arr)
    s = sd(arr)
    i = iqr(arr)
    sp = sd_pct(arr)
    return m, med, s, i, sp
