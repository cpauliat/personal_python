#!/usr/bin/env python3

# ---------------------------------------------------------------------------------------
# This script get the lowest prices for an AirFrance-KLM flight from an origin 
# to a destination in a given range in dates for outbound flight and return flight
#
# Author: Christophe Pauliat
# Last update: January 2, 2021
#
# Prereq: register as a developer at https://docs.airfranceklm.com and get your api key
#
# API docs:
# - https://docs.airfranceklm.com/docs/read/opendata/offers/POST_lowestfareoffers_v1
# - https://docs.airfranceklm.com/docs/read/opendata/offers/Errors_Code
# ---------------------------------------------------------------------------------------

# ---------- imports
import requests
import json
import sys
import argparse
from datetime import datetime
from datetime import timedelta

# ---------- Variables
my_api_key          = "xxxxxxxxxxxx"     # register for free at https://docs.airfranceklm.com/docs/read/opendata/offers to get your API key
default_cabin       = "ECONOMY"          # Can contain ECONOMY or PREMIUM or BUSINESS or FIRST or ALL
default_airline     = "AF"               # AF or KL
prices              = {}
lowest_price        = 9999
lowest_dates        = []
highest_price       = 0
highest_dates       = []

# ---------- Colors for output
# see https://misc.flogisoft.com/bash/tip_colors_and_formatting to customize
COLOR_YELLOW = "\033[93m"
COLOR_RED    = "\033[91m"
COLOR_GREEN  = "\033[32m"
COLOR_NORMAL = "\033[39m"
COLOR_CYAN   = "\033[96m"
COLOR_BLUE   = "\033[94m"
COLOR_GREY   = "\033[90m"

COLOR_TITLE     = COLOR_CYAN
COLOR_DATA      = COLOR_NORMAL
COLOR_PRICE1    = COLOR_GREEN
COLOR_PRICE2    = COLOR_RED
COLOR_NO_FLIGHT = COLOR_YELLOW

# ---------- Functions

# ---- Disable colored output
def disable_colored_output():
  global COLOR_NORMAL
  global COLOR_TITLE
  global COLOR_DATA
  global COLOR_PRICE1
  global COLOR_PRICE2
  global COLOR_NO_FLIGHT

  COLOR_NORMAL    = ""
  COLOR_TITLE     = ""
  COLOR_DATA      = ""
  COLOR_PRICE1    = ""
  COLOR_PRICE2    = ""
  COLOR_NO_FLIGHT = ""

# ---------- Functions

# ---- return a list of string dates between 2 dates
def range_date(strdate1, strdate2):
  list = []
  d   = datetime.strptime(strdate1, "%Y-%m-%d") 
  end = datetime.strptime(strdate2, "%Y-%m-%d") 
  while d <= end:
    list.append(d.strftime("%Y-%m-%d"))
    d = d + timedelta(days=1)  
  return list


# ---- Get data using REST APIs
def post_request(origin, destination, date_voyage_aller, date_voyage_retour, airline, cabin):
  url = "https://api.airfranceklm.com/opendata/offers/v1/lowest-fare-offers"

  payload = json.dumps({
    "type": "DAY",
    "commercialCabins": [
      cabin
    ],
    "passengerCount": {
      "ADT": 1,
      "C14": 0,
      "CHD": 0,
      "INF": 0,
      "YTH": 0,
      "YCD": 0
    },
    "requestedConnections": [
      {
        "departureDate": date_voyage_aller,
        "dateInterval": f"{date_voyage_aller}/{date_voyage_aller}",
        "origin": {
          "airport": {
            "code": origin
          }
        },
        "destination": {
          "airport": {
            "code": destination
          }
        }
      },
      {
        "dateInterval": f"{date_voyage_retour}/{date_voyage_retour}",
        "origin": {
          "airport": {
            "code": destination
          }
        },
        "destination": {
          "airport": {
            "code": origin
          }
        }
      }
    ],
    "displayPriceContent": "ALL_PAX_ROUNDED",
    "bookingFlow": "LEISURE",
    "customer": {}
  })

  headers = {
    'Content-Type': 'application/json',
    'Accept-Language': 'en-US',
    'AFKL-TRAVEL-Host': airline,
    'AFKL-TRAVEL-Country': 'FR',
    'api-key': my_api_key,
  }
#    'Cookie': 'TS018c59be=0191981a55f1065e2b40d522060a260683f26004493efd7420e7badf5a2baa04f1def875fe8b579486a1db90414bcada4b5697c68e'

  response = requests.request("POST", url, headers=headers, data=payload)
  mydict   = json.loads(response.text)

  # save JSON files if requested
  if args.save_to:
    filename = f"{args.save_to}_{date_voyage_aller}_{date_voyage_retour}.json"
    with open(filename, 'w') as file:  
      file.write(json.dumps(mydict, indent=4, sort_keys=False))

  return mydict

# ---- Display all data in JSON format
def display_raw_data(mydict):
  print (json.dumps(mydict, indent=4, sort_keys=False))

# ---- Display minimal data 
def display_1d_table ():
  global prices
  global lowest_price
  global lowest_dates
  global highest_price
  global highest_dates

  if args.airline:
    airline = args.airline.upper()
  else:
    airline = default_airline

  if args.cabin:
    cabin = args.cabin.upper()
  else:
    cabin = default_cabin

  titre1 = "date_aller"
  titre2 = "date_retour"
  titre3 = "total_price"
  titre4 = "fare"
  titre5 = "taxes"
  titre6 = "surcharges"

  if args.verbose:
    print (f"{titre1:12s} {titre2:12s} {titre3:12s} {titre4:12s} {titre5:12s} {titre6:12s}")

  prices = {}
  for odate in range_date(args.odate1, args.odate2):
    for rdate in range_date(args.rdate1, args.rdate2):
      mydict = post_request(origin=args.orig.upper(), destination=args.dest.upper(), date_voyage_aller=odate, date_voyage_retour=rdate, airline=airline, cabin=cabin)
      key = f"{odate}_{rdate}"
      try:
        total_price = mydict["itineraries"][0]["flightProducts"][0]["price"]["totalPrice"]
        currency    = mydict["itineraries"][0]["flightProducts"][0]["price"]["currency"]
        fare        = mydict["itineraries"][0]["flightProducts"][0]["price"]["pricePerPassengerTypes"][0]["fare"]
        taxes       = mydict["itineraries"][0]["flightProducts"][0]["price"]["pricePerPassengerTypes"][0]["taxes"]
        surcharges  = mydict["itineraries"][0]["flightProducts"][0]["price"]["pricePerPassengerTypes"][0]["surcharges"][0]["amount"]
        if args.verbose:
          print (f"{odate:12s} {rdate:12s} {total_price:9.2f}    {fare:7.2f}      {taxes:7.2f}      {surcharges:7.2f}")

        # store prices in a dictionary for the 2d table later
        prices[key] = total_price

        # compute lowest price and save dates for this lowest price
        if total_price < lowest_price:
          lowest_price = total_price
          lowest_dates = []
        if total_price == lowest_price:
          lowest_dates.append(key)      

        # compute highest price and save dates for this highest price
        if total_price > highest_price:
          highest_price = total_price
          highest_dates = []
        if total_price == highest_price:
          highest_dates.append(key)      
      except:
        if args.verbose:
          print (f"{odate:12s} {rdate:12s} "+COLOR_NO_FLIGHT+"NO-FLIGHT"+COLOR_NORMAL)
        # store prices in a dictionary for the 2d table later
        prices[key] = "N/A"

  print("")

def display_2d_table():
  # table headers
  print (COLOR_TITLE+"            ",end="")
  for rdate in range_date(args.rdate1, args.rdate2):
    print (f"{rdate:10s}  ",end="")
  print ("")

  # table content
  for odate in range_date(args.odate1, args.odate2):
    print (COLOR_TITLE+f"{odate:10s}  ",end="")
    for rdate in range_date(args.rdate1, args.rdate2):
      key = f"{odate}_{rdate}"
      if prices[key] == lowest_price:
        COLOR = COLOR_PRICE1
      elif prices[key] == highest_price:
        COLOR = COLOR_PRICE2
      else:
        COLOR = COLOR_DATA
      try:
        print (COLOR+f"  {prices[key]:7.2f}   ",end="")
      except:
        # no flight for those dates
        print (COLOR_NO_FLIGHT+f"  {prices[key]:7s}   ",end="")
    print ("")

  print (COLOR_NORMAL)

def display_lowest_price_dates():
  print (COLOR_TITLE+"Lowest price  : "+COLOR_PRICE1+f"{lowest_price:7.2f}")
  print (COLOR_TITLE+"Dates for lowest price: ")
  for date in lowest_dates:
    print (COLOR_DATA+f"- {date}")
  print (COLOR_NORMAL)

def display_highest_price_dates():
  print (COLOR_TITLE+"Highest price : "+COLOR_PRICE2+f"{highest_price:7.2f}")
  print (COLOR_TITLE+"Dates for highest price: ")
  for date in highest_dates:
    print (COLOR_DATA+f"- {date}")
  print (COLOR_NORMAL)

# ========== Main

# ---- parse arguments
parser = argparse.ArgumentParser(description = "Get Flights offers (lowest fares) from Air-France-KLM using REST APIs")
parser.add_argument("-o", "--orig", help="origin airport (3 letters code).", required=True)
parser.add_argument("-d", "--dest", help="destination airport (3 letters code).", required=True)
parser.add_argument("-od1", "--odate1", help="minimum date for outward flight (YYYY-MM-DD)", required=True)
parser.add_argument("-od2", "--odate2", help="maximum date for outward flight (YYYY-MM-DD)", required=True)
parser.add_argument("-rd1", "--rdate1", help="minimun date for return flight (YYYY-MM-DD)", required=True)
parser.add_argument("-rd2", "--rdate2", help="maximum date for return flight (YYYY-MM-DD)", required=True)
parser.add_argument("-al", "--airline", help=f"airline code (AF or KL). Default is {default_airline}.", choices=["AF","KL"])
parser.add_argument("-nc", "--no_color", help="Disable colored output", action="store_true")
parser.add_argument("-v", "--verbose", help="Displays prices details", action="store_true")
parser.add_argument("-cb", "--cabin", help=f"cabin (ECONOMY or PREMIUM or BUSINESS or FIRST). Default is {default_cabin}.", choices=["ECONOMY","PREMIUM","BUSINESS","FIRST"])
parser.add_argument("-sf", "--save_to", help="write raw data to file")
args = parser.parse_args()

# ---- look for lowest fare for each combination of dates for outward and return flights
if args.no_color:
  disable_colored_output()

display_1d_table()
display_2d_table()
display_lowest_price_dates()
display_highest_price_dates()

# ---- happy end
exit(0)