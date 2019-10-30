import csv

#Takes a file called sms.vmsg from the working directory. I will fix this later...

file = "sms.vmsg"

# Make some lists
listStatus = []
listSeen = []
listDate = []
listSMShex = []
hexDecode = []
listConvert = []
hexDecode1 = []
hexBuffer = []

# Make some functions.

#converts the list array of characters from the buffer to a string
def stringConvert(s):
    new = ""
    # traverse in the string
    for b in s:
        new += b
    # return string
    return new

#converts the hex characters into ASCII

def hexConvert(s1):
    pos=0
    for a1 in s1:
        #count some letters so we can loop
        length = len(s1)
        if pos <= length:
            try:
                #print(bytearray.fromhex(a1).decode())
                hexBuffer.append(bytearray.fromhex(a1).decode())
                pos=pos+1
            #needs more robust error correction
            except ValueError:
                pass

#once it has reached the end of the input characters, convert to a string, empty list etc.
        if pos >= length:
            sms = stringConvert(hexBuffer)
            print("Succesfully decoded SMS: " + str(sms))
            listConvert.append(sms)
            hexBuffer.clear()
            pos=0

#read the file and write data to lists.

print("Loading data. \n")
with open (file) as f:
    for x in f:
        if x.startswith('Date:'):
            x = x.split(':')
            x = x[1]
            listDate.append(x.strip('\n'))

        if x.startswith("SubjectENCODING"):
            #print (x)
            x = x.split(':')
            x = x[1]
            listSMShex.append(x.strip('\n'))

        if x.startswith('X-READ:'):
            x = x.split(':')
            x = x[1]
            listStatus.append(x.strip('\n'))

for z in listSMShex:
    z = z.split("=")
    sms=hexConvert(z)
      
## Zip the lists together
rows = zip(listDate,listStatus,listSMShex,listConvert)

#Write out a CSV
print("\nWriting CSV.")
with open('csv.csv', "w") as f:
    writer = csv.writer(f)
    writer.writerow(["Date: ",'Status: ', "HEX: ","Converted: "])
    for row in rows:
        writer.writerow(row)
print("Converion complete, exiting.")
