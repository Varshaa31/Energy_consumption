from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
import io
import base64

from backend.app.anamaly_detection import EnergyAnalyzer  # Changed to direct import

app = Flask(__name__)

# --------- Sample Historical Data (Replace with real dataset) ----------
np.random.seed(42)
data = pd.DataFrame({
    'Timestamp': pd.date_range(start='2025-09-01', periods=100, freq='H'),
    'Total_Energy_kWh': np.random.rand(100) * 2 + 0.5,
    'Temperature_C': np.random.rand(100) * 10 + 15
})

# Feature Engineering
data['Hour'] = data['Timestamp'].dt.hour
data['DayOfWeek'] = data['Timestamp'].dt.dayofweek
data['Month'] = data['Timestamp'].dt.month

features = ['Hour', 'DayOfWeek', 'Month', 'Temperature_C']
X = data[features]
y = data['Total_Energy_kWh']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
preds_test = model.predict(X_test)
print('Initial MAE:', mean_absolute_error(y_test, preds_test))

# Create energy analyzer instance
energy_analyzer = EnergyAnalyzer()

# Helper: Generate consumption comparison chart (base64 image)
def generate_consumption_chart(timestamps, actual, predicted):
    plt.figure(figsize=(10,5))
    plt.plot(timestamps, actual, label='Actual')
    plt.plot(timestamps, predicted, label='Predicted', linestyle='dashed')
    plt.xlabel('Timestamp')
    plt.ylabel('Energy Consumption (kWh)')
    plt.title('Actual vs Predicted Energy Consumption')
    plt.legend()
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    return img_base64

# Helper: Generate recommendations based on hour and predicted vs historical average consumption
def generate_recommendation(hour, predicted, historical_avg, threshold=1.2):
    recommendations = []
    if predicted > historical_avg * threshold:
        recommendations.append(f"Energy usage is {predicted/historical_avg:.2f} times higher than usual at hour {hour}.")
        if 18 <= hour <= 22:
            recommendations.append("Try shifting heavy appliance use to off-peak hours before 6 PM or after 10 PM.")
        else:
            recommendations.append("Consider turning off unused devices or check for appliance faults.")
    else:
        recommendations.append("Energy use is within normal limits. Keep up the good habits!")
    return recommendations

@app.route('/energy_analysis', methods=['POST'])
def analyze_energy():
    """
    Expects JSON:
    {
        "timestamp": "2025-09-27T19:00:00",
        "temperature_c": 23.5
    }
    Responds with predicted consumption, recommendations, and consumption chart image.
    """
    input_json = request.get_json()

    try:
        timestamp = pd.to_datetime(input_json['timestamp'])
        temperature_c = float(input_json['temperature_c'])
    except (KeyError, ValueError):
        return jsonify({"error": "Provide valid 'timestamp' and 'temperature_c' fields"}), 400
    
    hour = timestamp.hour
    dayofweek = timestamp.dayofweek
    month = timestamp.month
    
    # Predict energy consumption
    features_input = np.array([[hour, dayofweek, month, temperature_c]])
    predicted_energy = model.predict(features_input)[0]
    
    # Calculate historical average consumption for this hour to compare
    hist_avg = data.loc[data['Hour'] == hour, 'Total_Energy_kWh'].mean()

    # Generate recommendations
    recs = generate_recommendation(hour, predicted_energy, hist_avg)
    
    # Analyze patterns and anomalies
    recent_data = pd.DataFrame({
        'hour_of_day': [hour],
        'energy_usage': [predicted_energy]
    })
    
    analysis_results = energy_analyzer.analyze(recent_data)
    
    # Check for anomalies
    anomaly_detected = analysis_results['anomalies'][0] == -1
    if anomaly_detected:
        recs.append("ALERT: Unusual energy consumption pattern detected!")
        if predicted_energy > hist_avg:
            recs.append("Energy usage is significantly higher than expected. Please check for malfunctioning equipment.")
        else:
            recs.append("Energy usage is significantly lower than expected. This might indicate equipment shutdown or malfunction.")
    
    # Generate chart for last 24 hours from historical data
    last_24h = data.tail(24)
    preds_hist = model.predict(last_24h[features].values)
    chart_base64 = generate_consumption_chart(
        last_24h['Timestamp'].dt.strftime('%Y-%m-%d %H:%M'),
        last_24h['Total_Energy_kWh'],
        preds_hist
    )
    
    return jsonify({
        "predicted_energy_kwh": round(predicted_energy, 3),
        "recommendations": recs,
        "consumption_chart_base64": chart_base64,
        "anomaly_detected": anomaly_detected,
        "pattern_cluster": analysis_results['clusters'][0]
    })

if __name__ == '__main__':
    app.run(debug=True)
    app.run(debug=True)
