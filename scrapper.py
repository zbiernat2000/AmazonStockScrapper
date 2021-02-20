import requests
from bs4 import BeautifulSoup
import smtplib
import time

url_list = []
send_list = []
title_list = []
SENDER_EMAIL = '' #Add email that sends the message (has to be gmail)
SENDER_EMAIL_PASSWORD = '' #Add the password(
RECIEVER_EMAIL = ''#Add the email that recieves the message


def main():
    url_list.clear()
    send_list.clear()
    title_list.clear()
    with open('shoppinglist.txt', 'r') as filehandle:
        for line in filehandle:
            current_url = line[:-1]
            url_list.append(current_url)
    for x in url_list:
        check_stock(x)
    i = 0
    body = 'Check amazon link: '
    while i < len(send_list) and len(title_list):
        body += "\n" + title_list[i] + "\n" + url_list[i] + "\n"
        i+= 1
    send_mail(body)




def check_stock(URL):

    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'}#Replace with your user agent

    page = requests.get(URL, headers=headers)

    soup1 = BeautifulSoup(page.content, 'html.parser')
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    title = soup2.find(id="productTitle").get_text()
    try:
        stock = soup2.find(id="availability-string").get_text()
    except AttributeError:
        stock = soup2.find(id="availability").get_text()
    title = title.strip()

    if "In Stock." or "Available to ship" in stock:
        send_list.append(URL)
        title_list.append(title)

    print(stock)
    print(title)


def send_mail(body):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(SENDER_EMAIL, SENDER_EMAIL_PASSWORD) 

    subject = 'Items in stock'

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(SENDER_EMAIL, RECIEVER_EMAIL, msg)

    print('email has been sent')

    server.quit()

main()