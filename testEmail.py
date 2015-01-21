import smtplib

sender = "dnaplasteringservices@gmail.com"
recipient = "dnaplasteringservices@gmail.com"

message = "This is a test message..."


#Gmail
username = "dnaplasteringservices@gmail.com"
password = "Plastering2015!"

print("Connecting to Host...")
server = smtplib.SMTP("localhost",25)
#server.starttls()
#server.login(username, password)
print("sending mail")
server.sendmail(sender, recipient, message)

server.quit()
