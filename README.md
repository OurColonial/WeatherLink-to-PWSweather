# WeatherLink-to-PWSweather
A script to query the Davis Weatherlink Live Local API and upload the data to PWSweather


## Sample PWSWeather.com API Call
Below is a sample API call to the PWSWeather update endpoint at pwsupdate.pwsweather.com/api/v1

https://pwsupdate.pwsweather.com/api/v1/submitwx?ID=STATIONID&PASSWORD=password&dateutc=2000-12-01+15:20:01&winddir=225&windspeedmph=0.0&windgustmph=0.0&tempf=34.88&rainin=0.06&dailyrainin=0.06&monthrainin=1.02&yearrainin=18.26&baromin=29.49&dewptf=30.16&humidity=83&weather=OVC&solarradiation=183&UV=5.28&softwaretype=Examplever1.1&action=updateraw

#### Required Parameters 
The following parameters are required by the PWSWeather API when making an update call.
* ID
* Password
* dateUTC
* SoftwareType

If the software or station you are using does not support a parameter other than those above, it can be omitted from the string. 

#### Full PWSWeather Parameter List

| Parameter      | Parameter Description                                      |
|:--------------:|:----------------------------------------------------------:|
| ID             | Station ID as registered                                   |
| PASSWORD       | Station Specific API Key From The PWSWeather Admin page    |
| dateutc        | Date & Time in The Format of year-mo-da+hour:min:sec     |
| winddir        | Wind Direction in Degrees from North                       |
| windspeedmph   | Current Wind Speed in Miles Per Hour (mph)                 |
| windgustmph    | Wind Gust Speed in Miles Per Hour (mph)                    |
| tempf          | Temperature in Degrees Fahrenheit                          |
| rainin         | Current Hourly Rain in Inches                              |
| dailyrainin    | Total Daily Rain in Inches                                 |
| monthrainin    | Total Monthly Rain in Inches                               |
| yearrainin     | Total Rain in Inches for the local Meteorological Year     |
| baromin        | Current Barometric Pressure in inches Hg                   |
| dewptf         | Current Dew Point in Degrees Fahrenheit                    |
| humidity       | Current Humidity Percentage                                |
| weather        | Current weather or sky conditions using standard METAR abbreviations and intensity (e.g. -RA, +SN, SKC, etc.) |
| solarradiation | Current Solar Radiation in Watts per Square Meter (w/m2)   |
| UV             | Current ultraviolet radiation                              |
| softwaretype   | Software type                                              |                 

The string always concludes with action=updateraw to indicate the end of the readings
For more information contact AerisWeather Support: https://www.aerisweather.com/support/
