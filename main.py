import requests
import smtplib
import time
from datetime import datetime

#------------------LATITUDE AND LONGITUDE--------------------#
MY_LAT = 51.66337967
MY_LONG = 32.67463884
#You should enter gmail for EMAIL constant but RECIPIENT_EMAIL can be anything#
EMAIL = ""
PASSWORD = ""
RECIPIENT_EMAIL = ""
#----------------------------ISS API REQUEST-------------------------------#
response = requests.get("http://api.open-notify.org/iss-now.json")
response.raise_for_status()
iss_data = response.json()

iss_longitude = float(iss_data["iss_position"]["longitude"])
iss_latitude = float(iss_data["iss_position"]["latitude"])


#------------------------API REQUEST Sunrise Sunset-------------------------#
parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}
response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()

sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

#------------------------------CURRENT TIME HOUR------------------------------#
now = datetime.now()
current_hour = now.hour

#------------------------SEND MAIL WHEN ISS IS CLOSE--------------------------#
while True:
    time.sleep(60)
    if iss_latitude in range(45, 57) and iss_longitude in range(27, 37) and (current_hour > sunset or current_hour < sunrise):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=EMAIL,
                to_addr=RECIPIENT_EMAIL,
                msg="Subject:Iss is close!\n\nLook up!"
            )

#===============================================================================#