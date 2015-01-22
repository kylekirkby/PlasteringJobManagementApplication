import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl

class Gmailer:
    
    """ This class takes a username and password aswell as the message details etc"""

    def __init__(self, user, passwd):
        
        #Login Details
        self.username = user
        self.password = passwd

        #Message Attributes

        self.message = MIMEMultipart('alternative')
        self.message['From'] = self.username
        self.sender = self.username
        
    

        #Mail Server - Gmail
        self.server = smtplib.SMTP("smtp.gmail.com", 587)


        
    def sendEmail(self, recipient, subject, message):

        self.message['Subject'] = subject
        self.message['To'] = recipient

        self.recipient = recipient

        # Create the body of the message (a plain-text and an HTML version).
        text = "{0}\r\n {1}\r\n".format(subject, message)
        html = """\r\n
        <html>
          <head></head>
          <body>
            <h4>{0}</h4>
             <p>
             {1}
            </p>
          </body>
        </html>
        """.format(subject,message)

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        self.message.attach(part1)
        self.message.attach(part2)
        
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv3)



        try:
            self.server.ehlo()
            self.server.starttls(context=context)
            self.server.login(self.username,self.password)
            self.server.sendmail(self.sender, self.recipient, message)
            #self.server.send_message(self.message)
            self.server.quit()
            return True
        except Exception as e:
            print(e)
            return False

if __name__ == "__main__":

    gmail = Gmailer("","")
    res = gmail.sendEmail("new@gmail.com","Test Email", "This is a message test!")
    if res:
        print("Sent")
    else:
        print("Failed")

        
