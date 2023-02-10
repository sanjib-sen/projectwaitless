import requests
from scrape import UseScrapper
from os import getenv
from dotenv import load_dotenv
import json

load_dotenv()
positionstack_api_key = getenv('positionstack_api_key')


'''
Address, Phone, Links - All three of the sections have same className 'Text-sc-1t0gn2o-0 esJZBM' for the innerText.
So, one workaround for this can be we can go one step back check the first child element if it's innerText is Address, phone or link.
Then we go to the second child and get the address / phone or link based on the previous result.

Another workaround can be, we iterate through the parents until we find a unique className for each of them. I follwed this and found all
of the three elements. I preferred this method over the previous one.

address_parent = "Column-sc-18hsrnn-0 flWpec"
phone_parent = "Column-sc-18hsrnn-0 bdYlQW"
links_parent = "Column-sc-18hsrnn-0 dNpgll"

Then we can just use soup.find to get our desired element by className.
'''


class Club:
    '''
    An Object-Schema for every club
    '''

    def __init__(self, id, venue_name, owner_url, location) -> None:
        self.id = id
        self.venue_name = venue_name
        self.owner_url = owner_url
        self.location = location
        ra = UseScrapper(URL=self.owner_url)
        self.city_name = ra.get_text_by_tagNclass(
            "span", "Text-sc-1t0gn2o-0 hqwJEU", index=1)
        phone_parent = ra.get_element_by_tagNclass(
            "li", "Column-sc-18hsrnn-0 bdYlQW")
        self.phone_number = UseScrapper(element=phone_parent).get_text_by_tagNclass(
            "span", "Text-sc-1t0gn2o-0 esJZBM").replace(" ", "") if phone_parent else "Not found"

        links_parent = ra.get_element_by_tagNclass(
            "li", "Column-sc-18hsrnn-0 dNpgll")
        links_child_elements = UseScrapper(element=links_parent).soup.find_all(
            "a", class_="Link__AnchorWrapper-k7o46r-1 iRSXcp") if links_parent else []

        self.club_website = "Not found"
        self.google_map = "Not found"

        for link_element in links_child_elements:
            if link_element.text.strip() == "Website":
                self.club_website = link_element.get("href").split("<")[0]
            elif link_element.text.strip() == "Maps":
                self.google_map = link_element.get("href")
        self.ra_followers = ra.get_text_by_tagNclass(
            "span", "Text-sc-1t0gn2o-0 dHaoUU")
        self.capacity = "Not found"
        '''
        The element that contains capacity has the same classname and tag
        with 40+ other elements.
        So, we have to check the elements if it contains the text capacity or not
        '''
        for element in ra.soup.find_all(
                "span", "Text-sc-1t0gn2o-0 cMSjeb"):
            if "Capacity" in element.getText().strip():
                self.capacity = element.parent.parent.find_all(
                    "span", class_="Text-sc-1t0gn2o-0 fILZhg")[0].getText().strip()
        description = ra.get_text_by_tagNclass(
            "span", "Text-sc-1t0gn2o-0 CmsContent__StyledText-g7gf78-0 icTUBR")
        self.ra_venue_description = {
            "text": description, "external_link": self.club_website} if description != "Not found" else None
        self.most_listed_artists = [{"name": artist.text.strip(), "url": "https://ra.co" + artist.get("href")} for artist in ra.soup.find_all(
            "span", class_="Text-sc-1t0gn2o-0 Link__StyledLink-k7o46r-0 kvupNG")]

        '''
        If location is not provided with parameter, it will use the google map url to get the location.
        '''
        location = self.google_map.split(
            "?q=")[1] if self.location == None and self.google_map else None

        if location != None:
            # using positionstack API to use get latitude and longitude
            open_map_url = f"http://api.positionstack.com/v1/forward?access_key={positionstack_api_key}&query={location}"
            self.venue_latitude = "Not found"
            self.venue_longitude = "Not found"
            try:
                response = requests.get(open_map_url).json()
                self.venue_latitude = response["data"][0]["latitude"]
                self.venue_longitude = response["data"][0]["latitude"]
            except:
                raise Exception(
                    "Error getting latitude and longitude data for", location)

    def __str__(self) -> str:
        '''
        Useful for printing purposes
        '''
        return json.dumps(self.__dict__, indent=2, default=str)
