from datetime import timedelta, date
import smtplib, ssl
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "ssc.project.tracker@gmail.com"  # Enter your address
password = 'Parks12345'

class RFI:
    
    def __init__(self, rfi_number, date_received, title, dwg_refer, spec_refer, assigned_to,team_list):

        self.rfi_number = rfi_number
        self.date_received = date_received
        self.title = title
        self.dwg_refer = dwg_refer
        self.spec_refer = spec_refer
        self.assigned_to = assigned_to
        self.date_response = ''
        self.response = ''
        self.reviewer=''
        self.orig_file=''
        self.response_file=''
        self.team_list=team_list
        self.cost_change=False
        self.time_change=False

        dates= self.date_received.split('/')
        received_date=date(int(dates[2]),int(dates[0]),int(dates[1]))
        
        self.date_due = received_date + timedelta(7)
        
    def notify(self):

        emails = {
                  'Engineer':'gregory.stone@parks.ca.gov',
                  'Architect':'test@parks.ca.gov',
                  'Natural':'test@parks.ca.gov',
                  'Cultural':'test@parks.ca.gov',
                  'Project Manager':'test@parks.ca.gov'
                  }                        
        receiver_email=emails[self.assigned_to]
       
        
        message='''\
            Subject: [New RFI] for **insert project name**
            
            You have been assigend a new RFI for **insert project name**

            {} - {}
            Response is due by {}

            **Automated Message Sent by SSC Project Tracker**

            '''.format(self.rfi_number,self.title,self.date_due)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
       
            


