import requests
from bs4 import BeautifulSoup
import time

def get_match_list(number_of_pages, website):
    list_of_links = []
    prefix = "https://siege.gg"
    for page in range(number_of_pages, 0, -1):
        r = requests.get(website + str(page))
        soup = BeautifulSoup(r.content, "html5lib")
        div = soup.find("div", attrs={"class": "matches__results tab-pane fade show active"})
        links = div.select("a[class*='match--h']")
        for link in range(len(links)):
            list_of_links.append(prefix + links[-link]['href'])
        time.sleep(3)
    return list_of_links
