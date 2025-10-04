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
/**
 * US EPA AQI hesaplama fonksiyonu
 * Her kirletici için ayrı ayrı hesaplanır, en yüksek değer genel AQI olur
 */
function calculateUSEPAAQI(pollutants) {
    // EPA AQI aralıkları ve formülleri
    const AQI_BREAKPOINTS = {
        pm25: [
            { min: 0, max: 12.0, iMin: 0, iMax: 50 },
            { min: 12.1, max: 35.4, iMin: 51, iMax: 100 },
            { min: 35.5, max: 55.4, iMin: 101, iMax: 150 },
            { min: 55.5, max: 150.4, iMin: 151, iMax: 200 },
            { min: 150.5, max: 250.4, iMin: 201, iMax: 300 },
            { min: 250.5, max: 500.4, iMin: 301, iMax: 500 }
        ],
        pm10: [
            { min: 0, max: 54, iMin: 0, iMax: 50 },
            { min: 55, max: 154, iMin: 51, iMax: 100 },
            { min: 155, max: 254, iMin: 101, iMax: 150 },
            { min: 255, max: 354, iMin: 151, iMax: 200 },
            { min: 355, max: 424, iMin: 201, iMax: 300 },
            { min: 425, max: 604, iMin: 301, iMax: 500 }
        ],
        o3: [ // 8-hour average
            { min: 0, max: 0.054, iMin: 0, iMax: 50 },
            { min: 0.055, max: 0.070, iMin: 51, iMax: 100 },
            { min: 0.071, max: 0.085, iMin: 101, iMax: 150 },
            { min: 0.086, max: 0.105, iMin: 151, iMax: 200 },
            { min: 0.106, max: 0.200, iMin: 201, iMax: 300 }
        ],
        no2: [ // 1-hour average
            { min: 0, max: 0.053, iMin: 0, iMax: 50 },
            { min: 0.054, max: 0.100, iMin: 51, iMax: 100 },
            { min: 0.101, max: 0.360, iMin: 101, iMax: 150 },
            { min: 0.361, max: 0.649, iMin: 151, iMax: 200 },
            { min: 0.650, max: 1.249, iMin: 201, iMax: 300 },
            { min: 1.250, max: 2.049, iMin: 301, iMax: 500 }
        ],
        so2: [ // 1-hour average
            { min: 0, max: 0.035, iMin: 0, iMax: 50 },
            { min: 0.036, max: 0.075, iMin: 51, iMax: 100 },
            { min: 0.076, max: 0.185, iMin: 101, iMax: 150 },
            { min: 0.186, max: 0.304, iMin: 151, iMax: 200 },
            { min: 0.305, max: 0.604, iMin: 201, iMax: 300 },
            { min: 0.605, max: 1.004, iMin: 301, iMax: 500 }
        ],
        co: [ // 8-hour average
            { min: 0, max: 4.4, iMin: 0, iMax: 50 },
            { min: 4.5, max: 9.4, iMin: 51, iMax: 100 },
            { min: 9.5, max: 12.4, iMin: 101, iMax: 150 },
            { min: 12.5, max: 15.4, iMin: 151, iMax: 200 },
            { min: 15.5, max: 30.4, iMin: 201, iMax: 300 },
            { min: 30.5, max: 50.4, iMin: 301, iMax: 500 }
        ]
    };

    let maxAQI = 0;
    let dominantPollutant = '';
    
    // Her kirletici için AQI hesapla
    Object.keys(pollutants).forEach(pollutant => {
        if (AQI_BREAKPOINTS[pollutant] && pollutants[pollutant].value !== undefined) {
            const value = parseFloat(pollutants[pollutant].value);
            const breakpoints = AQI_BREAKPOINTS[pollutant];
            
            // Uygun aralığı bul
            const range = breakpoints.find(bp => value >= bp.min && value <= bp.max);
            
            if (range) {
                // AQI formülü: I = [(I_high - I_low) / (C_high - C_low)] * (C - C_low) + I_low
                const aqi = Math.round(
                    ((range.iMax - range.iMin) / (range.max - range.min)) * 
                    (value - range.min) + range.iMin
                );
                
                if (aqi > maxAQI) {
                    maxAQI = aqi;
                    dominantPollutant = pollutant;
                }
            }
        }
    });
    
    return {
        aqi: maxAQI,
        dominant_pollutant: dominantPollutant,
        pollutants: pollutants
    };
}    