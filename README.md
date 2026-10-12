# Smart Irrigation Prediction System (Full Stack)

A student project prototype with:
- **Frontend:** HTML, CSS, JavaScript dashboard
- **Backend:** Python Flask REST API
- **Prediction:** transparent rule-based demonstration logic
- **Storage:** JSON file for recent prediction history
- **Pump control:** simulated UI/API state only (no real hardware connected)

## Run locally

1. Install Python 3.10+.
2. Open a terminal in this project folder.
3. Create and activate a virtual environment (recommended):
   - Windows: `py -m venv .venv` then `.venv\Scripts\activate`
   - macOS/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Start the server: `python app.py`
6. Open `http://127.0.0.1:5000` in your browser.

## API endpoints

- `GET /` — dashboard page
- `POST /api/predict` — accepts moisture, temperature, humidity, rain_expected and returns an irrigation recommendation
- `GET /api/history` — latest saved prediction records
- `POST /api/pump` — updates a simulated pump state

Example prediction request JSON:
```json
{
  "moisture": 24,
  "temperature": 31,
  "humidity": 48,
  "rain_expected": false
}
```

## Important project note

This is a **working full-stack demonstration**, not a validated agricultural ML model. The current backend uses understandable rules so the project runs without a dataset. To accurately claim machine-learning prediction, train and evaluate a model on labelled crop/soil/weather data, then replace `predict_irrigation()` with the trained model. The pump toggle is simulated. Do not connect this directly to mains electricity or real irrigation equipment without suitable hardware, isolation, fail-safe logic, and supervision.
