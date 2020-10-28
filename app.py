# import necessary libraries
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import pandas as pd
from sqlalchemy import create_engine
from flask import Flask, render_template, jsonify
from config import pg_user, pg_password, db_name
# create instance of Flask app

app = Flask(__name__)

connection_string = f"{pg_user}:{pg_password}@localhost:5432/{db_name}"
engine = create_engine(f'postgresql://{connection_string}')

Base = automap_base()
Base.prepare(engine, reflect=True)
print(Base.classes.keys())
shelter_data = Base.classes.shelterdata

# create route that renders index.html template
@app.route("/")
def index():
    session = Session(engine)
    results = session.query(shelter_data).all()

    # close the session to end the communication with the database
    session.close()

    # Convert list of tuples into normal list
    shelter_list = []
    for obj in results:
        animal = obj.__dict__
        animal.pop("_sa_instance_state")
        shelter_list.append(animal)
    print(shelter_list)
    return jsonify(shelter_list)

if __name__ == "__main__":
    app.run(debug=True)