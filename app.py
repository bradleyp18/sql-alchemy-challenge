# Surfs up Flask APP

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
    return jasonify(r)

# -----

@app.route("/api/v1.0/stations")
def stations():
  session  = Session(engine)

  stationsList = session.query(Station.station, Station.name).all()
  return jasonify (stationsList)

# -----

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)








@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def start(start = none, end = none):
    session = Session(engine)
