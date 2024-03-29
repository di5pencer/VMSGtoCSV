import csv

#Takes a file called sms.vmsg from the working directory.

file = "sms.vmsg"

# Make some lists
listStatus = []
listSeen = []
listDate = []
listBox=[]
listSMShex = []
hexDecode = []
listConvert = []
hexBuffer = []

# Make some functions.

#converts the list array of characters into a string
def stringConvert(stringInput):
    new = ""
    for b in stringInput:
        new += b
    # return string
    return new.strip('\n')

#converts the hex characters into ASCII
def hexConvert(stringInput2):
    pos = 0
    sms = ""
    for hexCharacter in stringInput2:
        #count some letters so we can loop
        length = len(stringInput2)
        if pos <= length:
            try:
                #print(bytearray.fromhex(a1).decode())
                #unicode to prevent errors with certain characters
                hexBuffer.append(bytearray.fromhex(
                    hexCharacter.strip('\n')).decode('unicode_escape'))
                pos = pos+1
            #Needs more robust error correction
            #Prints error message
            except ValueError as e:
                print('\x1b[1;31;40m' + "Error!!" +
                      '\x1b[0m')
                print('\x1b[1;31;40m' + str(e) + '\x1b[0m')
                #pass

#Once it has reached the end of the input characters, convert to a string, empty list etc.
        if pos >= length:
            sms = stringConvert(hexBuffer)
            print('\x1b[1;32;40m' + "Succesfully decoded SMS:" +
                  '\x1b[0m' +" " + str(sms))
            hexBuffer.clear()
            pos = 0
            return sms

#Read the file and write data to lists.

print('\x1b[1;33;40mLoading data.\x1b[0m\n')

with open(file) as f:
    for x in f:
        if x.startswith('Date:'):
            x = x.split(':')
            x = x[1]
            listDate.append(x.strip('\n'))

        if x.startswith('X-BOX:'):
            x = x.split(':')
            x = x[1]
            listBox.append(x.strip('\n'))

        if x.startswith("SubjectENCODING"):
            #print (x)
            x = x.split(':')
            x = x[1]
            listSMShex.append(x.strip('\n'))
            message = x.split('=')
            message1 = hexConvert(message)
            listConvert.append(message1)

        if x.startswith('X-READ:'):
            x = x.split(':')
            x = x[1]
            listStatus.append(x.strip('\n'))

## Zip the lists together
rows = zip(listDate, listStatus,listBox, listConvert,listSMShex)

#Write out a CSV
print('\n\x1b[1;33;40mWriting CSV.\x1b[0m')
with open('output.csv', "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    #add some headers
    writer.writerow(["Date: ", 'Status: ',"Box:", "Converted: ", "Orig Values"])
    #write the rows
    for row in rows:
        writer.writerow(row)

print('\x1b[1;33;40m' "Conversion complete, exiting." '\x1b[0m')
