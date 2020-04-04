
# Dependencies
from flask import Flask, render_template, jsonify
import json
from bson import ObjectId
import pymongo

# Init
app = Flask(__name__)
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.corona_db


# Set route
@app.route('/')
def index():

    # Query from db
    corona = list(db.corona_data.find())

    # Thanks stackoverflow
    class JSONEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, ObjectId):
                return str(o)
            return json.JSONEncoder.default(self, o)
    
    corona = JSONEncoder().encode(corona)

    print(corona)


    # Return the template with the teams list passed in
    return render_template('index.html', corona=corona)

if __name__ == "__main__":
    app.run(debug=True)

