"""Generate fictional flow records for the educational dashboard."""
from pathlib import Path
import csv, random
from datetime import datetime, timedelta

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "data" / "network_flows.csv"
FIELDS = ["timestamp", "source_ip", "destination_ip", "protocol", "duration_ms", "bytes_sent", "packets", "unique_ports", "failed_connections"]

def main():
    random.seed(42)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    rows=[]
    start=datetime(2026,10,20,8,0,0)
    for i in range(120):
        unusual = i % 9 == 0
        source=f"192.168.1.{random.randint(2,240)}"
        dest=f"10.0.0.{random.randint(2,100)}"
        if unusual:
            duration=random.randint(500,18000); bytes_sent=random.randint(90000,350000)
            packets=random.randint(300,1800); ports=random.randint(12,30); failed=random.randint(4,18)
        else:
            duration=random.randint(5,2200); bytes_sent=random.randint(200,45000)
            packets=random.randint(2,180); ports=random.randint(1,5); failed=random.randint(0,3)
        rows.append({"timestamp":(start+timedelta(minutes=i*7)).strftime("%Y-%m-%d %H:%M:%S"),"source_ip":source,"destination_ip":dest,"protocol":random.choice(["TCP","UDP","DNS","HTTP"]),"duration_ms":duration,"bytes_sent":bytes_sent,"packets":packets,"unique_ports":ports,"failed_connections":failed})
    with OUT.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=FIELDS); writer.writeheader(); writer.writerows(rows)
    print(f"Created {len(rows)} synthetic records: {OUT}")

if __name__ == "__main__": main()
