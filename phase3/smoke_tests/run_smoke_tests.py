import requests, sys, time
BASE = "http://localhost:8000"
def health():
    r = requests.get(BASE + "/healthz", timeout=5)
    print("health", r.status_code, r.text)
    return r.status_code == 200
def analyze():
    payload = {"kpi":"CTR","window":5,"values":[1,1,1,1,1],"role":"anon"}
    r = requests.post(BASE + "/analyze", json=payload, timeout=5)
    print("analyze", r.status_code, r.text)
    return r.status_code == 200 and "severity" in r.json()
if __name__ == '__main__':
    if not health():
        print("health failed"); sys.exit(2)
    if not analyze():
        print("analyze failed"); sys.exit(3)
    print("SMOKE OK")
