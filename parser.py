
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

# List of .dat files that will be created
DATS = ['Item.dat', 'User.dat', 'Category.dat', 'Bid.dat', 'Category_Of.dat', 'Seller_Of.dat', 'Bid_Item.dat', 'Bidder_Of.dat']

# holds all userIds
bidder_dict = dict()
seller_dict = dict()
category_set = set()


bid_counter = 0
bid_counter_joint = 0
bid_counter_joint_2 = 0
counter = 0

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

def handleQuotes(str):
    if str == None or str == 'null' or str == "NULL":
        return "\"NULL\""
    str_list = []
    for char in str:
      str_list.append(char)
    str_list_new = str_list[:]
    counter = 0
    for i in range(0, len(str_list)):
      chr = str_list[i]
      if chr == '\"':
        str_list_new.insert(i+counter, '\"')
        counter += 1
    return_str = ''
    for char in str_list_new:
      return_str += char
    return_str = '"' + return_str + '"'
    return return_str

def create_item_row(item):
    row = []
    row.append(str(item['ItemID']))
    row.append(handleQuotes(item['Name']))
    try:
        buy_price = item['Buy_Price']
        if (buy_price == "null" or buy_price == "NULL" or buy_price == None):
            buy_price = -1
        else:
            buy_price = transformDollar(buy_price)
        row.append(str(buy_price))
    except KeyError:
        row.append(str(-1))
    row.append(transformDollar(item['Currently']))
    row.append(transformDollar(item['First_Bid']))
    row.append(item['Number_of_Bids'])
    row.append(transformDttm(item['Started']))
    row.append(transformDttm(item['Ends']))
    row.append(handleQuotes(item['Description']))

    return_row = '|'
    return_row = return_row.join(row)
    return return_row

def create_category_row(item):
    list_of_categories = item['Category']
    return_str = ''
    for category in list_of_categories:
        if (category not in category_set):
            return_str += (handleQuotes(category) + '\n')
            category_set.add(category)
    return return_str

def create_category_item_row(item):
    ItemID = item['ItemID']
    list_of_categories = item['Category']
    cats = set()
    return_str= ''
    for category in list_of_categories:
        if category not in cats:
            category_str = handleQuotes(category)
            return_str += ItemID + '|' +  category_str + '\n'
            cats.add(category)
    return return_str

def create_user_row_from_bidders(item):
    bids = item['Bids']
    if bids == None or bids == 'null' or bids == 'NULL':
        return
    for bid in bids:
        for bid_dict in bid:
            d = bid[bid_dict]
            bidder = d['Bidder']

            # Get bidder info
            bidder_user_id = handleQuotes(bidder['UserID'])
            rating = bidder['Rating']
            try:
                location = bidder['Location']
            except KeyError:
                location = None
            try:
                country = bidder['Countrys']
            except KeyError:
                country = None
            
            # If not present, add bidder to bidder_dict
            if country == None or country == 'null' or country == 'NULL':
                country == "\"NULL\""
            if location == None or location == 'null' or location == 'NULL':
                location == "\"NULL\""

            row = [rating, handleQuotes(country), handleQuotes(location)]
            return_str = '|'
            return_str = return_str.join(row)
            if (bidder_user_id not in bidder_dict):
                bidder_dict[bidder_user_id] = return_str
    
def create_user_row_from_sellers(item):
    addingSeller = True
    seller = item['Seller']
    seller_user_id = handleQuotes(seller['UserID'])
    seller_rating = seller['Rating']
    seller_location = item['Location']

    
    # If not present, add seller to seller_dict
    if seller_user_id not in seller_dict:
        seller_dict[seller_user_id] = seller_rating+'|'+'\"NULL\"|' + handleQuotes(seller_location)

def addBidder(user_file):
    for bidder_id in bidder_dict:
        row = bidder_id + '|' +  bidder_dict[bidder_id] + '\n'
        user_file.write(row)

def addSeller(user_file):
    for seller_id in seller_dict:
        if seller_id not in bidder_dict:
            row = seller_id + '|' +  seller_dict[seller_id] + '\n'
            user_file.write(row)

def create_bid_row(item):
    global bid_counter
    bids = item['Bids']
    if bids == None or bids == 'null' or bids == 'NULL':
        return -1
    return_str = ''
    for bid in bids:
        for bid_dict in bid:
            d = bid[bid_dict]
            time = d['Time']
            time = transformDttm(time)
            amount = d['Amount']
            amount = transformDollar(amount)
            return_str += str(bid_counter) + '|' + time + '|' + amount + '\n'
            bid_counter += 1
    return return_str

def create_user_item_row(item):
    itemId = item['ItemID']
    seller = item['Seller']
    seller_id = seller['UserID']
    return_str = itemId + '|' + handleQuotes(seller_id) + '\n'
    return return_str

def create_bidder_of_row(item):
    global bid_counter_joint
    bids = item['Bids']
    if bids == None or bids == 'null' or bids == 'NULL':
        return -1
    return_str = ''
    for bid in bids:
        for bid_dict in bid:
            d = bid[bid_dict]
            bidder = d['Bidder']
            bid_id = bid_counter_joint
            bid_counter_joint += 1
            bid_id = str(bid_id)
            bidder_id = bidder['UserID']
            return_str += bid_id + '|' + handleQuotes(bidder_id) + '\n'
    return return_str

def create_bid_item_row(item):
    global bid_counter_joint_2
    itemID = handleQuotes(item['ItemID'])
    bids = item['Bids']
    if bids == None or bids == 'null' or bids == 'NULL':
        return -1
    return_str = ''
    for bid in bids:
        for bid_dict in bid:
            bid_id = bid_counter_joint_2
            bid_counter_joint_2 += 1
            bid_id = str(bid_id)
            return_str += bid_id + '|' + itemID + '\n'
    return return_str


            

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file, length):
    global counter
    print(counter)
    open_arg = 'a'
    with open(json_file, 'r') as f, open(DATS[0], open_arg) as item_file, open(DATS[1], open_arg) as user_file, \
         open(DATS[2], open_arg) as category_file, open(DATS[3], open_arg) as bid_file, open(DATS[4], open_arg) as category_item_file, \
         open(DATS[5], open_arg) as user_item_file, open(DATS[6], open_arg) as bid_item_file, open(DATS[7], open_arg) as bid_user_file:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        for item in items:
            item_row = create_item_row(item)
            item_file.write(item_row + '\n')

            category_row = create_category_row(item)
            category_file.write(category_row)

            category_item_row = create_category_item_row(item)
            category_item_file.write(category_item_row)

            create_user_row_from_bidders(item)
            create_user_row_from_sellers(item)

            bid_rows = create_bid_row(item)
            if (bid_rows != -1):
                bid_file.write(bid_rows)

            seller_of_row = create_user_item_row(item)
            user_item_file.write(seller_of_row)

            bidder_of_row = create_bidder_of_row(item)
            if (bidder_of_row != -1):
                bid_user_file.write(bidder_of_row)

            bid_item_row = create_bid_item_row(item)
            if bid_item_row != -1:
                bid_item_file.write(bid_item_row)
        print(length)
        if counter == length - 2:
            addBidder(user_file)
            addSeller(user_file)
        counter += 1
            
            




"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        sys.stderr.write('Usage: python skeleton_json_parser.py <path to json files>')
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f, len(argv))
            print("Success parsing " + f)

if __name__ == '__main__':
    main(sys.argv)
