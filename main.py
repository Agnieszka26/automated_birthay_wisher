import smtplib
import datetime as dt
import random
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

GMAIL_ADDRESS= os.getenv('GMAIL_ADDRESS')
GMAIL_PASSWORD= os.getenv('GMAIL_PASSWORD')
GMAIL_HOST_NAME=os.getenv("GMAIL_HOST_NAME")
PORT = int(os.getenv('PORT'))
TIMEOUT = int(os.getenv('TIMEOUT'))

# 1. Check if today matches a birthday in the birthdays.csv
now= dt.datetime.now()
today_day=now.day
today_month=now.month
letters = []
birthday_data = pd.read_csv("./birthdays.csv")
df =  birthday_data[( birthday_data['month'] == today_month) & (birthday_data['day'] == today_day)]

# 2. If step 1 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual
# name from birthdays.csv

if not df.empty:
    b_email= df.email.item()
    b_name=df.name.item()

    for i in range(1,4):
        with open(f"./letter_template/letter_{i}.txt") as letter_file:
            letters.append(letter_file.read())

    letter = random.choice(letters)

    letter = letter.replace("[NAME]",b_name)

# 3. Send the letter generated in step 3 to that person's email address.
    with smtplib.SMTP(GMAIL_HOST_NAME, PORT, timeout=TIMEOUT) as connection:
        connection.starttls()
        connection.login(GMAIL_ADDRESS, GMAIL_PASSWORD)
        connection.sendmail(from_addr=GMAIL_ADDRESS, to_addrs=b_email, msg=f"Subject:Birthday wishes \n\n"
                                                                           f"{letter}")



