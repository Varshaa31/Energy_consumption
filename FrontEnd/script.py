# Create a comprehensive data structure with sample energy data for the AI platform
import json
import random
import datetime
from datetime import timedelta

# Generate sample appliance data
appliances = [
    {"id": 1, "name": "Smart AC", "type": "HVAC", "power_rating": 3500, "status": "on"},
    {"id": 2, "name": "LED Lights Living Room", "type": "Lighting", "power_rating": 150, "status": "on"},
    {"id": 3, "name": "Refrigerator", "type": "Kitchen", "power_rating": 400, "status": "on"},
    {"id": 4, "name": "Smart TV", "type": "Entertainment", "power_rating": 250, "status": "off"},
    {"id": 5, "name": "Washing Machine", "type": "Appliance", "power_rating": 2000, "status": "off"},
    {"id": 6, "name": "Water Heater", "type": "Utility", "power_rating": 4500, "status": "on"},
    {"id": 7, "name": "Dishwasher", "type": "Kitchen", "power_rating": 1800, "status": "off"},
    {"id": 8, "name": "Smart Thermostat", "type": "HVAC", "power_rating": 50, "status": "on"},
    {"id": 9, "name": "LED Lights Bedroom", "type": "Lighting", "power_rating": 100, "status": "on"},
    {"id": 10, "name": "Desktop Computer", "type": "Electronics", "power_rating": 500, "status": "on"}
]

# Generate historical energy consumption data (last 30 days)
historical_data = []
base_date = datetime.datetime.now() - timedelta(days=30)

for i in range(30):
    current_date = base_date + timedelta(days=i)
    # Simulate daily energy consumption with variations
    base_consumption = 45 + random.uniform(-10, 15)  # kWh per day
    
    # Add seasonal/time patterns
    if current_date.weekday() >= 5:  # Weekend
        base_consumption *= 1.2
    
    historical_data.append({
        "date": current_date.strftime("%Y-%m-%d"),
        "consumption": round(base_consumption, 2),
        "cost": round(base_consumption * 0.12, 2),  # $0.12 per kWh
        "carbon_footprint": round(base_consumption * 0.4, 2),  # 0.4 kg CO2 per kWh
        "peak_hours_usage": round(base_consumption * 0.3, 2),
        "efficiency_score": random.randint(65, 95)
    })

# Generate real-time data
current_hour_data = {
    "timestamp": datetime.datetime.now().isoformat(),
    "total_power": 8950,  # Total watts currently being used
    "active_appliances": 6,
    "estimated_daily_cost": 6.24,
    "current_efficiency": 78,
    "weather": {
        "temperature": 24,
        "humidity": 65,
        "condition": "partly_cloudy"
    }
}

# Generate AI predictions and recommendations
predictions = {
    "next_day_consumption": 48.5,
    "next_week_average": 46.2,
    "monthly_projection": 1420,
    "cost_savings_potential": 15.8,
    "efficiency_improvements": [
        {
            "appliance": "Smart AC",
            "current_efficiency": 72,
            "recommended_action": "Adjust temperature to 25°C during 2-6 PM",
            "potential_savings": 8.5
        },
        {
            "appliance": "Water Heater",
            "current_efficiency": 65,
            "recommended_action": "Schedule heating during off-peak hours",
            "potential_savings": 12.3
        }
    ]
}

# Generate anomaly detection data
anomalies = [
    {
        "timestamp": "2025-09-27T14:30:00",
        "appliance": "Smart AC",
        "type": "unusual_spike",
        "severity": "medium",
        "description": "Power consumption 40% higher than normal for this time period"
    },
    {
        "timestamp": "2025-09-26T22:15:00",
        "appliance": "Washing Machine",
        "type": "idle_consumption",
        "severity": "low",
        "description": "Consuming 15W while in standby mode"
    }
]

# Generate gamification data
gamification = {
    "user_level": 7,
    "points_earned": 2450,
    "badges": [
        {"name": "Energy Saver", "description": "Reduced consumption by 10% this month"},
        {"name": "Peak Hour Avoider", "description": "Shifted 70% of usage to off-peak hours"},
        {"name": "Smart Scheduler", "description": "Used automated scheduling for 15 days"}
    ],
    "challenges": [
        {
            "name": "Weekend Energy Challenge",
            "description": "Keep weekend consumption below weekday average",
            "progress": 75,
            "reward": 150
        },
        {
            "name": "Off-Peak Champion",
            "description": "Use 80% of daily energy during off-peak hours",
            "progress": 45,
            "reward": 200
        }
    ],
    "leaderboard_position": 12,
    "total_users": 150
}

# Compile all data
complete_data = {
    "appliances": appliances,
    "historical_data": historical_data,
    "real_time": current_hour_data,
    "predictions": predictions,
    "anomalies": anomalies,
    "gamification": gamification
}

# Convert to JSON and save
json_data = json.dumps(complete_data, indent=2)
print("Sample data structure created successfully!")
print(f"Total appliances: {len(appliances)}")
print(f"Historical data points: {len(historical_data)}")
print(f"Anomalies detected: {len(anomalies)}")
print(f"Active challenges: {len(gamification['challenges'])}")

# Save to file for the web app
with open('energy_data.json', 'w') as f:
    f.write(json_data)

print("\nData saved to 'energy_data.json'")