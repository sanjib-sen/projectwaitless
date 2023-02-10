import requests
from bs4 import BeautifulSoup
from os import getenv
from dotenv import load_dotenv

load_dotenv()
scrapeops_api_key = getenv('scrapeops_api_key')


def use_requests(URL):
    '''
    The ra.co website uses cloudflare to protect their website from scraping.
    To Bypass that, we had to use scrapeops as a proxy
    '''

    try:
        response = requests.get(
            url='https://proxy.scrapeops.io/v1/',
            params={
                'api_key': scrapeops_api_key,
                'url': URL,
                'bypass': 'cloudflare',
            },
        )
        return BeautifulSoup(response.content, "html.parser")
    except:
        raise Exception("Error getting data for", URL)


class UseScrapper:
    '''
    You can use this class either providing an URL or a HTML element.
    Just make sure that you are using the appropriate parameter.
    Providing an url will make the scrapper automatically grab the full html from the url
    '''

    def __init__(self, URL: str = None, element=None):
        if (URL != None and element == None):
            self.soup = use_requests(URL)
        elif (URL == None and element != None):
            self.soup = element
        else:
            raise Exception(
                "You have to provide either an URL or a HTML element")

    def get_element_by_tagNclass(self, tagName: str, className: str, index: int = 0):
        '''
        This repo can be used for getting the element based on tag and classname
        If there are multiple elements with the same tag and classname, provide an index.
        '''
        elements = self.soup.find_all(
            tagName, class_=className)
        return elements[index] if len(elements) > index else None

    def get_text_by_tagNclass(self, tagName: str, className: str, index: int = 0, get_attribute: str = None) -> str:
        '''
        This repo can be used for both getting textContent and attribute values.
        To get text, just provide the tag and classname.
        If there are multiple elements with the same tag and classname, provide an index.
        To get an attribute e.g. "href" use get_attribute="href" parameter
        '''
        elements = self.soup.find_all(
            tagName, class_=className)
        if (len(elements) > index and get_attribute != None):
            return elements[index].get(get_attribute)
        elif (len(elements) > index and get_attribute == None):
            return elements[index].text.strip()
        else:
            return "Not found"
