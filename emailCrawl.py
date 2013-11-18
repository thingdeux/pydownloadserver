#If you work now - eff you!!

#Better to use the built in smtp library probably

#Connect  |  Verify Inbox connectivity | check for new e-mails | check the first e-mail for something that looks like a URL |
# if there's a URL try to download it.  | if there's not  move on

#E-mail account: pydownloadserver@gmail.com
#Birthdate: January 1 1901
#

import imaplib
import re

#E-mail auth information for the pydownloadserver@gmail.com inbox
emailUsername = "pydownloadserver"
emailPassword = "Kaiser123"
popHostName = "imap.gmail.com"
popPort = "993"

#Create an imaplib mailbox Object
def connectToMailbox():
    try:
        #Attempt connection to google imap server with user/pass - and return
        a_mailbox = imaplib.IMAP4_SSL(popHostName, popPort)
        a_mailbox.login(emailUsername, emailPassword)
        return (a_mailbox)
    except:
        print("unable to access email box")


#Attempt to acquire list of all e-mail in the inbox.
def getAvailbleMail(mailboxObject):
    availableMail = mailboxObject.select()
    return (availableMail)




mailbox = connectToMailbox()
test = getAvailbleMail(mailbox)

print(test)

#queueDownload(url) function from Jasons file to queue a download