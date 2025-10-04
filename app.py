from flask import Flask, jsonify, request
from flask_cors import CORS
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)  # CORS'u etkinleştir

@app.route('/api/air-quality', methods=['GET'])
def get_air_quality():
    # Gerçek sensör verilerinizi buraya entegre edin
    data = {
        "aqi": random.randint(0, 500),
        "dominant_pollutant": "pm25",
        "pm25": round(random.uniform(0, 300), 1),
        "pm10": round(random.uniform(0, 400), 1),
        "o3": round(random.uniform(0, 0.5), 3),
        "no2": round(random.uniform(0, 0.3), 3),
        "timestamp": datetime.now().isoformat(),
        "location": "Istanbul"
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
import math
from typing import Dict, Any

def calculate_aqi_epa(pollutants: Dict[str, float]) -> Dict[str, Any]:
    """
    US EPA AQI hesaplama fonksiyonu (Python versiyonu)
    """
    AQI_BREAKPOINTS = {
        'pm25': [
            (0, 12.0, 0, 50),
            (12.1, 35.4, 51, 100),
            (35.5, 55.4, 101, 150),
            (55.5, 150.4, 151, 200),
            (150.5, 250.4, 201, 300),
            (250.5, 500.4, 301, 500)
        ],
        'pm10': [
            (0, 54, 0, 50),
            (55, 154, 51, 100),
            (155, 254, 101, 150),
            (255, 354, 151, 200),
            (355, 424, 201, 300),
            (425, 604, 301, 500)
        ],
        'o3': [
            (0, 0.054, 0, 50),
            (0.055, 0.070, 51, 100),
            (0.071, 0.085, 101, 150),
            (0.086, 0.105, 151, 200),
            (0.106, 0.200, 201, 300)
        ],
        'no2': [
            (0, 0.053, 0, 50),
            (0.054, 0.100, 51, 100),
            (0.101, 0.360, 101, 150),
            (0.361, 0.649, 151, 200),
            (0.650, 1.249, 201, 300),
            (1.250, 2.049, 301, 500)
        ]
    }
    
    max_aqi = 0
    dominant_pollutant = ''
    
    for pollutant, value in pollutants.items():
        if pollutant in AQI_BREAKPOINTS and value is not None:
            breakpoints = AQI_BREAKPOINTS[pollutant]
            
            for bp_min, bp_max, i_min, i_max in breakpoints:
                if bp_min <= value <= bp_max:
                    # AQI formülü
                    aqi = ((i_max - i_min) / (bp_max - bp_min)) * (value - bp_min) + i_min
                    aqi = round(aqi)
                    
                    if aqi > max_aqi:
                        max_aqi = aqi
                        dominant_pollutant = pollutant
                    break
    
    return {
        'aqi': max_aqi,
        'dominant_pollutant': dominant_pollutant,
        'pollutants': pollutants
    }

# Kullanım örneği:
pollutant_data = {
    'pm25': 45.6,
    'pm10': 120.3,
    'o3': 0.062,
    'no2': 0.085
}

aqi_result = calculate_aqi_epa(pollutant_data)
print(f"AQI: {aqi_result['aqi']}")
print(f"Dominant Pollutant: {aqi_result['dominant_pollutant']}")