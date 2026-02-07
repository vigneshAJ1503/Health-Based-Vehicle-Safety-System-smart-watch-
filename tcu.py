# tcu.py

from fastapi import FastAPI
from enum import Enum
import time

from common import (
    WARN_LEVEL,
    ALERT_LEVEL,
    CRITICAL_LEVEL
)

app = FastAPI()


# --------------------------------
# FSM States
# --------------------------------

class State(str, Enum):

    NORMAL = "NORMAL"
    WARNING = "WARNING"
    ALERT = "ALERT"
    PULL_OVER = "PULL_OVER"
    STOPPED = "STOPPED"


# --------------------------------
# Safety Controller
# --------------------------------

class SafetyFSM:

    def __init__(self):

        self.state = State.NORMAL
        self.last_change = time.time()
        self.speed = 80
        self.last_risk = 0


    def transition(self, risk, ack):

        self.last_risk = risk

        if self.state == State.NORMAL:

            if risk > WARN_LEVEL:
                self._set(State.WARNING)

        elif self.state == State.WARNING:

            if ack:
                self._set(State.NORMAL)

            elif risk > ALERT_LEVEL:
                self._set(State.ALERT)

        elif self.state == State.ALERT:

            if ack:
                self._set(State.WARNING)

            elif risk > CRITICAL_LEVEL:
                self._set(State.PULL_OVER)

        elif self.state == State.PULL_OVER:

            # Gradual braking
            self.speed = max(0, self.speed - 10)

            if self.speed <= 5:
                self._set(State.STOPPED)

        return self.state


    def _set(self, new_state):

        print(f"\nSTATE CHANGE → {self.state} → {new_state}")
        self.state = new_state
        self.last_change = time.time()


# --------------------------------
# Instance
# --------------------------------

fsm = SafetyFSM()


# --------------------------------
# UI Helpers
# --------------------------------

def speed_bar(speed):

    blocks = int(speed / 5)
    return "█" * blocks + "-" * (16 - blocks)


def print_status():

    bar = speed_bar(fsm.speed)

    print(
        f"[{time.strftime('%H:%M:%S')}] "
        f"STATE={fsm.state:<10} "
        f"SPEED={fsm.speed:>3}km/h "
        f"RISK={fsm.last_risk:>3} "
        f"|{bar}|"
    )


def vehicle_actions(state):

    if state == State.WARNING:
        print("🔔 Action: Soft beep + dashboard alert")

    elif state == State.ALERT:
        print("🚨 Action: Loud alarm + reduce speed")
        fsm.speed = max(0, fsm.speed - 5)

    elif state == State.PULL_OVER:
        print("⚠️ Action: Hazard ON + braking")

    elif state == State.STOPPED:
        print("\n🆘 VEHICLE STOPPED | SOS SENT\n")


# --------------------------------
# API
# --------------------------------

@app.post("/control")
def control(data: dict):

    risk = data["risk"]
    ack = data["ack"]

    state = fsm.transition(risk, ack)

    vehicle_actions(state)

    print_status()

    status = {
        "state": state,
        "speed": fsm.speed,
        "risk": risk
    }

    return status
