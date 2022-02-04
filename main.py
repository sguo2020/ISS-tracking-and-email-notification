import requests
from datetime import datetime
import time
import smtplib

MYEMAIL = "susanguo0@gmail.com"
MYPASSWORD = "selosnoc8792"
MYLAT = 37.55
MYLNG = -121.98
MSG = "Subject:Look up! \n\nISS is visible in your area.\n" + str(datetime.now())

parameters = {
    "lat": 37.55,
    "lng": -121.98,
    "formatted": 0
}


def is_iss_overhead():
    # ISS API response
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    iss_lat = float(response.json()["iss_position"]['latitude'])
    lat_diff = abs(iss_lat - MYLAT) % 180
    iss_lng = float(response.json()["iss_position"]['longitude'])
    lng_diff = abs(iss_lng - MYLNG) % 180
    print(lat_diff, lng_diff, datetime.now())
    if lat_diff < 5 and lng_diff < 5:
        return True


def is_night():
    # Sunrise, sunset API response
    response = requests.get('https://api.sunrise-sunset.org/json', params=parameters)
    response.raise_for_status()
    # print(response.json())
    data = response.json()['results']
    sunrise = (int(data['sunrise'].split('T')[1].split(':')[0]) + 16) % 24
    sunset = (int(data['sunset'].split('T')[1].split(':')[0]) + 16) % 24
    now = datetime.now().hour
    # print(sunrise, sunset)
    if now < sunrise or now > sunset:
        return True


def send_email():
    # connection = smtplib.SMTP("smtp.gmail.com")
    connection = smtplib.SMTP("smtp.gmail.com", port=587)
    connection.starttls()
    connection.login(user=MYEMAIL, password=MYPASSWORD)
    connection.sendmail(from_addr=MYEMAIL, to_addrs=MYEMAIL, msg=MSG)
    connection.close()


# run the code every 60 seconds. |
while True:
    is_iss_overhead()
    time.sleep(5)
    # send_email()

# while the ISS.is.close to my current position, and it is currently dark
    if is_night() and is_iss_overhead():
        send_email()






