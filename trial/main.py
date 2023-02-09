'''
Address, Phone, Links - All three of the sections have same className 'Text-sc-1t0gn2o-0 esJZBM' for the innerText.
So, one workaround for this can be we can go one step back check the first child element if it's innerText is Address, phone or link.
Then we go to the second child and get the address / phone or link based on the previous result.

Another workaround can be, we iterate through the parents until we find a unique className for each of them. I follwed this and found all
of the three.

address_parent = "Column-sc-18hsrnn-0 flWpec"
phone_parent = "Column-sc-18hsrnn-0 bdYlQW"
links_parent = "Column-sc-18hsrnn-0 dNpgll"

Now we can just use soup.find to get our desired element by className.
'''

# Task 1

import csv
from club import Club


csv_input = open('trial/resources/residentadvisor_root_db_rows.csv', mode='r')
csv_output = open('trial/resources/output.csv', mode='w')
csv_reader = csv.DictReader(csv_input)
writer = csv.DictWriter(csv_output, fieldnames=Club.__dict__)
writer.writeheader()
for row in csv_reader:
    id = row["id"]
    venue_name = row["venue_name"]
    owner_url = row["owner_url"]
    location = row["location"]
    print("Currently processing", id)

    club = Club(id, venue_name, owner_url, location)
    writer.writerow(club.__dict__)

csv_input.close()
csv_output.close()
