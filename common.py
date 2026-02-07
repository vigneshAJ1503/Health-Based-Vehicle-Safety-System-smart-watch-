# common.py

# Sliding window
WINDOW_SIZE = 15        # last 30s (2s interval)

# Risk thresholds
WARN_LEVEL = 30
ALERT_LEVEL = 50
CRITICAL_LEVEL = 70

# Network
GATEWAY_URL = "http://localhost:8000/health"
RISK_URL = "http://localhost:7000/risk"
TCU_URL = "http://localhost:9000/control"

# Timing
SEND_INTERVAL = 1
ACK_TIMEOUT = 10
