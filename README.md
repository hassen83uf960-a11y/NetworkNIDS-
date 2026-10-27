# NIDS — AI Network Monitoring Demo

Educational university prototype using synthetic data. It does not capture live traffic, block devices, or confirm real attacks.

## Windows setup
Open CMD in this folder, then run one command at a time:

```bat
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python generate_data.py
python app.py
```

Open http://127.0.0.1:5000 in your browser. Press Ctrl+C in CMD to stop it.

## Sidebar
- Dashboard: overview and charts
- Alerts: records flagged by the model
- Traffic Monitor: all synthetic records
- Network Topology: four logical routers and illustrative BGP links (simulation only)
- Analysis: model and features
- Reports: print/save the summary as PDF
- Rules: sample alert logic
- System: component status
- Settings: demo configuration

An anomaly is not proof of an attack; it requires human review.
