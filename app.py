from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import time

import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)


@app.route("/")
def index():
    
    mars_data = mongo.db.mars_coll.find_one()
    
    return render_template("index.html", mars_data = mars_data)

@app.route("/scrape")
def scrape():

    mars_dict = scrape_mars.scrape()

    mongo.db.mars_coll.update({}, mars_dict, upsert=True)
    
    #return redirect("http://localhost:5000/", code=302)
    return redirect("/", code=302)
    
    #return "Scraping was successful."

if __name__ == "__main__":
    #print (scrape_mars.scrape())
    #time.sleep(4)
    app.run(debug=True)    