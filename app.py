#import dependencies
from datetime import date
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask,jsonify


#create database
engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect = True)

measurement = Base.classes.measurement
station = Base.classes.station


#flask setup
app = Flask(__name__)


#flask routes
@app.route("/")
def home():
    return (
        f"Welcome to the Hawaii API.<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"For the following 2 endpoints, use the date format yyyy-mm-dd <br/>"
        f"/api/v1.0/startDate<br/>"
        f"/api/v1.0/startDate/endDate<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(measurement.date, measurement.prcp).all()
    session.close()

    precipitation = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["Date"] = date
        precip_dict["Precipitation"] = prcp
        precipitation.append(precip_dict)

    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(station.station).all()
    session.close()

    stations = []
    for station in results:
        station_dict = {}
        station_dict["Station"] = station
        stations.append(station_dict)

    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(measurement.date, measurement.tobs).\
        filter(measurement.date >= "2016-08-23").\
            filter(measurement.station == "USC00519281").all()
    session.close()

    tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["TOBS"] = tobs
        tobs.append(tobs_dict)

    return jsonify(tobs)


@app.route("/api/v1.0/<start>")
def startOnly(start):
    session = Session(engine)
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).all()
    session.close()

    tobs = []
    for min, avg, max in results:
        tobs_dict = {}
        tobs_dict["TMIN"] = min
        tobs_dict["TAVG"] = avg
        tobs_dict["TMAX"] = max
        tobs.append(tobs_dict)

    return jsonify(tobs)



@app.route("/api/v1.0/<start>/<end>")
def startEnd(start, end):
    session = Session(engine)
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()
    session.close()
    tobs = []
    for min, avg, max in results:
        tobs_dict = {}
        tobs_dict["TMIN"] = min
        tobs_dict["TAVG"] = avg
        tobs_dict["TMAX"] = max
        tobs.append(tobs_dict)

    return jsonify(tobs)


if __name__ == '__main__':
    app.run(debug=True)
