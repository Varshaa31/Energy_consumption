# AI-Powered Energy Management Platform

## Quick Start Guide

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Backend Setup

1. Create a virtual environment:
```bash
python -m venv energy_env
```

2. Activate the virtual environment:
- Windows: `energy_env\Scripts\activate`
- macOS/Linux: `source energy_env/bin/activate`

3. Install dependencies:
```bash
pip install Flask==2.3.3 Flask-CORS==4.0.0 pandas==2.1.0 numpy==1.25.2 scikit-learn==1.3.0
```

4. Run the Flask backend:
```bash
python energy_backend.py
```

The backend will start on http://localhost:5000

### Frontend Access
Open the provided web application URL in your browser. The frontend will automatically connect to the Flask backend running on port 5000.

### API Endpoints

The Flask backend provides the following RESTful API endpoints:

- `GET /` - API information and available endpoints
- `GET /api/dashboard` - Real-time dashboard data
- `GET /api/appliances` - All appliances with current status
- `GET /api/historical` - Historical energy consumption data
- `GET /api/predictions` - AI-powered consumption predictions
- `GET /api/recommendations` - Energy saving recommendations
- `GET /api/gamification` - User stats, badges, and challenges
- `GET /api/analytics` - Detailed analytics and insights
- `GET /api/alerts` - System alerts and notifications
- `POST /api/control/<appliance_id>` - Control appliance status
- `GET /api/export/<data_type>` - Export data as CSV

### Features

#### Core AI Features:
✓ **Predictive Analytics** - Random Forest algorithm for energy consumption forecasting
✓ **Anomaly Detection** - Isolation Forest for identifying unusual consumption patterns
✓ **Smart Recommendations** - Context-aware energy saving suggestions
✓ **Real-time Monitoring** - Live appliance status and consumption tracking

#### Advanced Features:
✓ **Gamification System** - Points, badges, challenges, and leaderboards
✓ **Interactive Dashboard** - Real-time metrics with beautiful visualizations
✓ **Appliance Control** - Remote on/off control with immediate feedback
✓ **Comprehensive Analytics** - Detailed consumption breakdowns and insights
✓ **Goal Setting & Tracking** - Customizable energy saving targets
✓ **Data Export** - CSV export functionality for external analysis
✓ **Mobile Responsive** - Optimized for all device sizes
✓ **Dark/Light Mode** - User preference themes

#### Machine Learning Models:
- **Random Forest Regressor** - For predicting future energy consumption
- **Isolation Forest** - For detecting anomalous consumption patterns
- **Feature Engineering** - Time-based features (day of week, day of month)
- **Real-time Training** - Models update with new data

### Technical Architecture

**Backend (Python Flask):**
- RESTful API architecture
- SQLite database for data persistence
- Machine learning models for predictions and anomaly detection
- Real-time data processing and analytics

**Frontend (JavaScript/HTML/CSS):**
- Single Page Application (SPA)
- Modern responsive design with Tailwind-inspired styling
- Interactive charts using Chart.js
- Real-time data updates every 30 seconds
- Progressive Web App features

### Customization

The system can be easily extended with:
- Additional appliance types and sensors
- More sophisticated ML models (LSTM, neural networks)
- Integration with IoT devices and smart home systems
- Advanced scheduling and automation features
- Integration with utility company APIs
- Weather data integration for better predictions

### Data Sources

The platform uses sample data but is designed to integrate with:
- Smart meters and IoT sensors
- Home automation systems (Zigbee, Z-Wave, WiFi)
- Weather APIs for environmental factors
- Utility company rate schedules
- Occupancy sensors for behavioral patterns

### Security Considerations

- API endpoints use proper HTTP methods
- Input validation and sanitization
- Database prepared statements to prevent SQL injection
- CORS configuration for secure cross-origin requests
- No sensitive data stored in frontend localStorage

### Troubleshooting

**Common Issues:**

1. **Port 5000 already in use:**
   - Change port in energy_backend.py: `app.run(debug=True, host='0.0.0.0', port=5001)`

2. **Module not found errors:**
   - Ensure virtual environment is activated
   - Install all requirements: `pip install -r requirements.txt`

3. **CORS errors:**
   - Verify Flask-CORS is installed
   - Check that backend is running on expected port

4. **Database errors:**
   - Delete energy_management.db file to reset database
   - Restart the Flask application

### Future Enhancements

**Phase 2 Features (Suggested):**
- Machine learning model retraining pipeline
- Advanced scheduling and automation
- Integration with smart home platforms (Alexa, Google Home)
- Mobile app development
- Multi-user support with authentication
- Cloud deployment and scaling
- Integration with renewable energy sources
- Predictive maintenance algorithms
- Advanced reporting and compliance features
- API for third-party integrations
