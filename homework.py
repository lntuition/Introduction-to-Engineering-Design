import email
import imaplib
import base64
import zipfile
import sys
import os

# -------------------------------- Usage -------------------------------
# mailId : email Id
# mailPassword : email Password
# homeworkId : homework number (example : 4 includes 4 and 4_1)
# saveDir : Directory to save attachments, default is current directory
# isZipped : if isZipped is True, unzipped attachments after download

mailId = ''
mailPassword = ''
studentId = ["20181632", "20181699", "20171704", "20181671", "20181676", "20181622", "20181628"]
homeworkId = ""
saveDir = '.'
isZipped = True
isCfile = True

# Need to Change Upper Variables
def Decode(s, encodings=('UTF', 'ISO-8859-1')):
    for encoding in encodings:
        try:
            return s.decode(encoding)
        except UnicodeDecodeError:
            pass

def Decode_with_chardet(s):
    import chardet
    try:
        return s.decode(chardet.detect(s)['encoding'])
    except UnicodeDecodeError:
        print(UnicodeDecodeError)

def MakeCriteria(studentId):
    criteria = ""
    for i in range(len(studentId)):
        criteria = criteria + 'SUBJECT ' + studentId[i] + ' '
        if i != 0:
            criteria = 'OR ' + criteria 
    return criteria;

if __name__ == "__main__":
    mail = imaplib.IMAP4_SSL('imap.gmail.com',993)
    response, account = mail.login(mailId, mailPassword)
    if response != 'OK':
        print("Not able to login to e-mail, check id/password please")
        sys.exit()
    
    mail.select('INBOX')
    mail.literal = ('실습' + homeworkId).encode('UTF-8')
    response, data = mail.search('UTF-8', MakeCriteria(studentId) + 'SUBJECT')
    if response != 'OK':
        print("Not able to search e-mail by criteria")
        sys.exit()

    zipFileSet = set()
    if 'zipfile' not in os.listdir(saveDir):
        os.mkdir('zipfile')
        
    for mId in data[0].split():
        response, messageParts = mail.fetch(mId, '(RFC822)')
        if response != 'OK':
            print("Not able to fetch e-mail")
            sys.exit()

        for part in email.message_from_string(Decode(messageParts[0][1])).walk():
            if part.get('Content-Disposition') is None:
                continue

            zipFileName = email.header.decode_header(part.get_filename())
            if type(zipFileName[0][0]) is bytes:
                zipFileName = zipFileName[0][0].decode(zipFileName[0][1])
            elif type(zipFileName[0][0]) is str:
                zipFileName = zipFileName[0][0]
            zipFileSet.add(zipFileName)
        
            fp = open(os.path.join(saveDir, 'zipfile') + '\\' + zipFileName, 'wb')
            fp.write(part.get_payload(decode=True))
            fp.close()

    mail.close()
    mail.logout()

    cFileSet = set()
    if isZipped is True:
        for zipFileName in zipFileSet:
            try:
                zipFile = zipfile.ZipFile(os.path.join(saveDir, 'zipfile') + '\\' + zipFileName)
            except zipfile.BadZipFile:
                print(zipFileName, "is not ZipFile")
                continue

            if 'cfile' not in os.listdir(saveDir):
                os.mkdir('cfile')
            
            for zipInfo in zipFile.infolist():
                zipInfo.filename = zipInfo.filename.encode('CP437').decode('CP949')
                cFileSet.add(zipInfo.filename)
                zipFile.extract(zipInfo, os.path.join(saveDir, 'cfile'))
            zipFile.close()


    if isCfile is True:
        if 'exefile' not in os.listdir(saveDir):
            os.mkdir('exefile')
            os.chdir('exefile/')
        
        for cFileName in cFileSet:
            os.system('cl ../cfile/' + cFileName)
