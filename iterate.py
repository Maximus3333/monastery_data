import csv
from os import write
import re


orders_net_volume = {}
gross_volume_dic = {}
with open('Data\orders-items1of4.csv', 'r', encoding='Latin1') as orders_file:
    reader_orders_file = csv.DictReader(orders_file)
    with open('Data\weights_for_shipper.csv') as icon_info:
        reader_icon_info = csv.DictReader(icon_info)
        with open('Data\weight_list.csv') as A_series_icon_info:
            reader_A_series_icon_info = csv.DictReader(A_series_icon_info)
        
            order_items = {}
            volume_of_products = {}
            # sets order numbers as keys to the dict order_items
            for line in reader_orders_file:  
                order_items[line['order number']] = {}
            orders_file.seek(0)
            
            #assigns the sku numbers of each product to the associated order
            
            for line2 in reader_orders_file:
                if line2['sku'] != 'sku':
                    #matchs sku number and associated
                    sku_match = re.match(r"^([ABDGHJLMRS])-?0{0,2}(\d{1,3})([A-Z]?)", line2['sku'])
                # print(str(match) + ' | ' + line2['Item ID']) 
                    size_match = re.search(r"(\d{1,2}) ?(x) ?(\d{1,2}) ?(mounted|laminated|lamination)|\[([A-Z])|(mounted|hard plastic)", line2['item options'])
                    try:
                        sku = sku_match.group(1) + '-' + sku_match.group(2)
                        # print(sku)
                        if (sku[0] == 'R'):
                            sku += 'M'
                        else:
                            if (sku[0] == 'A') and (size_match.group(1) + size_match.group(2) + size_match.group(3) != '8x10'):
                                sku += '.' + size_match.group(1) + size_match.group(2) + size_match.group(3)
                                if size_match.group(4) == 'mounted':
                                    sku += 'M'
                                else:
                                    sku += 'P'
                            elif (sku[0] == 'D'):
                                # print(sku)
                                try:
                                    if size_match.group(6) == 'mounted' or size_match.group(6) == 'hard plastic':
                                        sku += 'M'
                                except AttributeError:
                                    sku += 'P'
                                    # print(sku, line2['order number'])
                                # print(sku, line2['order number'])
                            else:
                                # print(sku)
                                sku += str(sku_match.group(3))
                                print(sku_match.group(3))
                                try:
                                    if sku[0] == 'A':
                                        if size_match.group(1) + size_match.group(2) + size_match.group(3) == '8x10':
                                            # print(sku)

                                            if size_match.group(4) == 'laminated' or size_match.group(4) == 'lamination':
                                                sku += 'P'
                                except AttributeError:
                                    # print(sku)
                                    pass
                                try:
                                    if size_match.group(5):
                                        sku += size_match.group(5)                               
                                except AttributeError:
                                    # print(sku, line2['order number'])
                                    pass
                            try:
                                if size_match.group(3) == '8x10':
                                    print(sku)

                                    if size_match.group(4) == 'mounted':
                                        sku += 'M'
                                    else:
                                        sku += 'P'
                            except AttributeError:
                                # print(sku)
                                pass
                        order_items[line2['order number']][sku] = line2['quantity']
                      
                    except AttributeError:
                        # print(sku)
                        # print(sku, line2['order number'])
                        pass
                    
#todo: remove this
            for c, v in order_items.items():
                if c == '37019':
                    print(c,v)
            
            # assigns each product sku as key and gives it a default of sku of 1 in dict
            for order_values in order_items.values():
                for sku in order_values:
                    # print(sku)
                    volume_of_products[sku] = 0
            # print(volume_of_products.keys())

            # calculates volumes for each sku and replaces the default sku of 1
            for lines3 in reader_icon_info:
                dimensions_list = [lines3['Width'], lines3['Height'], lines3['Depth']]
                i = 0
                for dimension in dimensions_list:
                    if dimension != 0:
                        try:
                            dimensions_list[i] = float(dimension)
                            # print(i)
                            # print(dimensions_list[i])
                            
                        except ValueError:
                            dimension_match = re.match("^(\d*)(?: *|-)(\d+ ?)/(\d+)$", dimension)
                            # print(dimension_match.group(1))
                            try:
                                dimensions_list[i] = float(dimension_match.group(1)) + float(dimension_match.group(2))/float(dimension_match.group(3))
                            except ValueError:
                                dimensions_list[i] = float(dimension_match.group(2))/float(dimension_match.group(3))                      
                    else:
                        dimensions_list[i] = float(0)
                    i+=1
                    
                volume = 1
                for dimension in dimensions_list:
                    volume *= dimension
                        # print(lines3['Product_ID'])
                volume_of_products[lines3['Product_ID']] = volume
                        
            # calculates volume of a series skus
            for lines4 in reader_A_series_icon_info:
                dimensions_list = [lines4['width'], lines4['height'], lines4['depth']]
                i = 0

                for dimension in dimensions_list:
                    if len(dimension) != 0:
                        dimensions_list[i] = float(dimension)
                    else:
                        dimensions_list[i] = float(0)
                    i+=1
                volume = 1
                for dimension in dimensions_list:
                    volume *= dimension
                volume_of_products[lines4['Sku']] = volume

                
            with open('pythonOutputCode.txt', 'w') as f:
                for d, e in volume_of_products.items():
                    f.write(str(d) + ' | ' + str(e))
                    f.write('\n')
            
            # calculates the net volume for each order 
            
            for key, skus in order_items.items():
                volume_of_order = 0
                missing_volume = False
                missing_volumes_in_order = ''
                for sku in skus:
                    if volume_of_products[sku] != float(0):
                        volume_of_order += volume_of_products[sku] * float(order_items[key][sku])
                    else:
                        missing_volume = True
                        missing_volumes_in_order += ' ' + sku
                        # print(sku)
                orders_net_volume[key] = volume_of_order
                # if missing_volume:
                #     orders_net_volume[key] += ' <-- missing volume: ' + missing_volumes_in_order
                # print(key, ' | ', items, ' | ', volume_of_order)

            # with open('pythonOutputCode.txt', 'w') as f:
            #     for d, e in orders_net_volume.items():
            #         f.write(str(d) + ' ' + e)
            #         f.write('\n')

with open('new_orders.csv', 'r') as all_order_data:
    reader_all_order_data = csv.DictReader(all_order_data)
    box_type = {}
    box_type['RRA'] = 11.0625*2.5*13.0625
    box_type['Fdx S Box'] = 10*12
    box_type['SFRB'] = 5.4375*8.6875*1.75
    box_type['LFRB'] = 12.25*12.25*6
    box_type['MFRB'] = 11.25*8.75*6
    box_type['RRB'] = 12.25*10.5*5.5
    envelope_counter = 0
    for line in reader_all_order_data:
        if line['Package Type'] in box_type:
            gross_volume_dic[line['Order Number']] = box_type[line['Package Type']]
        elif line['Package Type'] == 'FRPE' or line['Package Type'] == 'Th' or line['Package Type'] == 'Lg Env' or line['Package Type'] == 'FRE':
            envelope_counter += 1
        else:
            try:
                volume = float(line['Package Width']) * float(line['Package Height']) * float(line['Package Length'])
                if volume != 0:
                    gross_volume_dic[line['Order Number']] = volume
            except ValueError:
                pass
    print(envelope_counter)


# print(gross_volume_dic)

gross_net_volume = {}

for order_number, gross_vol in gross_volume_dic.items():
    gross_net_vol_dict = {}
    if order_number in orders_net_volume.keys():
        gross_net_vol_dict['Gross Volume'] = gross_vol
        gross_net_vol_dict['Net Volume'] = orders_net_volume[order_number]
        gross_net_volume[order_number] = gross_net_vol_dict

# print(gross_net_volume)


# with open('pythonOutputCode2.txt', 'w') as f:
#                 for d, e in orders_net_volume.items():
#                     f.write(str(d) + ' ' + str(e))
#                     f.write('\n')

with open('order_gross_and_net_volumes.csv', 'w', newline='') as f:
    # f.write('Order_Number ')
    # f.write('Gross Volume ')
    fieldnames = ['Order_Number', 'Gross Volume', 'Net Volume']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for order_number, volumes in gross_net_volume.items():
        writer.writerow({ fieldnames[0]: order_number, fieldnames[1]: volumes['Gross Volume'], fieldnames[2]: volumes['Net Volume']})
        # writer.write(str(d) + ' ' + str(e))
        # writer.write('\n')


# line 50 height numerator

# print(orders_net_volume)