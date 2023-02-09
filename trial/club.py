import requests
from scrape import UseScrapper
from os import getenv

positionstack_api_key = getenv('positionstack_api_key')


class Club:
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
        location = self.google_map.split(
            "?q=")[1] if self.location == None and self.google_map else None

        if location != None:
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
