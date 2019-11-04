# VMSGtoCSV
Extracts SMS from VMSG and converts to them to a CSV file. This works with the VMSG format output by OPPO phones.
These phones convert ASCII Characters to HEX values in the SMS backup file. 

VmsgParse takes an inout file called "sms.vmsg".
VmsgBulkParse should attempt to load all .vmsg files in the directory and convert them.

At present there is little to no error corection or validation, so results need to be checked to ensure accuracy.



 OPPO VMSG conversion


