#!/usr/bin/env python3

# ---------------------------------------------------------------------------------------
# This script lists AirFrance-KLM flights (including price) from an origin
# to a destination using provided date for outbound flight and return flight
#
# Author: Christophe Pauliat
# Last update: January 4, 2021
#
# Prereq: register as a developer at https://docs.airfranceklm.com and get your api key
#
# API docs:
# - https://docs.airfranceklm.com/docs/read/opendata/flight_status_api/method_reference/GET_flightstatus_id
# - https://docs.airfranceklm.com/docs/read/opendata/offers/Errors_Code
# ---------------------------------------------------------------------------------------

# -------- imports
import requests
import json
import argparse

# ---------- Variables
my_api_key          = "xxxxxxxxxxxx"     # register for free at https://docs.airfranceklm.com/docs/read/opendata/offers to get your API key

# -------- functions
def get_flight_status_id(date, airline, flight_number):
  url = f"https://api.airfranceklm.com/opendata/flightstatus/{date}+{airline}+{flight_number}"

  payload={}
  headers = {
    'Content-Type': 'application/json',
    'Accept-Language': 'en-US',
    'AFKL-TRAVEL-Host': 'AF',
    'AFKL-TRAVEL-Country': 'FR',
    'api-key': my_api_key,
  }

  response = requests.request("GET", url, headers=headers, data=payload)
  mydict   = json.loads(response.text)

  # print (json.dumps(mydict, indent=4, sort_keys=False))
  # exit(1)

  # show flight status (ON_TIME, ARRIVED, IN_FLIGHT...)
  try:
    status = mydict["flightStatusPublic"]
    print (f"{'Flight status':24s} : {status}")
  except:
    pass

  try:
    terminal = mydict["flightLegs"][0]["departureInformation"]["airport"]["places"]["boardingTerminal"]
    print (f"{'Terminal':24s} : {terminal}")
  except:
    pass

  # for past or imminent flights, show boarding gate at departure airport
  try:
    boarding_gate = mydict["flightLegs"][0]["departureInformation"]["airport"]["places"]["gateNumber"][0]
    print (f"{'Gate':24s} : {boarding_gate}")
  except:
    pass

  try:
    aircraft_type = mydict["flightLegs"][0]["aircraft"]["typeName"]
    print (f"{'Aircraft type':24s} : {aircraft_type}")
  except:
    pass

  try:
    aircraft_registration = mydict["flightLegs"][0]["aircraft"]["registration"]
    print (f"{'Aircraft registration':24s} : {aircraft_registration}")
  except:
    pass

  try:
    departure_time_scheduled = mydict["flightLegs"][0]["departureInformation"]["times"]["scheduled"]
    print (f"{'Departure time scheduled':24s} : {departure_time_scheduled}")
  except:
    pass

  # for past flights, show real departure time
  try:
    departure_time_actual = mydict["flightLegs"][0]["departureInformation"]["times"]["actual"]
    print (f"{'Departure time actual':24s} : {departure_time_actual}")
  except:
    pass
# -------- Main

# ---- parse arguments
parser = argparse.ArgumentParser(description = "Get flight status")
parser.add_argument("-al", "--airline", help=f"airline code (AF or KL)", choices=["AF","KL"], required=True)
parser.add_argument("-fn", "--flight_number", help="Flight number (ex: 0084)")
parser.add_argument("-d", "--date", help="Date with format YYYYMMDD")
args = parser.parse_args()

get_flight_status_id(args.date, args.airline, args.flight_number)