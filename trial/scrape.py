import requests
from bs4 import BeautifulSoup
from os import getenv

scrapeops_api_key = getenv('scrapeops_api_key')


def use_requests(URL):
    try:
        response = requests.get(
            url='https://proxy.scrapeops.io/v1/',
            params={
                'api_key': scrapeops_api_key,
                'url': URL,
                'bypass': 'cloudflare',
            },
        )
    except:
        raise Exception("Error getting data for", URL)

    return BeautifulSoup(response.content, "html.parser")


class UseScrapper:
    def __init__(self, URL: str = None, element=None):
        print(URL, element)
        if (URL != None and element == None):
            self.soup = use_requests(URL)
        elif (URL == None and element != None):
            self.soup = element
        else:
            raise Exception(
                "You have to provide either an URL or a HTML Element")

    def pretty_print(self):
        print(self.soup.prettify())

    def get_element_by_tagNclass(self, tagName: str, className: str, index: int = 0):
        elements = self.soup.find_all(
            tagName, class_=className)
        return elements[index] if len(elements) > 0 else None

    def get_text_by_tagNclass(self, tagName: str, className: str, index: int = 0, get_attribute: str = None) -> str:
        elements = self.soup.find_all(
            tagName, class_=className)
        if (len(elements) > 0 and get_attribute != None):
            return elements[index].get(get_attribute)
        elif (len(elements) > 0 and get_attribute == None):
            return elements[index].text.strip()
        else:
            return "Not found"
