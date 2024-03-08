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
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

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
def welcome():
    """List all available api routes."""
    return(
        f"Available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # create session link from python to db
    session = Session(engine)
    """Return last 12 months of precipitation data"""
    #query the last 12 months
    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= previous_year).\
    order_by(Measurement.date).all()
    session.close()

    #create a dictionary using date as the key and prcp as the value
    precipitation_info = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict[date] = prcp
        precipitation_info.append(precipitation_dict)
    return jsonify(precipitation_info)

@app.route("/api/v1.0/stations")
def station():
    #create session link from python to db
    session = Session(engine)
    """Return station data"""
    #query station data
    station_results = session.query(Station.station, Station.name, Station.latitude, 
                                    Station.longitude, Station.elevation).all()
    session.close()

    #create a station dictionary
    station_info = []
    for station, name, latitude, longitude, elevation in station_results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        station_info.append(station_dict)
    return jsonify(station_info)

@app.route("/api/v1.0/tobs")
def tobs():
    #create session link from python to db
    session = Session(engine)
    """Return last 12 months of tobs data"""
    #query tobs data
    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= previous_year).\
    filter(Measurement.station=="USC00519281").order_by(Measurement.tobs).all()
    session.close()

    #create tobs dictionary
    tobs_info = []
    for date, tobs in tobs_results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_info.append(tobs_dict)
    return jsonify(tobs_info)

@app.route("/api/v1.0/<start>")
def start_date(start):
    #create session link from python to db
    session = Session(engine)
    """Return min temp, avg temp, max temp for specified start date"""
    #query start min temp, avg temp, max temp data
    sel = [func.min(Measurement.tobs),
       func.max(Measurement.tobs),
       func.avg(Measurement.tobs)]
    start_results = session.query(*sel).filter(Measurement.date >= start).all()
    session.close()

    #create start date dictionary
    start_date_info = []
    for min_temp, avg_temp, max_temp in start_results:
        start_date_dict={}
        start_date_dict["min_temp"] = min_temp
        start_date_dict["avg_temp"] = avg_temp
        start_date_dict["max_temp"] = max_temp
        start_date_info.append(start_date_dict)
    return jsonify(start_date_info)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    #create session link from python to db
    session = Session(engine)
    """Return min temp, avg temp, max temp for start-end range"""
    #query start-end min temp, avg temp, max temp data
    sel = [func.min(Measurement.tobs),
       func.max(Measurement.tobs),
       func.avg(Measurement.tobs)]
    start_end_results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    #create start-end range dictionary
    start_end_info = []
    for min_temp, avg_temp, max_temp in start_end_results:
        start_end_dict={}
        start_end_dict["min_temp"] = min_temp
        start_end_dict["avg_temp"] = avg_temp
        start_end_dict["max_temp"] = max_temp
        start_end_info.append(start_end_dict)
    return jsonify(start_end_info)

if __name__ == '__main__':
    app.run(debug=True)
