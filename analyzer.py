# analyzer.py

from fastapi import FastAPI
import requests

from common import MAX_SAFE_BPM, MIN_SAFE_BPM, TCU_URL

app = FastAPI()

@app.post("/analyze")
def analyze(data: dict):

    bpm = data["bpm"]

    is_danger = (
        bpm > MAX_SAFE_BPM or
        bpm < MIN_SAFE_BPM
    )

    decision = {
        "driver_id": data["driver_id"],
        "bpm": bpm,
        "danger": is_danger
    }

    print("Analysis:", decision)

    if is_danger:
        requests.post(TCU_URL, json=decision)

    return decision
