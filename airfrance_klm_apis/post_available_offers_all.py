#!/usr/bin/env python3

# ---------------------------------------------------------------------------------------
# This script lists AirFrance-KLM flights (including price) from an origin
# to a destination using provided date for outbound flight and return flight
#
# Author: Christophe Pauliat
#
# Prereq: register as a developer at https://docs.airfranceklm.com and get your api key
#
# API docs: 
# - https://docs.airfranceklm.com/docs/read/opendata/offers/POST_availableoffers_v1
# - https://docs.airfranceklm.com/docs/read/opendata/offers/Errors_Code
#
# Versions:
#     2022-01-04: initial version
#     2022-01-11: Add option --csv
# ---------------------------------------------------------------------------------------

# ---------- imports
import requests
import json
import sys
import argparse
from datetime import datetime

# ---------- Variables
my_api_key          = "xxxxxxxxxxxx"     # register for free at https://docs.airfranceklm.com/docs/read/opendata/offers to get your API key
default_cabin       = "ECONOMY"          # Can contain ECONOMY or PREMIUM or BUSINESS or FIRST or ALL
default_airline     = "AF"               # AF or KL
lowest_price        = 9999
highest_price       = 0
decile1_max_price   = 0

# ---------- Colors for output
# see https://misc.flogisoft.com/bash/tip_colors_and_formatting to customize
COLOR_YELLOW = "\033[93m"
COLOR_RED    = "\033[91m"
COLOR_GREEN  = "\033[32m"
COLOR_NORMAL = "\033[39m"
COLOR_CYAN   = "\033[96m"
COLOR_BLUE   = "\033[94m"
COLOR_GREY   = "\033[90m"

COLOR_TITLE         = COLOR_GREEN
COLOR_DATA          = COLOR_BLUE
COLOR_ITINERARY     = COLOR_YELLOW
COLOR_PRICE1        = COLOR_RED
COLOR_PRICE2        = COLOR_CYAN
COLOR_LINKS         = COLOR_GREY
COLOR_LOWEST_PRICE  = COLOR_GREEN  
COLOR_HIGHEST_PRICE = COLOR_RED
COLOR_DECILE1_PRICE = COLOR_YELLOW

# ---------- Functions

# ---- Disable colored output
def disable_colored_output():
  global COLOR_NORMAL
  global COLOR_TITLE
  global COLOR_DATA
  global COLOR_ITINERARY
  global COLOR_PRICE1
  global COLOR_PRICE2
  global COLOR_LINKS
  global COLOR_LOWEST_PRICE   
  global COLOR_HIGHEST_PRICE
  global COLOR_DECILE1_PRICE

  COLOR_NORMAL        = ""
  COLOR_TITLE         = ""
  COLOR_DATA          = ""
  COLOR_ITINERARY     = ""
  COLOR_PRICE1        = ""
  COLOR_PRICE2        = ""
  COLOR_LINKS         = ""
  COLOR_LOWEST_PRICE  = ""  
  COLOR_HIGHEST_PRICE = ""
  COLOR_DECILE1_PRICE = ""

# ---- Get data using REST APIs
def post_request(origin, destination, date_voyage_aller, date_voyage_retour, airline, cabin):
  url = "https://api.airfranceklm.com/opendata/offers/v1/available-offers/all"

  payload = json.dumps({
    "commercialCabins": [cabin],
    "passengerCount": {
      "ADT": 1,
      "CHD": 0,
      "INF": 0
    },
    "requestedConnections": [
      {
        "departureDate": date_voyage_aller,
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
        "departureDate": date_voyage_retour,
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
    ]
  })

  headers = {
    'Content-Type': 'application/json',
    'Accept-Language': 'en-US',
    'AFKL-TRAVEL-Host': airline,
    'AFKL-TRAVEL-Country': 'FR',
    'api-key': my_api_key,
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  mydict   = json.loads(response.text)
  return mydict

# ---- Save all data to file
def save_data_to_file(mydict, filename):
  with open(filename, 'w') as file:  
    file.write(json.dumps(mydict, indent=4, sort_keys=False))

# ---- Load all data from file
def load_data_from_file(filename):
  with open(filename, 'r') as file:  
    mydict = json.load(file)
  return mydict

# ---- Display taxes breakdown
def display_tax_breakdown(url):
  # print (url)
  # return

  payload = {}

  headers = {
    'Content-Type': 'application/json',
    'Accept-Language': 'en-US',
    'AFKL-TRAVEL-Host': 'AF',
    'AFKL-TRAVEL-Country': 'FR',
    'api-key': my_api_key,
  }

  response = requests.request("GET", url, headers=headers, data=payload)
  mydict   = json.loads(response.text)

  print (COLOR_NORMAL+f"---------- "+COLOR_ITINERARY+"taxes breakdown"+COLOR_NORMAL+" (total taxes = "+COLOR_PRICE2+f"{mydict['price']['totalTaxes']:7.2f}"+COLOR_NORMAL+")")
  taxes = mydict['price']['pricePerPassengerTypes'][0]['taxes']
  for tax in taxes:
    title = f"{tax['code']} ({tax['name']})"
    print (f"{title:54s} : {tax['amount']:7.2f}")
  try:
    yr_tax = mydict['price']['pricePerPassengerTypes'][0]['airTransportationSurcharges'][0]
    title = f"{yr_tax['code']} ({yr_tax['name']})"
    print (f"{title:54s} : {yr_tax['amount']:7.2f}")
  except:
    pass

# ---- Display all data in JSON format
def display_raw_data(mydict):
  print (json.dumps(mydict, indent=4, sort_keys=False))

# ---- Get lowest and highest prices
def get_lowest_and_highest_prices(mydict):
  global lowest_price
  global highest_price
  global decile1_max_price

  try:
    itineraries = mydict["itineraries"]
    for itinerary in itineraries:
      price       = itinerary["flightProducts"][0]["price"]["totalPrice"]
      if price < lowest_price: 
        lowest_price = price
      if price > highest_price: 
        highest_price = price
    decile1_max_price = lowest_price + (highest_price - lowest_price) / 10
  except:
    pass

# ---- Display only relevant data in formatted output
def display_formatted_data(mydict):
  num_iti = 0
  connection_max_segments = 0
  try:
    itineraries = mydict["itineraries"]

    # First, compute max number of segments for connection1 (outbound flights) and connection2 (return flights)
    for itinerary in itineraries:
      connections = itinerary["connections"]
      connection1 = connections[0]
      connection2 = connections[1]
      if len(connection1["segments"]) > connection_max_segments:
        connection_max_segments = len(connection1["segments"])
      if len(connection2["segments"]) > connection_max_segments:
        connection_max_segments = len(connection2["segments"])

    # Then display information
    for itinerary in itineraries:
      num_iti += 1
      price       = itinerary["flightProducts"][0]["price"]["totalPrice"]
      currency    = itinerary["flightProducts"][0]["price"]["currency"]
      connections = itinerary["connections"]

      print (COLOR_PRICE1+"======================================== "+COLOR_ITINERARY+f"Itinerary {num_iti}"+COLOR_NORMAL+" : Price = "+COLOR_PRICE1+f"{price:.2f} {currency}  ", end="")
      if price == lowest_price:
        print (COLOR_LOWEST_PRICE+" ======== LOWEST PRICE ========")
      elif price == highest_price:
        print (COLOR_HIGHEST_PRICE+" ======== HIGHEST PRICE ========")
      elif price <= decile1_max_price:
        print (COLOR_DECILE1_PRICE+" ======== 1st DECILE PRICE ========")
      else:
        print (COLOR_NORMAL)
      print (COLOR_NORMAL)

      num_con = 0
      for connection in connections:
        price_connection = itinerary["flightProducts"][0]["connections"][num_con]["price"]["totalPrice"]
        num_con += 1
        segments = connection["segments"]
        if num_con == 1 and len(segments) == 1:
          name_con = "Outbound flight : DIRECT"
        elif num_con == 1 and len(segments) > 1:
          name_con = "Outbound flights : WITH CONNECTION"
        elif num_con > 1 and len(segments) == 1:
          name_con = "Return flight : DIRECT"      
        elif num_con > 1 and len(segments) > 1:
          name_con = "Return flights : WITH CONNECTION"
  
        connection_title = COLOR_NORMAL+"---------- "+COLOR_ITINERARY+f"{name_con:34s}"+COLOR_NORMAL+" : price = "+COLOR_PRICE2+f"{price_connection:7.2f} {currency:3s}"+COLOR_NORMAL
        # connection_title uses 67 characters so add 17 spaces to reach 84 characters
        print (f"{connection_title}{' ':17s}",end="")
        if connection_max_segments == 3:
          print (f"{' ':42s}",end="")        
        print ("   ",end="")
      print ("")

      for connection in connections:
        segments = connection["segments"]
        for segment in segments:
          line1 = COLOR_TITLE+"Flight   : "+COLOR_DATA+f"{segment['marketingFlight']['carrier']['code']}{segment['marketingFlight']['number']}"
          # line1 uses 17 characters so add 25 spaces to reach 42 characters
          print (f"{line1}{' ':25s}",end="")
        # if less segments than connection_max_segments, add spaces for each missing segment
        for _ in range(connection_max_segments - len(segments)):
          print (f"{' ':42s}",end="")
        print (COLOR_LINKS+" | "+COLOR_NORMAL,end="")
      print ("")

      for connection in connections:
        segments = connection["segments"]
        for segment in segments:
          line2 = COLOR_TITLE+"Departure: "+COLOR_DATA+f"{segment['origin']['code']} at {segment['departureDateTime']}"
          # line2 uses 37 characters so add 5 spaces to reach 42 characters
          print (f"{line2}{' ':5s}",end="")
        # if less segments than connection_max_segments, add spaces for each missing segment
        for _ in range(connection_max_segments - len(segments)):
          print (f"{' ':42s}",end="")
        print (COLOR_LINKS+" | "+COLOR_NORMAL,end="")
      print ("")

      for connection in connections:
        segments = connection["segments"]
        for segment in segments:
          line3 = COLOR_TITLE+"Arrival  : "+COLOR_DATA+f"{segment['destination']['code']} at {segment['arrivalDateTime']}"
          # line3 uses 37 characters so add 5 spaces to reach 42 characters
          print (f"{line3}{' ':5s}",end="")
        # if less segments than connection_max_segments, add spaces for each missing segment
        for _ in range(connection_max_segments - len(segments)):
          print (f"{' ':42s}",end="")        
        print (COLOR_LINKS+" | "+COLOR_NORMAL,end="")
      print ("")

      for connection in connections:
        segments = connection["segments"]
        for segment in segments:
          line4 = COLOR_TITLE+"Aircraft : "+COLOR_DATA+f"{segment['marketingFlight']['operatingFlight']['equipmentType']['name']:26s}"
          # line3 uses 37 characters so add 5 spaces to reach 42 characters
          print (f"{line4}{' ':5s}",end="")
        # if less segments than connection_max_segments, add spaces for each missing segment
        for _ in range(connection_max_segments - len(segments)):
          print (f"{' ':42s}",end="")
        print (COLOR_LINKS+" | "+COLOR_NORMAL,end="")
      print ("")

      # If requested, display links for cabin plans
      if args.cabin_plan:
        print ("")
        for connection in connections:
          segments = connection["segments"]
          for segment in segments:
            try:
              flight_number = f"{segment['marketingFlight']['carrier']['code']}{segment['marketingFlight']['number']}"
              link          = f"{segment['marketingFlight']['operatingFlight']['equipmentType']['_links']['information']['href']}"
              print (COLOR_TITLE+f"Cabin plan {flight_number}: "+COLOR_LINKS+f"{link}")
            except:
              pass

      print (COLOR_NORMAL)

      # If requested, display tax breakdown for the itinerary
      if args.tax_breakdown:
        offer_link = itinerary["flightProducts"][0]["_links"]["taxBreakdown"]["href"]
        display_tax_breakdown(offer_link)
        print (COLOR_NORMAL)

  except:
    # No flight available
    print ("No outbound or return flight available !")

# ---- Display minimal data 
def display_minimal_data(mydict):
  num_iti = 0
  try:
    itineraries = mydict["itineraries"]
    for itinerary in itineraries:
      num_iti += 1
      price       = itinerary["flightProducts"][0]["price"]["totalPrice"]
      currency    = itinerary["flightProducts"][0]["price"]["currency"]
      connections = itinerary["connections"]
    
      if price == lowest_price:
        COLOR = COLOR_LOWEST_PRICE    
      elif price == highest_price:
        COLOR = COLOR_HIGHEST_PRICE
      elif price <= decile1_max_price:
        COLOR = COLOR_DECILE1_PRICE
      else:
        COLOR = COLOR_NORMAL

      print (COLOR+f"Itinerary {num_iti:3d} : Price = {price:7.2f} {currency}      ",end="")
      num_con = 0
      for connection in connections:
        price_connection = itinerary["flightProducts"][0]["connections"][num_con]["price"]["totalPrice"]
        segments         = connection["segments"]
        connection_name  = segments[0]['departureDateTime']
        num_con += 1

        for segment in segments:
          connection_name = connection_name + "-" + segment['marketingFlight']['carrier']['code'] + segment['marketingFlight']['number']

        print (f"{connection_name:41s}: {price_connection:7.2f} {currency}      ", end="")

      if price == lowest_price:
        print ("LOWEST PRICE")
      elif price == highest_price:
        print ("HIGHEST PRICE")
      elif price <= decile1_max_price:
        print ("1st DECILE PRICE")
      else:
        print (COLOR_NORMAL)

  except:
    # No flight available
    print ("No outbound or return flight available !")

# ---- Display CSV data 
def display_csv_data(mydict):
  current_date = datetime.today().strftime('%Y-%m-%d')
  try:
    itineraries = mydict["itineraries"]
    for itinerary in itineraries:
      itinerary_price = itinerary["flightProducts"][0]["price"]["totalPrice"]
      connections     = itinerary["connections"]
  
      itinerary_name = ""
      connection_name  = []
      connection_price = []
      num_con = 0
      for connection in connections:
        connection_price.append(itinerary["flightProducts"][0]["connections"][num_con]["price"]["totalPrice"])
        connection_array = []
        num_con += 1

        for segment in connection["segments"]:
          connection_array.append(segment['marketingFlight']['carrier']['code'] + segment['marketingFlight']['number'])

        connection_name.append("-".join(connection_array))
      
      itinerary_name = f"{connection_name[0]}___{connection_name[1]}"

      print (f"{current_date},{itinerary_name},{itinerary_price:.2f},{connection_name[0]},{connection_price[0]:.2f},{connection_name[1]},{connection_price[1]:.2f}")
  except:
    # No flight available
    print ("No outbound or return flight available !")

# ========== Main

# ---- parse arguments
parser = argparse.ArgumentParser(description = "Get Flights offers from Air-France-KLM using REST APIs")
group1  = parser.add_mutually_exclusive_group()
group1.add_argument("-r", "--raw", help="displays raw formatted data (JSON)", action="store_true")
group1.add_argument("-s", "--short", help="displays minimal data (short)", action="store_true")
group1.add_argument("-c", "--csv", help="displays minimal data in CSV format", action="store_true")
group2  = parser.add_mutually_exclusive_group()
group2.add_argument("-lf", "--load_from", help="read data from file instead of API request")
group2.add_argument("-sf", "--save_to", help="write raw data to file")
parser.add_argument("-o", "--orig", help="origin airport (3 letters code).")
parser.add_argument("-d", "--dest", help="destination airport (3 letters code).")
parser.add_argument("-od", "--odate", help="date for outward flight (YYYY-MM-DD)")
parser.add_argument("-rd", "--rdate", help="date for return flight (YYYY-MM-DD)")
parser.add_argument("-al", "--airline", help=f"airline code (AF or KL). Default is {default_airline}.", choices=["AF","KL"])
parser.add_argument("-nc", "--nocolor", help="Disable colored output", action="store_true")
parser.add_argument("-tx", "--tax_breakdown", help="Display taxes breakdown", action="store_true")
parser.add_argument("-cp", "--cabin_plan", help="Display cabin plans links", action="store_true")
parser.add_argument("-cb", "--cabin", help=f"cabin (ECONOMY or PREMIUM or BUSINESS or FIRST). Default is {default_cabin}.", choices=["ECONOMY","PREMIUM","BUSINESS","FIRST"])
args = parser.parse_args()

if args.load_from and (args.orig or args.dest or args.odate or args.rdate):
  parser.error("-lf/--load_from cannot be used with -o/--orig, -d/--dest, -od/--odate or -rd/--rdate !")

if args.load_from == None and (args.orig == None or args.dest == None or args.odate == None or args.rdate == None):
  parser.error("Arguments -o/--orig, -d/--dest, -od/--odate and -rd/--rdate are mandatory if -lf/--load_form not provided !")

if args.nocolor:
  disable_colored_output()

# ---- get data from live API request or from saved file
if args.load_from:
  mydict = load_data_from_file(args.load_from)
else:
  if args.airline:
    airline = args.airline.upper()
  else:
    airline = default_airline
  if args.cabin:
    cabin = args.cabin.upper()
  else:
    cabin = default_cabin
  mydict = post_request(origin=args.orig.upper(), destination=args.dest.upper(), date_voyage_aller=args.odate, date_voyage_retour=args.rdate, airline=airline, cabin=cabin)
  if args.save_to:
    save_data_to_file(mydict, args.save_to)

# ---- display data with selected format
get_lowest_and_highest_prices(mydict)

if args.raw:
  display_raw_data(mydict)
elif args.short:
  display_minimal_data(mydict)
elif args.csv:
  display_csv_data(mydict)
else:
  display_formatted_data(mydict)

# ---- happy end
exit(0)