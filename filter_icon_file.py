import csv

with open('new_icon.csv', 'w', encoding='Latin1') as n_i:
    writer = csv.writer(n_i)

    with open('Data\icon.csv', 'r', encoding='Latin1') as orders_file:
        reader_orders_file = csv.DictReader(orders_file)
        i=0
        for line in reader_orders_file:
            if i == 0:
                writer.writerow(line)
            i+=1
            if line['Store'] != 'Bread List' and line['Store'] != 'Manual Orders':
                    writer.writerow(line.values())
            else:
                print(line['Order Number'])