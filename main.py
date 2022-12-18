import random
from datetime import datetime
import pandas

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "jonsnow9091.fs@gmail.com"  # Enter your address
receiver_emails = ['kenan9091.fs@gmail.com', 'semraarik91@gmail.com',
                   'gsarik1414@gmail.com', 'frank9091.johansen@gmail.com']  # Enter receiver address
password = "piqsebtpohevyzin"




now = datetime.now()
today_day = now.day
today_month = now.month
today_tuple = (today_month, today_day)
print(today_tuple)

data = pandas.read_csv('birthdays.csv')

print(data)


# birthdays_dict = {
#     (data['month'], data['day']): ('03', '02')
# }

birthdays_dict = {(data_row['month'], data_row['day']): data_row for (index, data_row) in data.iterrows()}

# print(birthdays_dict)

# print(data['email'])

if today_tuple in birthdays_dict:
    birthday_person = birthdays_dict[today_tuple]
    with open(f'letter_templates/letter_{random.randint(1,3)}.txt') as letter_file:
        new_letter_file = letter_file.read()
        new_letter_file = new_letter_file.replace('[NAME]', birthday_person['name'])
        print(birthday_person['email'])

        receiver_emails.append(birthday_person['email'])

        message = MIMEMultipart("alternative")
        message["Subject"] = "multipart test"
        message["From"] = sender_email
        message["To"] = ", ".join(receiver_emails)
        # message["To"] = receiver_email
        # for receiver_email in receiver_emails:
        #     message["To"] = receiver_email
        #     print(receiver_email)


        # Create the plain-text and HTML version of your message
        text = """\
           Hi,
           How are you?
           Real Python has many great tutorials:
           www.realpython.com"""

        html = """\
           <html>
             <body>
               <p>Hi,<br>
                  How are you?<br>
                  <a href="http://www.realpython.com">Real Python</a> 
                  has many great tutorials.
               </p>

             </body>
           </html>
           """ + f'{new_letter_file}'

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_emails, message.as_string())