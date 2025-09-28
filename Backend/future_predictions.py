import json
import datetime
from datetime import timedelta
import random
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor, IsolationForest
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)

class EnergyManagementSystem:
    def __init__(self):
        self.appliances = []
        self.historical_data = []
        self.load_sample_data()
        self.init_database()
        self.prediction_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        self.train_models()

    def load_sample_data(self):
        """Load sample data from JSON file"""
        try:
            with open('energy_data.json', 'r') as f:
                data = json.load(f)
                self.appliances = data['appliances']
                self.historical_data = data['historical_data']
        except FileNotFoundError:
            self.generate_sample_data()

    def generate_sample_data(self):
        """Generate sample appliance and historical data"""
        self.appliances = [
            {"id": 1, "name": "Smart AC", "type": "HVAC", "power_rating": 3500, "status": "on"},
            {"id": 2, "name": "LED Lights", "type": "Lighting", "power_rating": 150, "status": "on"},
            {"id": 3, "name": "Refrigerator", "type": "Kitchen", "power_rating": 400, "status": "on"},
            {"id": 4, "name": "Smart TV", "type": "Entertainment", "power_rating": 250, "status": "off"},
            {"id": 5, "name": "Water Heater", "type": "Utility", "power_rating": 4500, "status": "on"}
        ]

        self.historical_data = []
        base_date = datetime.datetime.now() - timedelta(days=30)
        for i in range(30):
            current_date = base_date + timedelta(days=i)
            consumption = 45 + random.uniform(-10, 15)
            self.historical_data.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "consumption": round(consumption, 2),
                "cost": round(consumption * 0.12, 2),
                "carbon_footprint": round(consumption * 0.4, 2)
            })

    def init_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect('energy_management.db')
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS energy_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                appliance_id INTEGER,
                power_consumption REAL,
                status TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                goal_type TEXT,
                target_value REAL,
                current_value REAL,
                created_at TEXT
            )
        """)

        conn.commit()
        conn.close()

    def train_models(self):
        """Train AI models for prediction and anomaly detection"""
        if len(self.historical_data) < 7:
            return

        df = pd.DataFrame(self.historical_data)
        df['date'] = pd.to_datetime(df['date'])
        df['day_of_week'] = df['date'].dt.dayofweek
        df['day_of_month'] = df['date'].dt.day

        features = ['day_of_week', 'day_of_month']
        X = df[features].values
        y = df['consumption'].values

        self.prediction_model.fit(X, y)

        consumption_reshaped = df['consumption'].values.reshape(-1, 1)
        self.anomaly_detector.fit(consumption_reshaped)

    def predict_consumption(self, days_ahead=1):
        """Predict energy consumption for future days"""
        future_date = datetime.datetime.now() + timedelta(days=days_ahead)
        features = [future_date.weekday(), future_date.day]

        try:
            prediction = self.prediction_model.predict([features])[0]
            return max(0, prediction)
        except:
            recent_avg = np.mean([d['consumption'] for d in self.historical_data[-7:]])
            return recent_avg

    def detect_anomalies(self, consumption_value):
        """Detect if current consumption is anomalous"""
        try:
            anomaly_score = self.anomaly_detector.decision_function([[consumption_value]])[0]
            is_anomaly = self.anomaly_detector.predict([[consumption_value]])[0] == -1
            return {"is_anomaly": is_anomaly, "score": anomaly_score}
        except:
            return {"is_anomaly": False, "score": 0}

    def generate_recommendations(self):
        """Generate AI-powered energy saving recommendations"""
        recommendations = []
        current_hour = datetime.datetime.now().hour

        if current_hour > 22 or current_hour < 6:
            recommendations.append({
                "type": "scheduling",
                "title": "Night Mode Optimization",
                "description": "Consider reducing AC temperature by 2°C during sleeping hours",
                "potential_savings": "12-15%",
                "difficulty": "easy"
            })

        if 14 <= current_hour <= 18:
            recommendations.append({
                "type": "load_shifting",
                "title": "Peak Hour Load Shifting",
                "description": "Delay washing machine and dishwasher until after 6 PM",
                "potential_savings": "8-10%",
                "difficulty": "medium"
            })

        for appliance in self.appliances:
            if appliance['type'] == 'HVAC' and appliance['status'] == 'on':
                recommendations.append({
                    "type": "efficiency",
                    "title": f"Optimize {appliance['name']}",
                    "description": "Use programmable schedules and adjust setpoints based on occupancy",
                    "potential_savings": "15-20%",
                    "difficulty": "easy"
                })

        return recommendations[:5]

    def calculate_carbon_footprint(self, consumption_kwh):
        """Calculate carbon footprint based on energy consumption"""
        return round(consumption_kwh * 0.4, 2)

    def get_efficiency_score(self, current_consumption, historical_avg):
        """Calculate efficiency score based on consumption patterns"""
        if historical_avg == 0:
            return 50

        efficiency = max(0, (historical_avg - current_consumption) / historical_avg * 100)
        return min(100, max(0, 100 - efficiency))

# Initialize the energy management system
ems = EnergyManagementSystem()

@app.route('/')
def home():
    """Home page with basic info"""
    return jsonify({
        "message": "AI-Powered Energy Management System API",
        "version": "1.0.0",
        "endpoints": [
            "/api/dashboard",
            "/api/appliances", 
            "/api/predictions",
            "/api/recommendations",
            "/api/gamification",
            "/api/control/<appliance_id>"
        ]
    })

@app.route('/api/dashboard')
def dashboard():
    """Main dashboard data endpoint"""
    current_time = datetime.datetime.now()

    active_appliances = [a for a in ems.appliances if a['status'] == 'on']
    current_consumption = sum(a['power_rating'] for a in active_appliances) / 1000

    recent_data = ems.historical_data[-7:] if len(ems.historical_data) >= 7 else ems.historical_data
    historical_avg = np.mean([d['consumption'] for d in recent_data]) if recent_data else 45

    anomaly_result = ems.detect_anomalies(current_consumption)

    dashboard_data = {
        "timestamp": current_time.isoformat(),
        "current_consumption": round(current_consumption, 2),
        "active_appliances": len(active_appliances),
        "total_appliances": len(ems.appliances),
        "estimated_daily_cost": round(current_consumption * 24 * 0.12, 2),
        "efficiency_score": ems.get_efficiency_score(current_consumption, historical_avg),
        "carbon_footprint_today": ems.calculate_carbon_footprint(current_consumption * 24),
        "anomaly_detected": anomaly_result["is_anomaly"],
        "weather": {
            "temperature": 24 + random.uniform(-3, 3),
            "humidity": 60 + random.uniform(-10, 15),
            "condition": random.choice(["sunny", "cloudy", "partly_cloudy", "rainy"])
        }
    }

    return jsonify(dashboard_data)

@app.route('/api/appliances')
def get_appliances():
    """Get all appliances with current status and consumption"""
    appliances_data = []

    for appliance in ems.appliances:
        base_consumption = appliance['power_rating'] if appliance['status'] == 'on' else 0
        current_consumption = base_consumption + random.uniform(-50, 50) if base_consumption > 0 else 0
        current_consumption = max(0, current_consumption)

        appliances_data.append({
            **appliance,
            "current_consumption": round(current_consumption, 2),
            "daily_usage_hours": random.uniform(4, 16) if appliance['status'] == 'on' else 0,
            "estimated_daily_cost": round(current_consumption * 24 * 0.12 / 1000, 2),
            "efficiency_rating": random.choice(['A++', 'A+', 'A', 'B', 'C'])
        })

    return jsonify(appliances_data)

@app.route('/api/historical')
def get_historical_data():
    """Get historical energy consumption data"""
    return jsonify({
        "data": ems.historical_data,
        "summary": {
            "total_consumption": sum(d['consumption'] for d in ems.historical_data),
            "average_daily": np.mean([d['consumption'] for d in ems.historical_data]),
            "total_cost": sum(d['cost'] for d in ems.historical_data),
            "total_carbon": sum(d['carbon_footprint'] for d in ems.historical_data)
        }
    })

@app.route('/api/predictions')
def get_predictions():
    """Get AI-powered consumption predictions"""
    predictions = {
        "next_day": ems.predict_consumption(1),
        "next_week": ems.predict_consumption(7),
        "next_month": ems.predict_consumption(30),
        "confidence_interval": {
            "lower": ems.predict_consumption(1) * 0.85,
            "upper": ems.predict_consumption(1) * 1.15
        },
        "trending": "stable",
        "factors": [
            "Weather patterns suggest 15% increase in AC usage",
            "Weekend consumption typically 20% higher",
            "Recent efficiency improvements showing 8% reduction"
        ]
    }

    return jsonify(predictions)

@app.route('/api/recommendations')
def get_recommendations():
    """Get AI-generated energy saving recommendations"""
    recommendations = ems.generate_recommendations()

    return jsonify({
        "recommendations": recommendations,
        "total_potential_savings": "25-35%",
        "estimated_cost_reduction": "$45-65/month"
    })

@app.route('/api/gamification')
def get_gamification_data():
    """Get gamification data including points, badges, challenges"""
    recent_avg = np.mean([d['consumption'] for d in ems.historical_data[-7:]])
    current_consumption = sum(a['power_rating'] for a in ems.appliances if a['status'] == 'on') / 1000
    efficiency_bonus = max(0, (recent_avg - current_consumption) * 10)

    gamification_data = {
        "user_stats": {
            "level": 7,
            "points": 2450 + int(efficiency_bonus),
            "points_to_next_level": 550,
            "streak_days": 12
        },
        "badges": [
            {"id": 1, "name": "Energy Saver", "description": "Reduced consumption by 10%", "earned": True},
            {"id": 2, "name": "Peak Avoider", "description": "Avoid peak hour usage", "earned": True},
            {"id": 3, "name": "Smart Scheduler", "description": "Use automated scheduling", "earned": False},
            {"id": 4, "name": "Carbon Warrior", "description": "Reduce carbon footprint by 20%", "earned": False}
        ],
        "active_challenges": [
            {
                "id": 1,
                "name": "Weekend Energy Challenge",
                "description": "Keep weekend consumption below weekday average",
                "progress": 75,
                "max_progress": 100,
                "reward_points": 150,
                "expires_at": (datetime.datetime.now() + timedelta(days=2)).isoformat()
            },
            {
                "id": 2,
                "name": "Off-Peak Champion",
                "description": "Use 80% of energy during off-peak hours",
                "progress": 45,
                "max_progress": 100,
                "reward_points": 200,
                "expires_at": (datetime.datetime.now() + timedelta(days=5)).isoformat()
            }
        ],
        "leaderboard": {
            "user_position": 12,
            "total_users": 150,
            "top_users": [
                {"rank": 1, "name": "EcoWarrior123", "points": 5280},
                {"rank": 2, "name": "GreenGuru", "points": 4950},
                {"rank": 3, "name": "EnergyMaster", "points": 4720}
            ]
        }
    }

    return jsonify(gamification_data)

@app.route('/api/control/<int:appliance_id>', methods=['POST'])
def control_appliance(appliance_id):
    """Control appliance (turn on/off)"""
    try:
        data = request.get_json()
        action = data.get('action')

        appliance = next((a for a in ems.appliances if a['id'] == appliance_id), None)
        if not appliance:
            return jsonify({"error": "Appliance not found"}), 404

        old_status = appliance['status']
        appliance['status'] = action

        conn = sqlite3.connect('energy_management.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO energy_logs (timestamp, appliance_id, power_consumption, status)
            VALUES (?, ?, ?, ?)
        """, (
            datetime.datetime.now().isoformat(),
            appliance_id,
            appliance['power_rating'] if action == 'on' else 0,
            action
        ))
        conn.commit()
        conn.close()

        return jsonify({
            "success": True,
            "message": f"{appliance['name']} turned {action}",
            "appliance": appliance,
            "previous_status": old_status
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analytics')
def get_analytics():
    """Get detailed analytics and insights"""
    total_consumption = sum(d['consumption'] for d in ems.historical_data)
    avg_daily = np.mean([d['consumption'] for d in ems.historical_data])

    consumption_by_type = {}
    for appliance in ems.appliances:
        appliance_type = appliance['type']
        if appliance_type not in consumption_by_type:
            consumption_by_type[appliance_type] = 0
        if appliance['status'] == 'on':
            consumption_by_type[appliance_type] += appliance['power_rating']

    analytics_data = {
        "consumption_summary": {
            "total_monthly": round(total_consumption, 2),
            "average_daily": round(avg_daily, 2),
            "peak_day": max(ems.historical_data, key=lambda x: x['consumption'])['date'],
            "lowest_day": min(ems.historical_data, key=lambda x: x['consumption'])['date']
        },
        "consumption_by_type": consumption_by_type,
        "cost_analysis": {
            "total_cost": round(sum(d['cost'] for d in ems.historical_data), 2),
            "average_daily_cost": round(avg_daily * 0.12, 2),
            "projected_monthly": round(avg_daily * 30 * 0.12, 2)
        },
        "environmental_impact": {
            "total_carbon": round(sum(d['carbon_footprint'] for d in ems.historical_data), 2),
            "daily_average_carbon": round(np.mean([d['carbon_footprint'] for d in ems.historical_data]), 2),
            "trees_equivalent": round(sum(d['carbon_footprint'] for d in ems.historical_data) / 21.77, 1)
        }
    }

    return jsonify(analytics_data)

@app.route('/api/alerts')
def get_alerts():
    """Get system alerts and notifications"""
    alerts = []

    current_consumption = sum(a['power_rating'] for a in ems.appliances if a['status'] == 'on') / 1000
    avg_consumption = np.mean([d['consumption'] for d in ems.historical_data[-7:]])

    if current_consumption > avg_consumption * 1.3:
        alerts.append({
            "id": 1,
            "type": "warning",
            "title": "High Energy Consumption Detected",
            "message": "Current consumption is 30% above normal. Consider turning off non-essential appliances.",
            "timestamp": datetime.datetime.now().isoformat(),
            "actionable": True
        })

    for appliance in ems.appliances:
        if appliance['status'] == 'on' and appliance['type'] in ['Entertainment', 'Kitchen']:
            if datetime.datetime.now().hour > 23 or datetime.datetime.now().hour < 6:
                alerts.append({
                    "id": len(alerts) + 1,
                    "type": "info",
                    "title": f"{appliance['name']} Still Running",
                    "message": f"Consider turning off {appliance['name']} to save energy during off-hours.",
                    "timestamp": datetime.datetime.now().isoformat(),
                    "actionable": True,
                    "appliance_id": appliance['id']
                })

    alerts.append({
        "id": len(alerts) + 1,
        "type": "maintenance",
        "title": "AC Filter Maintenance",
        "message": "Smart AC filter may need cleaning. Clean filters improve efficiency by 15%.",
        "timestamp": datetime.datetime.now().isoformat(),
        "actionable": False
    })

    return jsonify({"alerts": alerts, "total_count": len(alerts)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
