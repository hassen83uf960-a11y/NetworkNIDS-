"""Score synthetic network-flow records with an Isolation Forest model."""
from pathlib import Path
import csv
from sklearn.ensemble import IsolationForest

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "network_flows.csv"
FEATURES = ["duration_ms", "bytes_sent", "packets", "unique_ports", "failed_connections"]

def load_and_score_flows():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Demo data file not found: {DATA_FILE}. Run: python generate_data.py")
    with DATA_FILE.open("r", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return []
    X = [[float(row[k]) for k in FEATURES] for row in rows]
    model = IsolationForest(n_estimators=120, contamination=0.12, random_state=42)
    predictions = model.fit_predict(X)
    scores = model.decision_function(X)
    result = []
    attack_cycle = ["ARP Spoofing", "Malware Beaconing", "DDoS", "Brute Force", "Port Scan", "Data Exfiltration"]
    flagged_index = 0
    for row, prediction, score in zip(rows, predictions, scores):
        flagged = prediction == -1
        # Demo-only priority rule, for explaining alert severity in class.
        high = flagged and (int(row["failed_connections"]) >= 8 or int(row["unique_ports"]) >= 18 or int(row["bytes_sent"]) >= 180000)
        attack_type = "None — normal traffic"
        if flagged:
            # Synthetic label for the university demo; it is an illustrative guess, not proof.
            if int(row["unique_ports"]) >= 18:
                attack_type = "Port Scan"
            elif int(row["failed_connections"]) >= 15:
                attack_type = "Brute Force"
            elif int(row["bytes_sent"]) >= 900000:
                attack_type = "Data Exfiltration"
            elif int(row["packets"]) >= 1500:
                attack_type = "DDoS"
            else:
                attack_type = attack_cycle[flagged_index % len(attack_cycle)]
            flagged_index += 1
        row.update({
            "attack_type": attack_type,
            "duration_ms": int(row["duration_ms"]), "bytes_sent": int(row["bytes_sent"]),
            "packets": int(row["packets"]), "unique_ports": int(row["unique_ports"]),
            "failed_connections": int(row["failed_connections"]),
            "is_anomaly": bool(flagged), "severity": "High" if high else ("Medium" if flagged else "Normal"),
            "label": "Unusual" if flagged else "Normal", "anomaly_score": round(float(score), 4)
        })
        result.append(row)
    return result
