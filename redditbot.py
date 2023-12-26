# get api info
# neccessary imports
import praw
import requests
import time
from api_keys import username, password, client_id, client_secret, api_key 

reddit = praw.Reddit(
    username=username, password=password,
    client_id=client_id, client_secret=client_secret,
    user_agent="a custom python script for user /" + str(username)
)

# function that checks weather condition and calls the posttoreddit function based on whether condition
# takes in a city and subreddit as a parameter
def get_weather(city,subreddit):
    base_url = "http://api.openweathermap.org/data/2.5/forecast?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city
    response = requests.get(complete_url)

    # check if the request was successful
    if response.status_code == 200:
        # parse the JSON response
        weather_data = response.json() 

        # extract relevant information from the response
        forecast_data = weather_data['list'][39]
        temperature = forecast_data['main']['temp']
        description = forecast_data['weather'][0]['description']
        temperature_fahrenheit = (temperature - 273.15) * 9/5 + 32
        date = forecast_data['dt_txt']

        # print the weather information for debugging if necessary 
   #     print(response.json())
   #     print(f'date {date}')
   #     print(f'Temperature in {city}: {temperature_fahrenheit:.2f} °F')
   #     print(f'Description: {description}')
    
        # check is it's snowing and almost or less than freezing temp
        if temperature_fahrenheit <= 34 and ('snow' in description.lower() or 'flurries' in description.lower()):
            post_to_reddit(city, temperature_fahrenheit, description, subreddit) 
    else:
        print(f"Failed to retrieve weather data for {city}. Status code: {response.status_code}")

# function that when called makes a post to reddit
# takes in a city, temperature, and weather condition and subreddit as parameters
def post_to_reddit(city, temperature, description,subreddit):
    subreddit = reddit.subreddit(subreddit) # subreddit is changable
    title = f"Weather Alert for {city}"
    body = f"In 5 days the weather at {city} will {temperature:.2f} °F and {description}. Buy your tickets early! [click here](https://summitatsnoqualmie.com/lift-tickets?)"
    submission = subreddit.submit(title, selftext=body)
    # debuging code if necessary
#   print(f"Reddit post submitted: {submission.url}")

# set the city and subreddit
city = "Snoqualmie" 
subreddit = "snowingatthesummit"

# infinite loop to run the code every 24 hours
while True:
    get_weather(city,subreddit)
    time.sleep(24 * 3600)  # sleep for 24 hours