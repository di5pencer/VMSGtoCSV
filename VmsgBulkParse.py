## Imports .vmsg files and converts them to a CSV
## of human readable text messages.
## This script uses Ansi escape codes to colour outputs.
## In incompatible sysstems it may lead to artefacts such as
## \x1b[1;31;40m appearing in the print output.

import csv
import os

#load up vmsg files in project directory

files = os.listdir()
inFiles = []
for allFiles in files:
    if allFiles.endswith('.vmsg'):
        inFiles.append(allFiles)

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
#Converts the list array of characters into a string
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
print("Loaded " + str(len(inFiles)) + " files. \n")
loopCount = 0
def vmsgConvert(fileName):
    with open(fileName) as f:
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
    print('\x1b[1;33;40m' "Conversion complete." '\x1b[0m')
    print('\x1b[1;33;40mWriting out to CSV file.\x1b[0m' + '\n\x1b[0m')
    global loopCount

    outFile = str(fileName.split('.')[0]) + ".csv"
    
    with open(outFile, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        #Add some headers to the CSV
        writer.writerow(["Date: ", 'Status: ',"Box:", "Converted: ", "Orig Values"])
        #write the rows
        for row in rows:
            writer.writerow(row)
        #Clear out the lists
        listDate.clear()
        listStatus.clear()
        listBox.clear()
        listConvert.clear()
        listSMShex.clear()  
    loopCount +=1

#Run it all. 
for vmsgFile in inFiles:
    vmsgConvert(vmsgFile)
print("\x1b[1;33;40mAll files complete.\x1b[0m")

