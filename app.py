# app.py - Programs to scrape data from multiple Mars-related sites, store a in Mongo database, and 
# produce a webpage to display the data and images, with a button able to re-scrape and refresh the information.

# Import tools.
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import time

# Import code that scrapes several websites for information
import scrape_mars

# Instantiate flask, connect to mongo database mars_db
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

# Base browser route to query database for Mars data stored in mars_coll collection, and display on webpage
@app.route("/")
def index():
    
    mars_data = mongo.db.mars_coll.find_one()
    return render_template("index.html", mars_data = mars_data)

# Route to scrape fresh Mars data from web and store in database
@app.route("/scrape")
def scrape():

    mars_dict = scrape_mars.scrape()
    mongo.db.mars_coll.update({}, mars_dict, upsert=True)
    return redirect("/", code=302)
    
if __name__ == "__main__":
    app.run(debug=True)    