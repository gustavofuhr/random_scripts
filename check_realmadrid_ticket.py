import time

import smtplib
import ssl
from email.message import EmailMessage

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


TICKETS_URL = "https://www.realmadrid.com/en-US/tickets?filter-tickets=vip;general&filter-football=primer-equipo-masculino"
GMAIL_SENDER_EMAIL = "YOUR EMAIL"
GMAIL_APP_PASSWORD = "GMAIL APP PASSWORD"
RECIPIENT_EMAIL = GMAIL_SENDER_EMAIL
CHECK_INTERVAL = 5*60 # in seconds
SEND_PING_INTERVAL = 60*60 # in seconds


def send_email(sender_gmail_address, gmail_app_password, to_email_address, subject_txt, message_txt = ""):
    port = 465  # This is the default SSL port
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_gmail_address, gmail_app_password)
        
        msg = EmailMessage()
        msg['Subject'] = subject_txt
        msg['From'] = sender_gmail_address
        msg['To'] = to_email_address
        msg.add_header('Content-Type', 'text')
        msg.set_payload(message_txt)

        server.sendmail(sender_gmail_address, to_email_address, msg.as_string())


def still_checking_alert():
    print("sending still checking")
    send_email(GMAIL_SENDER_EMAIL, GMAIL_APP_PASSWORD, RECIPIENT_EMAIL, "[MadridTickets] no change, still checking...")

def change_alert():
    print("sending change alert")
    send_email(GMAIL_SENDER_EMAIL, GMAIL_APP_PASSWORD, RECIPIENT_EMAIL, "[MadridTickets] GOT A CHANGE THERE! GO CHECK!", TICKETS_URL)

def error_alert(error_txt):
    print("sending error alert")
    send_email(GMAIL_SENDER_EMAIL, GMAIL_APP_PASSWORD, RECIPIENT_EMAIL, "[MadridTickets] GOT AN ERROR!", error_txt)



def check_ticket_availability(match_date_string):

    s = Service('/usr/lib/chromium-browser/chromedriver')
    driver = webdriver.Chrome(service=s)
    wait = WebDriverWait(driver, 20)


    time_elapsed = 0    
    while True:
        try:
            print()
            driver.get(TICKETS_URL)

            xpath_str = "//*[contains(text(), '" + match_date_string + "')]/../.."

            wait.until(EC.visibility_of_element_located((By.XPATH, xpath_str)))
            card_elem = driver.find_elements_by_xpath(xpath_str)[0]

            print("Searching in:", card_elem.text)
            if "entradas-aforo-general disponibles-proximamente" not in card_elem.text and \
                    "Tickets for general public available soon" not in card_elem.text:
                # tickets are open, or we have an error. Either way, send me an email.
                print("SOMETHING HAS CHANGED!")
                change_alert()
                break
            else:
                print("Just checked. Seemes the same")

            time.sleep(CHECK_INTERVAL)
            time_elapsed += CHECK_INTERVAL
            if time_elapsed > SEND_PING_INTERVAL:
                time_elapsed = 0
                still_checking_alert()
        except Exception as e:
            error_alert(str(e))

    driver.quit()

if __name__ == "__main__":
    check_ticket_availability("Tuesday, May 14")