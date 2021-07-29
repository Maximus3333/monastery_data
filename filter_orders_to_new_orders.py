import csv


with open('Data\orders.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    with open('new_orders.csv', 'w') as new_file:
        orderNumList = []
        duplicates = []
        csv_writer = csv.writer(new_file)
        i = 0
       
        for line in csv_reader:
            if i == 0:
                csv_writer.writerow(line)
            i += 1
            if line['Order Number'] not in orderNumList and len(line['Order Number']) != 7:
                if line['Store Name'] != 'Bread List' and line['Store Name'] != 'Manual Orders':
                    orderNumList.append(line['Order Number'])
                    # csv_read_writer.writerow(line.values())
            else:
                duplicates.append(line['Order Number'])
        
        print(duplicates)
        for duplicate in duplicates:
            for orderNum in orderNumList:
                if duplicate[0:5] == orderNum:
                    orderNumList.remove(duplicate[0:5])
        
        csv_file.seek(0) 
        for line in csv_reader:
            if line['Order Number'] in orderNumList:
                csv_writer.writerow(line.values())
     

with open('new_orders.csv', 'r') as new_file:
    reader = csv.DictReader(new_file)
    occurences = {}
    for line in reader:
        occurences[line['Order Number']] = occurences.get(line['Order Number'], 0) + 1

with open('pythonOutputCode3.txt', 'w') as f:
    for d, e in occurences.items():
        f.write(str(d) + ' | ' + str(e))
        f.write('\n')