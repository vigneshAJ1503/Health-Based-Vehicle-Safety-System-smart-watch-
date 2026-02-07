# risk_engine.py

from fastapi import FastAPI
from collections import deque
import requests
import statistics

from common import (
    WINDOW_SIZE,
    WARN_LEVEL,
    ALERT_LEVEL,
    CRITICAL_LEVEL,
    TCU_URL
)

app = FastAPI()

bpm_buffer = deque(maxlen=WINDOW_SIZE)


def compute_risk(window):

    avg = statistics.mean(window)
    std = statistics.pstdev(window)

    score = 0

    # Mean contribution
    if avg > 120:
        score += 25
    if avg > 140:
        score += 35

    # Variance (instability)
    if std > 15:
        score += 15

    # Persistent spikes
    high = len([x for x in window if x > 150])
    score += min(high * 5, 20)

    return min(score, 100)


@app.post("/risk")
def process(data: dict):

    bpm = data["bpm"]
    ack = data["ack"]

    bpm_buffer.append(bpm)

    if len(bpm_buffer) < WINDOW_SIZE:
        return {"status": "warming_up"}

    risk = compute_risk(bpm_buffer)

    payload = {
        "driver_id": data["driver_id"],
        "risk": risk,
        "ack": ack,
        "bpm": bpm
    }

    print("Risk →", payload)

    # Forward to TCU
    try:
        requests.post(TCU_URL, json=payload, timeout=2)
    except:
        print("TCU unreachable")

    return payload
