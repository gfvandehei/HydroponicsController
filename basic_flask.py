import flask
import RPi.GPIO as GPIO
import json
from threading import Timer, Thread
import datetime
from typing import List
import time
import logging
from hydroserver.pump_manager import PumpManager

from flask.helpers import send_file

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

app = flask.Flask(__name__)
fill_pin = None
drain_pin = None
pump_time = 100

state = "WAITING"

active_timer = None

GPIO.setmode(GPIO.BCM)



# load the schedule file
with open("conf.json", "r") as fp:
    conf_json = json.load(fp)
    fill_pin = conf_json['pins']['fill']
    drain_pin = conf_json['pins']['drain']
    fill_times: List[str] = conf_json['schedule']['fill']
    pump_time = conf_json['pump_drain_time']
    GPIO.setup(fill_pin, GPIO.OUT) 
    GPIO.setup(drain_pin, GPIO.OUT)
    GPIO.output(drain_pin, 0)
    GPIO.output(fill_pin, 0)

    log.info(f"Initialized config with\n FILL: {fill_pin} \n DRAIN: {drain_pin} \n PUMP: {pump_time} \n SCHED: {fill_times}") 

pump_manager = PumpManager(fill_pin, 100)

@app.route("/fill")
def _fill():
    try:
        pump_manager.fill()
    except Exception as err:
        return {
            "status": 200,
            "messages": [
                str(err)
            ]
        }
    log.info("fill request")
    return {
        "status": 200,
        "data": pump_manager.pump_state
    }

@app.route("/drain")
def _drain():
    pump_manager.drain()
    log.info("drain request")
    return {
        "status": 200,
        "data": state
    }

@app.route("/schedule", methods=["GET"])
def get_schedule():
    global fill_times
    return {
        "status": 200,
        "data": fill_times
    }

@app.route("/schedule", methods=["POST"])
def set_schedule():
    global fill_times
    body = flask.request.json
    schedule = body['schedule']
    fill_times = schedule

    return {
        "status": 200,
        "data": fill_times
    }

@app.route("/state")
def get_state():
    state = pump_manager.pump_state
    return {
        "status": 200,
        "data": state
    }

@app.route("/")
def serve_index():
    return send_file("index.html")

def threaded_follow_schedule():
    while True:
        #isoformat = time.localtime()
        isoformat = time.strftime("%H:%M", time.localtime())
        #isoformat = datetime.datetime.now().strftime("%H:%M")
        log.debug(f"Checking at time {isoformat}")
        if active_timer == None:
            try:
                index = fill_times.index(isoformat)
                if index >= 0:
                    # it is currently a time in the schedule, start fill
                    log.info("fill request from schedule")
                    pump_manager.fill()
            except ValueError:
                pass
        
        time.sleep(30)

Thread(target=threaded_follow_schedule).start()

app.run(host="0.0.0.0", port=5000)