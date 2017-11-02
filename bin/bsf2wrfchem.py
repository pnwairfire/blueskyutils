import csv

with open('fire_locations_20130817.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    #this function skips the first line, which in this case is the label for the column
    #next(csv_reader)

    for line in csv_reader:
        print(line['latitude'])