# Title: WeatherLink to PWSweather
# Version: 1.2
# Date: 31 October 2020
# Function: Because of the lack of official support from 
# Davis for PWSweather, this script queries the local 
# weatherlink API on your WLL device and ships the 
# results to the PWSweather API 
# Author: Gabriel Jaquish
# Twitter: @gabrieljaquish
# Website: gabrieljaquish.com

import argparse
import requests 
import datetime
import time
import sys
import os


# Gets the current conditions from the local WeatherLinkLive API, the IP of the device is passed as an argument
def get_current_conditions(WeatherlinkLiveIP):
    # Insert the local IP of the WeatherLink Live Device into the Current Conditions API URL
    url = "http://" + str(WeatherlinkLiveIP) + "/v1/current_conditions"
    response = requests.get(url)

    if response.status_code == 404 :
        print("Received an http 404, Page not Found for URL: " + url + "\nPlease check URL and try again.")
        exit()
    elif response.status_code != 200 :
        print("Received a " + str(response.status_code) + " http status code, please try again.")
        exit()

    return response


def upload_to_pwsweather(StationID, API_Key, response):

    # jump into the conditions section of the returned JSON
    response = response.json()["data"]["conditions"]

    # Get the current UTC Time in the format required by PWSweather
    # Format: 1900-01-01+00:00:00 or %Y-%m-%d %H:%M:%S
    utc = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    # Payload Mapping
    # Map the Davis Weatherlink API Paramaters to the PWSweather paramaters
    # For a full mapping see the mapping page of the GitHub Repository
    payload = {
        'ID' : StationID,
        'PASSWORD' : API_Key,
        'dateutc' : utc,
        'winddir' : response[0]["wind_dir_last"],
        'windspeedmph' : response[0]["wind_speed_last"],
        'windgustmph' : response[0]["wind_dir_at_hi_speed_last_10_min"],
        'tempf' : response[0]["temp"],
        'rainin' : response[0]["rainfall_last_60_min"],
        'dailyrainin' : response[0]["rainfall_last_24_hr"],
        'monthrainin' : "NULL",
        'yearrainin' : "NULL",
        'baromin' : response[2]["bar_sea_level"],
        'dewptf' : response[0]["dew_point"],
        'humidity' : response[0]["hum"],
        'weather' : "NULL",
        'solarradiation' : response[0]["solar_rad"],
        'UV' : "NULL",
        'softwaretype' : "DavisWeatherLinkLive",
        'action' : "updateraw"
    }

    # this URL provided by PWSweather for WX Submissions
    upload_url = "https://pwsupdate.pwsweather.com/api/v1/submitwx?"

    # Send the payload to PWSweather
    p = requests.post(upload_url, data=payload)
    print(str(utc) + "\tStatus Code: " + str(p.status_code) + "\tText:" + p.text, end='')

    return p.status_code

# Main Function
def main(): 

    parser = argparse.ArgumentParser(description='Accept Weatherlink IP and Processing Interval')
    parser.add_argument("WeatherlinkIP", help="IP Address of the local Davis WeatherLink Live Device")
    parser.add_argument("Interval", help='Update Interval in seconds')
    args = parser.parse_args()

    # Check for required environment variables, Station ID & APIKey
    WeatherlinkLocalIP = str(args.WeatherlinkIP)
    UploadInterval = float(args.Interval)

    # Check if the Environment variables are set, if they are set them
    if 'PWSWeatherStationID' in os.environ:
        PWSWeatherStationID = os.environ.get('PWSWeatherStationID')
    else:
        sys.exit("\nPWSweather Station ID Not Found!\nPlease set Environment Variable PWSWeatherStationID to the Station ID of your PWSweather Station.\n")

    if "PWSWeatherAPIKey" in os.environ: 
        PWSWeatherAPIKey = str(os.environ.get('PWSWeatherAPIKey'))
    else:
        sys.exit("\nAPI Key Not Found!\n\nPlease set Environment Variable PWSWeatherAPIKey to the value of your PWSWeather API Key.\nYour API Key can be found at https://dashboard.pwsweather.com\n")

    while True: 
        # get the response from the local Weatherlink API
        response = get_current_conditions(WeatherlinkLocalIP)

        # Map the weatherlink data to PWSweather and upload
        if upload_to_pwsweather(PWSWeatherStationID, PWSWeatherAPIKey, response) != 200:
            sys.exit("\nUnable to Post to PWSweather, Please see console error message.\n")

        # Wait the specified time interval before querying the API again
        time.sleep(UploadInterval)
  
# Main Function Caller
if __name__=="__main__": 
    main() 