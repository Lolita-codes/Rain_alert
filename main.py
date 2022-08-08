import requests
from twilio.rest import Client
import os
from dotenv import load_dotenv
load_dotenv('.env')


account_sid = os.environ['account_sid']
auth_token = os.environ['auth_token']
twilio_account_number = os.environ['twilio_account_number']
api_key = os.environ['api_key']
phone_number = os.environ['phone_number']

my_latitude = os.environ['my_latitude']
my_longitude = os.environ['my_longitude']

parameters = {
    'lat': my_latitude,
    'lon': my_longitude,
    'appid': api_key,
    'exclude': 'current,minutely,daily,alerts'
}

# Gets the weather details for the next 12 hours
response = requests.get(url='https://api.openweathermap.org/data/2.5/onecall', params=parameters)
response.raise_for_status()
data = response.json()['hourly'][:12]

will_rain = False

# Checks if it will rain
for hourly_data in data:
    weather_code = hourly_data['weather'][0]['id']
    if int(weather_code) < 700:
        will_rain = True

    if will_rain:
        # Sends a message if it will rain
        client = Client(account_sid, auth_token)

        message = client.messages \
            .create(
            body="It's going to rain today. Don't forget to bring an Umbrella",
            from_=twilio_account_number,
            to=phone_number
        )
        print(message.status)
