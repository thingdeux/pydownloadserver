#Connect  |  Verify Inbox connectivity | check for new e-mails | check the first e-mail for something that looks like a URL |
# if there's a URL try to download it.  | if there's not  move on

#E-mail account: pydownloadserver@gmail.com
#Birthdate: January 1 1901

import imaplib
import email

#E-mail auth information for the pydownloadserver@gmail.com inbox
email_username = "pydownloadserver"
email_password = "Kaiser123"
imap_host_name = "imap.gmail.com"
imap_port = "993"

#Create an imaplib mailbox Object
def connectToMailbox():
    try:
        #Attempt connection to google imap server with user/pass - and return
        mailbox_object = imaplib.IMAP4_SSL(imap_host_name, imap_port)
        mailbox_object.login(email_username, email_password)
        return (mailbox_object)
    except:
        print("unable to access email box")


#Attempt to acquire list of all e-mail in the inbox.
def getAvailableMail(mailbox_object):
    mailbox_object.select()
    valid_message, data = mailbox_object.search(None, 'ALL')
    table_to_return = []

    #For some reason the number of messages in the inbox is returned as just one string so if there are 3 messages the string is
    # '1 2 3' - so I have to run the split command to properly iterate over the inboxes messages
    for num in data[0].split():

        if valid_message == "OK":
            valid_message, data = mailbox_object.fetch(num, '(RFC822)')

            #Example of how the fetched tuple is presented - ('1 (RFC822 {2364}', 'Delivered-To: pydownloadserver@gm
            #The first segment contains the message ID '1' and the character set 'RFC822' - the next segment is the e-mail text
            #So [0][1] simply returns the e-mail text

            #Add just the body of each e-mail message to a table and when finished return said table.
            parsed_email = getBodyFromMailMessage(data[0][1])
            table_to_return.append(parsed_email)

    return (table_to_return)

def getBodyFromMailMessage(mail_message):
    #Used pythons email parser and chop down the ridiculousness that is e-mail by just getting the body
    parsed_message = email.message_from_string(mail_message)
    if parsed_message.is_multipart():  #All of these e-mails will be multipart but just in case
        return ( parsed_message.get_payload(0) )
    else:
        return (parsed_message.get_payload() )


mailbox = connectToMailbox()
current_inbox = getAvailableMail(mailbox)

for test_email in current_inbox:
    print test_email


#queueDownload(url) function from Jasons file to queue a download