import smtplib
import requests
from datetime import datetime
import os

my_mail = os.environ.get("MY_MAIL")
password = os.environ.get("MY_PASSWORD")

MY_LAT = -32.92700204623853
MY_LONG = -60.6647053653211

#Your position is within +5 or -5 degrees of the ISS position.

#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.

def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True

def is_night():
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

    time_now = datetime.now()

    if time_now >= sunset and time_now <= sunrise:
        return True

    if is_iss_overhead() and is_night():
        try:
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(my_mail, password)
                connection.sendmail(from_addr=my_mail, to_addrs=my_mail, msg=f"Subject:Look Up!\n\n The ISS is passing overhead.")
        except Exception as e:
            print("Error sending email",e)
