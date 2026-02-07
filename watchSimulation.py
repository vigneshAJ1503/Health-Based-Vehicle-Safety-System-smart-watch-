# watch_simulator.py

import time
import requests
import argparse
from common import GATEWAY_URL, SEND_INTERVAL


# --------------------------------
# Scenario Definitions
# --------------------------------

SCENARIOS = {

    "S1": {
        "name": "NORMAL",
        "pattern": [(75, False)] * 15
    },

    "S2": {
        "name": "SPIKE",
        "pattern": (
            [(75, False)] * 7 +
            [(165, False)] * 1 +
            [(75, False)] * 7
        )
    },

    "S3": {
        "name": "SUSTAINED_HIGH",
        "pattern": (
            [(85, False)] * 10 +
            [(150, False)] * 35
        )
    },

    "S4": {
        "name": "RECOVERY_ACK",
        "pattern": (
            [(150, False)] * 7 +
            [(150, True)] * 4 +
            [(80, True)] * 4
        )
    },

    "S5": {
        "name": "CRITICAL",
        "pattern": (
            [(90, False)] * 3 +
            [(180, False)] * 12
        )
    },

    "S6": {
        "name": "FLAPPING",
        "pattern": (
            [(70, False), (150, False)] * 8
        )
    }
}


# --------------------------------
# Sender
# --------------------------------

def send(bpm, ack):

    payload = {
        "driver_id": "DRV001",
        "bpm": bpm,
        "ack": ack,
        "ts": time.time()
    }

    try:
        requests.post(GATEWAY_URL, json=payload, timeout=2)
        print(f"Sent → BPM:{bpm} ACK:{ack}")

    except Exception as e:
        print("Send failed:", e)


# --------------------------------
# Runner
# --------------------------------

def run_scenario(sid, scenario):

    print("\n" + "=" * 60)
    print(f"▶ Running {sid} : {scenario['name']}")
    print("=" * 60)

    for bpm, ack in scenario["pattern"]:
        send(bpm, ack)
        time.sleep(SEND_INTERVAL)

    print(f"✔ Completed {sid}\n")


# --------------------------------
# CLI
# --------------------------------

def parse_args():

    parser = argparse.ArgumentParser(
        description="Health-Car Watch Simulator"
    )

    parser.add_argument(
        "--scenario",
        type=str,
        help="Scenario ID (S1–S6, ALL)"
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="List available scenarios"
    )

    return parser.parse_args()


# --------------------------------
# Main
# --------------------------------

def main():

    args = parse_args()

    # List Mode
    if args.list:

        print("\nAvailable Scenarios:\n")

        for k, v in SCENARIOS.items():
            print(f"{k} → {v['name']}")

        print()
        return


    # No Scenario Provided
    if not args.scenario:

        print("❌ Please specify --scenario or --list")
        return


    # Run All
    if args.scenario.upper() == "ALL":

        print("\n🚗 Running ALL scenarios\n")

        for sid, scenario in SCENARIOS.items():
            run_scenario(sid, scenario)

        print("✅ All completed")
        return


    # Run Single
    sid = args.scenario.upper()

    if sid not in SCENARIOS:

        print(f"❌ Invalid scenario: {sid}")
        print("Use --list to see valid options")
        return


    run_scenario(sid, SCENARIOS[sid])


if __name__ == "__main__":
    main()


#python watchSimulation.py --list

# S1 → NORMAL
# S2 → SPIKE
# S3 → SUSTAINED_HIGH
# S4 → RECOVERY_ACK
# S5 → CRITICAL
# S6 → FLAPPING


# python watchSimulation.py --scenario S3
