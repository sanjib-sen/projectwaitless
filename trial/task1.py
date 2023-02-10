

# Task 1

import csv
from club import Club


def complete_csv():
    csv_input = open(
        'trial/resources/residentadvisor_root_db_rows.csv', mode='r')
    csv_output = open('trial/resources/output.csv', mode='w')
    csv_reader = csv.DictReader(csv_input)

    list_of_clubs = []
    for row in csv_reader:
        id = row["id"]
        venue_name = row["venue_name"]
        owner_url = row["owner_url"]
        location = row["location"]
        print("Currently processing", id)
        club = Club(id, venue_name, owner_url, location)
        print(club)
        list_of_clubs.append(club.__dict__)

    writer = csv.DictWriter(
        csv_output, fieldnames=list_of_clubs[0].__dict__.keys())
    writer.writeheader()
    writer.writerows(list_of_clubs)
    csv_input.close()
    csv_output.close()
