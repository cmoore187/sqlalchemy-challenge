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
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/start<br>"
        f"/api/v1.0/start_end"

    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Design a query to retrieve the last 12 months of precipitation data and plot the results

    # Calculate the date one year from the last date in data set.
    previous = dt.date(2017, 8 , 23) - dt.timedelta(days=365)
    # Perform a query to retrieve the date and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= previous).all()

    # dictionary with the date as the key and the precipitation as the value
    precip = {date: prcp for date, prcp in results}

    session.close()
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
     results = session.query(Station.station).all()

     #unravel the results into a list
     stations = list(np.ravel(results))

     session.close()
     return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
        previous = dt.date(2017,8,23) - dt.timedelta(days=365)
        tobs_data = session.query(Measurement.tobs).filter(Measurement.date >= previous).order_by(Measurement.date).all()
        tobs_data_list = list(np.ravel(tobs_data))
        return jsonify(tobs_data_list=tobs_data_list)

@app.route("/api/v1.0/start")
def start():
    previous = dt.date(2017,8,23) - dt.timedelta(days=365)

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query TMIN, TAVG, and TMAX for all dates greater than and equal to the start date
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= previous).all()

    session.close()

    # Create a list of min, max, and avg
    agg_data = []
    for result in results:
        agg_dict = {}
        agg_dict["TMIN"] = result[0]
        agg_dict["TMAX"] = result[1]
        agg_dict["TAVG"] = result[2]
        agg_data.append(agg_dict)
        
        return jsonify(agg_data)


@app.route("/api/v1.0/start_end")
def start_end():

    previous = dt.date(2017,8,23) - dt.timedelta(days=365)

    # Create our session (link) from Python to the DB
    session = Session(engine)
    today = dt.datetime(2016, 8, 23)
    # Query TMIN, TAVG, and TMAX for all dates between dates
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= previous).filter(Measurement.date <= today).all()

    session.close()

    # Create a list of min, max, and avg
    agg_data = []
    for result in results:
        agg_dict = {}
        agg_dict["TMIN"] = result[0]
        agg_dict["TMAX"] = result[1]
        agg_dict["TAVG"] = result[2]
        agg_data.append(agg_dict)
        
        return jsonify(agg_data)


if __name__ == '__main__':
    app.run(debug=True)
