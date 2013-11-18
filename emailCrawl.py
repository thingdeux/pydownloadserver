#Connect  |  Verify Inbox connectivity | check for new e-mails | check the first e-mail for something that looks like a URL |
# if there's a URL try to download it.  | if there's not  move on

import imaplib
import email
import re
import downloader

#E-mail auth information for the pydownloadserver@gmail.com inbox
#E-mail account: pydownloadserver@gmail.com
#Birthdate: January 1 1901
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
    list_to_return = []

    #For some reason the number of messages in the inbox is returned as just one string so if there are 3 messages the string is
    # '1 2 3' - so I have to run the split command to properly iterate over the inboxes messages
    for num in data[0].split():

        if valid_message == "OK":
            valid_message, data = mailbox_object.fetch(num, '(RFC822)')

            #Example of how the fetched tuple is presented - ('1 (RFC822 {2364}', 'Delivered-To: pydownloadserver@gm
            #The first segment contains the message ID '1' and the character set 'RFC822' - the next segment is the e-mail text
            #So [0][1] simply returns the e-mail text

            #find just the body of each e-mail message
            parsed_email_body = getBodyFromMailMessage(data[0][1])
            #use regex to find a url
            filtered_url = filterURLS(parsed_email_body)

            #If an actual url is found then add it to the table_to_return list
            if len(filtered_url) > 0:
                list_to_return.append(filtered_url)

    #Return a list of
    return (list_to_return)

def getBodyFromMailMessage(mail_message):
    #Used pythons email parser and chop down the ridiculousness that is e-mail by just getting the body
    parsed_message = email.message_from_string(mail_message)
    if parsed_message.is_multipart():  #All of these e-mails will be multipart but just in case
        return ( parsed_message.get_payload(0) )
    else:
        return (parsed_message.get_payload() )

def filterURLS(mail_message):

    try:
        parse_criteria = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        found_urls = parse_criteria.findall(str(mail_message) )
        number_of_returned_urls = len(found_urls)

        #If an e-mail has more than one download url in it - return the list of urls
        if number_of_returned_urls > 1:
            list_to_return = []
            for url in found_urls:
                list_to_return.append(url)

            return (list_to_return)
        else:
            return ( found_urls  )

    except:
        return (False)



def queueAllEmailInbox():
    try:
        mailbox = connectToMailbox()   #Connect to the gmail inbox
        current_inbox = getAvailableMail(mailbox)  #Get

        #Queue up each of the URLS in the inbox for download
        for url in current_inbox:
            if len(url) > 1:  #If the current URL is actually a list of URLS then process each URL
                for sub_url in url:
                    downloader.queueDownload(sub_url)
            else: #Only one download URL in the e-mail, queue it up
                downloader.queueDownload(url[0])
    except:
        return (False)


def listAllEmails():
    try:
        mailbox = connectToMailbox()   #Connect to the gmail inbox
        current_inbox = getAvailableMail(mailbox)  #Get
        returned_list = []

        #Queue up each of the URLS in the inbox for download
        for url in current_inbox:
            if len(url) > 1:  #If the current URL is actually a list of URLS then process each URL
                for sub_url in url:
                    returned_list.append(sub_url)
            else: #Only one download URL in the e-mail, queue it up
                returned_list.append(url[0])

        print(returned_list)
        #return(returned_list)
    except:
        return (False)