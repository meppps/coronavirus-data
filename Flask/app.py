from flask import Flask, render_template, jsonify
import json
from bson.json_util import dumps
from flask_json import FlaskJSON, JsonError, json_response, as_json





# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

db = client.corona_db


# Set route
@app.route('/')
def index():
    # Store the entire team collection in a list

    corona = list(db.corona_data.find())
    # json = jsonify(corona)
    # print(json)

    print(corona)
    dumps(corona)

    # Return the template with the teams list passed in
    return render_template('index.html', corona=corona)


if __name__ == "__main__":
    app.run(debug=True)

