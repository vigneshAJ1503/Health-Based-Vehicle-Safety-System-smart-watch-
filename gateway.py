# gateway.py

from fastapi import FastAPI
import requests
from common import RISK_URL

app = FastAPI()


@app.post("/health")
def ingest(data: dict):

    print("Gateway ←", data)

    # Forward to risk engine
    try:
        requests.post(RISK_URL, json=data, timeout=2)
    except:
        print("Risk engine unreachable")

    return {"status": "received"}
