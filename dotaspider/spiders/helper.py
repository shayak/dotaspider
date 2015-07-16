def sendMail(data):
    import smtplib
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText

    gmailUser = 'dotaspider007@gmail.com'
    gmailPassword = 'dotapass'
    recipient = 'dotaspider007@gmail.com'
    title = '{0} vs {1}'.format(data['team1'], data['team2'])
    html="""\
    <html>
      <head></head>
        <body>
            <a href="{0}" style="text-decoration:none">
                {1} ({2}) vs {3} ({4})
            </a>
        </body>
    </html>
    """.format(data['link'], data['team1'], data['odds1'], data['team2'], data['odds2'])

    msg = MIMEMultipart()
    msg['From'] = gmailUser
    msg['To'] = recipient
    msg['Subject'] = title
    msg.attach(MIMEText(html, 'html'))

    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmailUser, gmailPassword)
    mailServer.sendmail(gmailUser, recipient, msg.as_string())
    mailServer.close()

def nameMatch(namelist, string):
    for name in namelist:
        if (name in string.lower()):
            return True
    return False
