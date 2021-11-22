# Surfs up Flask APP

# Having issues with jinja2 modulenotfounderror 
# App architecture seems good
#

from os import stat
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt
import numpy as np
import pandas as pd
from datetime import timedelta

engine  = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect = True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)
@app.route("/")
def Home():
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation")
def percipitation():
    session = Session(engine)

    recentDate = session.query(Measurement.date).order_by(Measurement.date.desc()).first
    recentDate = dt.datetime.strptime(recentDate[0],'%Y-%m-%d')
    firstDate = recentDate - timedelta(days = 365)
    r = (session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= firstDate).order_by(Measurement.date).all())
    return jsonify(r)

# -----

@app.route("/api/v1.0/stations")
def stations():
  session  = Session(engine)

  stationsList = session.query(Station.station, Station.name).all()
  return jsonify (stationsList)

# -----

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    recentDate = session.query(Measurement.date).order_by(Measurement.date.desc()).first
    recentDate = dt.datetime.strptime(recentDate[0],'%Y-%m-%d')
    firstDate = recentDate - timedelta(days = 365)

    stationCount = (session.query(Measurement.station, func.count).filter(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    top = (stationCount[0])
    topStation = (top[0])
    (session.query(func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs),).filter(Measurement.station == topStation).all())
    topStationYear = session.query(Measurement.tobs).filter(Measurement.station == topStation).filter(Measurement.date >= firstDate).all()
    return jsonify (topStationYear)

# -----

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def start(start = none, end = none):
    session = Session(engine)

    s = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        r = session.query(*s).filter(Measurement.date >= start).all()
        temp = list(np.ravel(r))
        return jsonify (temp)

    r = session.query(*s).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return (r)

if __name__ == '__main__':
    app.run()