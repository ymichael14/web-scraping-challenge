from ast import Import
from flask import Flask, render_template, redirect
import scrape_all 


import pymongo

app = Flask(__name__)

# connect to database
conn='mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db=client.mars_facts_db
db.planet_facts.drop()

@app.route('/')
def home():
    data=db.planet_facts.find_one()
    return render_template('index.html', data=data)

@app.route('/scrape')
def get_data():
    data=scrape_all.scrape()
    db.planet_facts.insert_one(data)
    return redirect('/', code=302)


if __name__ == "__main__":
    app.run(debug=True)
