information = {"name":"Fasih Ahmed" ,"roll number" : "24K-0956" , "marks" :86}
print("Dictionary Keys: ")
for key in information:
    print(key)
print("Key values: ")
for i in information:
    print(information[i])
information["marks"]= 90    # marks updated to 90
print("Dictionary after upodating marks: ")
for i in information:
    print(information[i])


