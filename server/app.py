from crawl import process_data, country_data
from flask import Flask, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

app = Flask(__name__)
scheduler = BackgroundScheduler()
intervalTrigger = IntervalTrigger(minutes=1)
scheduler.add_job(process_data, intervalTrigger, id='crawl')
scheduler.start()


@app.get('/')
def post():
    country = request.values.get('country')
    r = country_data.get(country, None)
    if r is None:
        status = 404
    else:
        status = 200
    return jsonify(r), status


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
