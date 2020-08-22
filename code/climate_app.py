# Aaron Wollman

from flask import Flask, jsonify
from climate_lib import Climate_Database, year_ago

app = Flask(__name__)

@app.route("/")
def index():
    """
    The home page provides a list of all routes available.
    """
    return (
        f"<h1>Index</h1>"
        f"/api/v1.0/precipitation"
        f"<br>"
        f"/api/v1.0/stations"
        f"<br>"
        f"/api/v1.0/tobs"
        f"<br>"
        f"/api/v1.0/(start)"
        f"<br>"
        f"/api/v1.0/(start)/(end)"
        f"<br>"
        f"Where (start) and (end) are dates in the format 'YYYY-MM-DD'"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """
    Returns a list of precipitations and their dates.
    """
    database = Climate_Database()
    precip_data = database.get_all_precip_data()
    precip_dict = {}
    for date, prcp in precip_data:
        precip_dict[date] = prcp
    
    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations():
    """
    Return a list of stations.
    """
    database = Climate_Database()
    station_data = database.get_all_stations()
    print(station_data)
    station_dicts = []
    for station in station_data:
        station_dict = {
            "id" : station.id,
            "name" : station.name,
            "station" : station.station,
            "latitude" : station.latitude,
            "longitude" : station.longitude,
            "elevation" : station.elevation
        }
        station_dicts.append(station_dict)
    return jsonify(station_dicts)

@app.route("/api/v1.0/tobs")
def tobs():
    """
    Returns the temperatures of the most active station 
    for the last year of data.
    """
    database = Climate_Database()
    most_active_station = database.get_most_active_station().station

    latest_date = database.get_latest_date()
    one_year_ago = year_ago(latest_date)

    temps = database.get_temps(most_active_station, one_year_ago, latest_date)
    temp_dicts = []
    for date, temp in temps:
        temp_dict = {
            date : temp
        }
        temp_dicts.append(temp_dict)
    return jsonify(temp_dicts)

@app.route("/api/v1.0/<start>")
def stats_start_only(start):
    database = Climate_Database()
    end = database.get_latest_date()
    return get_stats_json(database, start, end)

@app.route("/api/v1.0/<start>/<end>")
def stats(start, end):
    database = Climate_Database()
    return get_stats_json(database, start, end)

def get_stats_json(database, start, end):
    stats = database.get_temp_stats_by_date(start, end)
    min_temp = stats["min"]
    max_temp = stats["max"]
    avg_temp = stats["avg"]
    stats = {
        "TMIN" : min_temp,
        "TMAX" : max_temp,
        "TAVG" : avg_temp
    }
    return jsonify(stats)

if __name__ == "__main__":
    app.run(debug=True)