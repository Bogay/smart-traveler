from crawl import process_data, country_data
from flask import Flask, jsonify, request
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

# Setup scheduler to crawl country data every 1 min.
scheduler = BackgroundScheduler()
intervalTrigger = IntervalTrigger(minutes=1)
scheduler.add_job(process_data, intervalTrigger, id='crawl')
scheduler.start()

app = Flask(__name__)
CORS(app)


# Register `GET /`
@app.get('/')
def post():
    country = request.values.get('country')
    # Query country data by given country name
    r = country_data.get(country, None)
    # Return 404 if the name not in dictionary
    if r is None:
        status = 404
    else:
        status = 200
    return jsonify(r), status


if __name__ == '__main__':
    # Start servere and listen 5000 port on any address
    app.run(host='0.0.0.0', port='5000')
