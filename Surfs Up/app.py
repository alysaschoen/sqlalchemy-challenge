# Import the dependencies.
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model

Base = automap_base()

# reflect the tables

Base.prepare(engine, reflect=True)

# Save references to each table

Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB

session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def homepage():
    """Available API Routes"""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def get_precipitation():
    annual = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= annual).all()

    prcp_data = []
    for date, prcp in results:
        prcp_dict = {
            "Date": date,
            "Precipitation": prcp
        }
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)


@app.route("/api/v1.0/stations")
def get_stations():
    station_data = session.query(Station.name, Station.station).all()
    stations_dict = dict(station_data)
    return jsonify(stations_dict)


def get_active_stations():
    active_station_data = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    active_stations_dict = dict(active_station_data)
    return jsonify(active_stations_dict)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def get_temperature_stats(start, end=None):
    if end:
        temperature_stats = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start, Measurement.date <= end).all()
    else:
        temperature_stats = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()

    return jsonify(temperature_stats)

if __name__ == "__main__":
    app.run(debug=True)








    


